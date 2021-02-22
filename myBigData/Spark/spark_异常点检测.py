from pyspark.sql import SparkSession
from pyspark.sql.types import Row, StructType, StructField, StringType, IntegerType
from pyspark import SparkContext, SparkConf
from pyspark.sql import functions as F
from pyspark.sql import types as T

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf=conf)
spark = SparkSession.builder.enableHiveSupport().getOrCreate()

# metric_meta = spark.read.format("jdbc").options(url="jdbc:mysql://localhost:3306/spark",
#                                                 driver="com.mysql.jdbc.Driver",
#                                                 dbtable="student",
#                                                 user="root",
#                                                 password="Dosea0118").load()

metric_meta = spark.read.format("jdbc").options(url="jdbc:mysql://10.39.38.13:3306/metric_alg",
                                                driver="com.mysql.jdbc.Driver",
                                                dbtable="metric_outlier_info_raw",
                                                user="root",
                                                password="123456").load()

metric_meta.printSchema()
metric_meta.show(10)
print(metric_meta)

# 累加器
start = sc.accumulator(160000)

# 原始数据， 来源于hive 的 orc文件
metric_path = "/data/copy_ods_detail_data/data_date=2020-07-*[0-9]"
metric_df = spark.read.orc(metric_path)  # orc 是一种hive 文件格式
step = 10000


def filter_func3(data_list):
    # data_list = set(data_list)
    def in_list(df_col2, df_col3, df_col5):
        if (df_col2, df_col3, df_col5) in data_list:
            return True
        return False

    return F.udf(in_list, T.BooleanType())


while True:
    # 1, 分步 （10000）， 首先过滤出 10000 个数据, 滑窗10000
    metric_meta_sample = metric_meta.filter((metric_meta.id >= start.value) & (metric_meta.id < start.value + step))
    # 2, 数据取其中三列，组成（x.metric, x.equip_id, x.staid）
    filter_list = metric_meta_sample.rdd.map(lambda x: (x.metric, x.equip_id, x.staid))
    # 3, 广播变量
    filter_list = sc.broadcast(set(filter_list.collect()))

    if len(filter_list.value) == 0:
        break

    # 4,
    in_list_udf3 = filter_func3(filter_list.value)
    one_metric = metric_df.filter(in_list_udf3("_col2", "_col3", "_col5"))
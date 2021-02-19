from pyspark.sql import SparkSession
from pyspark.sql.types import Row, StructType, StructField, StringType
from pyspark import SparkContext, SparkConf

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf=conf)
spark = SparkSession.builder.getOrCreate()

peopleRDD = sc.textFile('../data/text4.txt')
schemaString = "name age"
fields = list(map(lambda fieldName: StructField(fieldName, StringType(), nullable=True), schemaString.split(" ")))
# 1. 创建表头 schema
schema = StructType(fields)
# 2. 创建表内容, RDD
rowRDD = peopleRDD.map(lambda line: line.split(',')).map(lambda attributes: Row(attributes[0], attributes[1]))
# 3. 创建DF (表头， 表内容)
peopleDF = spark.createDataFrame(rowRDD, schema)

# 必须注册为临时表才能供下面查询使用
peopleDF.createOrReplaceTempView("people")
res = spark.sql("SELECT * FROM people")
res.show()

# #########################
# +-------+---+
# |   name|age|
# +-------+---+
# |   小明| 18|
# |   小白| 21|
# |Michael|   |
# |   Andy| 30|
# | Justin| 19|
# +-------+---+

from pyspark.sql import SparkSession
from pyspark.sql.types import Row, StructType, StructField, StringType, IntegerType
from pyspark import SparkContext, SparkConf

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf=conf)
spark = SparkSession.builder.getOrCreate()

studentRDD = spark.sparkContext.parallelize(["3 Rongcheng M 26", "4 Guanhua M 27"]).map(lambda line: line.split(" "))
# 下面要设置模式信息
schema = StructType([StructField("name", StringType(), True),
                     StructField("gender", StringType(), True),
                     StructField("age", IntegerType(), True)])
rowRDD = studentRDD.map(lambda p: Row(p[1].strip(), p[2].strip(), int(p[3])))
# 建立起Row对象和模式之间的对应关系，也就是把数据和模式对应起来
studentDF = spark.createDataFrame(rowRDD, schema)

prop = {}
prop['user'] = 'root'
prop['password'] = 'Dosea0118'
prop['driver'] = "com.mysql.jdbc.Driver"
studentDF.write.jdbc("jdbc:mysql://localhost:3306/spark", 'student', 'append', prop)

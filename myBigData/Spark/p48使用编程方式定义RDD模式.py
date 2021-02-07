# -*- coding: utf-8 -*-

"""
@Time        : 2020/9/23
@Author      : dosea
@File        : 使用编程方式定义RDD模式
@Description : 
"""
from pyspark.sql.types import *
from pyspark import Row
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()

# 1 生成表头
schemaString = "name age"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split(" ")]
schema = StructType(fields=fields)

# 2 生成表中记录
lines = spark.sparkContext.textFile("file:///usr/local/spark/examples/src/main/resources/people.txt")
parts = lines.map(lambda x: x.split(","))
people = parts.map(lambda p:Row(p[0], p[1].strip()))

# 3
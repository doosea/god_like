# -*- coding: utf-8 -*-

"""
@Time        : 2020/9/23
@Author      : dosea
@File        : Spark_SQL_demo
@Description : 
"""
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf=conf)
spark = SparkSession.builder.config(conf=conf).getOrCreate()

people = spark.read.json("file:///usr/local/spark/examples/src/main/resources/people.json")
people.show()


spark.createDataFrame
# -*- coding: utf-8 -*-

"""
@Time        : 2020/9/23
@Author      : dosea
@File        : 4.2.4综合实例
@Description : 
"""
from pyspark import SparkContext, SparkConf, sql


conf = SparkConf().setMaster("local").setAppName("App")
sc = SparkContext(conf=conf)
data = [("spark", 2), ("spark", 6), ("Hadoop", 4), ("Hadoop", 6)]
rdd = sc.parallelize(data)
rdd_res = rdd.mapValues(lambda x: (x, 1)).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1])).mapValues(lambda x: x[0] / x[1]).collect()

print(rdd_res)


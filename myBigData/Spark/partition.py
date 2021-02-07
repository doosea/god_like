# -*- coding: utf-8 -*-

"""
@Time        : 2020/9/23
@Author      : dosea
@File        : partition
@Description : 
"""
from pyspark import SparkContext, SparkConf


def MyPartitioner(key):
    return key % 10


def main():
    conf = SparkConf().setMaster(value="local").setAppName("Dosea Spark App")
    sc = SparkContext(conf=conf)
    data = sc.parallelize(range(10), 4)
    data.map(lambda x: (x, 1)) \
        .partitionBy(10, MyPartitioner) \
        .map(lambda x: x[0]) \
        .saveAsTextFile("file:///home/dosea/桌面/spark")


if __name__ == '__main__':
    main()

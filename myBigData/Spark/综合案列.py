# -*- coding: utf-8 -*-

"""
@Time        : 2020/9/23
@Author      : dosea
@File        : 综合案列
@Description : 
"""
from pyspark import SparkContext, SparkConf


def word_count():
    conf = SparkConf().setMaster("local").setAppName("dhp app")
    sc = SparkContext(conf=conf)
    lines = sc.textFile("file:///home/dosea/桌面/r.txt", 4)
    wordCount = lines.flatMap(lambda x: x.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    wordCount.sortBy()
    print(wordCount.collect())


if __name__ == '__main__':
    word_count()

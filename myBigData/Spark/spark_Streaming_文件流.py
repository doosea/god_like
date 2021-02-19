from operator import add
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext

conf = SparkConf()
conf.setAppName('TestDStream')
conf.setMaster('local[2]')
sc = SparkContext(conf=conf)
ssc = StreamingContext(sc, 10)
lines = ssc.textFileStream('../data/text3.txt')
words = lines.flatMap(lambda line: line.split(' '))
wordCounts = words.map(lambda x: (x, 1)).reduceByKey(add)
wordCounts.pprint()
ssc.start()
ssc.awaitTermination()

# 程序监听 “../data/text3.txt” 目录下的所有新增文件， 测试时，需要在窗口期内新创建文件并写入

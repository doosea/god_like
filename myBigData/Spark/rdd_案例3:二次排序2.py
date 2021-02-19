from pyspark import SparkContext, SparkConf
from operator import gt


class SecondarySortKey(object):
    def __init__(self, k):
        self.c1 = k[0]
        self.c2 = k[1]

    def __gt__(self, other):
        if other.c1 == self.c1:
            return gt(self.c2, other.c2)
        else:
            return gt(self.c1, other.c1)


conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf=conf)
rdd1 = sc.textFile("../data/text3.txt/*.txt")
rdd2 = rdd1.filter(lambda line: len(line.strip()) > 0)  # 去除空行
rdd3 = rdd2.map(lambda x: ((int(x.split(" ")[0]), int(x.split(" ")[1])), x))
rdd4 = rdd3.map(lambda x: (SecondarySortKey(x[0]), x[1]))
rdd5 = rdd4.sortByKey(False)
rdd6 = rdd5.map(lambda x: x[1])
rdd6.foreach(print)

# 报错。。。。

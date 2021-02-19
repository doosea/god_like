from pyspark import SparkContext, SparkConf

i = 0


def getindex():
    global i
    i += 1
    return i


conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf=conf)
rdd = sc.textFile("../data/text2.txt/*.txt")
res1 = rdd.filter(lambda line: (len(line.strip()) > 0))  # 去除空行
res2 = res1.map(lambda x: (int(x.strip()), ""))  # 变成键值对
res3 = res2.repartition(1)
res4 = res3.sortByKey(True)
res5 = res4.map(lambda x: x[0])
res6 = res5.map(lambda x: (getindex(), x))
res6.saveAsTextFile("../data/res2out")

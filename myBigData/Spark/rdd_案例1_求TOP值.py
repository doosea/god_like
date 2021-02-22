from pyspark import SparkContext, SparkConf

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf=conf)
lines_rdd = sc.textFile("../data/text1.txt/*.txt")
result1 = lines_rdd.filter(lambda line: (len(line.strip()) > 0 and len(line.split(",")) == 4))
result2 = result1.map(lambda x: x.split(",")[2])
result3 = result2.map(lambda x: (int(x), ""))
result4 = result3.repartition(1)
result5 = result4.sortByKey(False)
result6 = result5.map(lambda x: x[0])
result7 = result6.take(3)
print(result7)

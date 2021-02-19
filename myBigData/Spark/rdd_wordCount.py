from pyspark import SparkConf, SparkContext


def a(x):
    return 'a' in x


conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf=conf)
logFile = "file:///home/dosea/workspaces/python_workspaces/god_like/myBigData/README.md"
logData = sc.textFile(logFile, 2).cache()
numAs = logData.filter(a).count()
numBs = logData.filter(lambda line: 'b' in line).count()
print(numAs, numBs)

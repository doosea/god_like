from pyspark import SparkContext, SparkConf


def main():
    # 生成一个SparkContext对象
    conf = SparkConf().setMaster('local').setAppName('spark_sort')
    sc = SparkContext(conf=conf)
    line = sc.textFile("../data/text3.txt/*.txt")

    # 剔除空行列，txt文件最后行能会读入空行列
    rdd = line.filter(lambda x: (len(x.strip()) > 0))
    # 对每行拆成((5,3),(5 3))的格式，第一项排序用列，第二项则为最后结果列
    rdd1 = rdd.map(lambda x: ((int(x.split(" ")[0]), int(x.split(" ")[1])), x))
    # 排序，由于False为降序，对第二列加-号实现降序
    rdd2 = rdd1.sortBy(lambda x: (x[0][0], -x[0][1]), False)
    # 排序后提取结果列，rdd1做拆分的原因在此
    rdd3 = rdd2.map(lambda x: x[1])
    print(rdd3.collect())
    # 保存结果，文件夹路径必须不存在，否则报错
    # rdd3.saveAsTextFile("file:///usr/local/spark/mycode/rdd/filesort2")


if __name__ == '__main__':
    main()

# ps：RDD中sortBy是基于键值对操作，rdd1步骤操作既为了达到取结果也为了生成键值对

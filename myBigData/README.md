# BigData
hadoop 伪分布式 + spark 单机模式
## hadoop 安装
- [Hadoop在Ubuntu的安装和使用](https://zhuanlan.zhihu.com/p/112275959)

- 启动Hadoop: 
    - start-dfs.sh
    - jps
    - http://localhost:9870/

1. HDFS: 分布式文件系统

2. MapReduce

3. YARN 资源调度

## Spark 

- [Ubuntu 16.04下Spark安装与开发环境搭建](https://blog.csdn.net/lengconglin/article/details/77847623)
- [子雨大数据之Spark入门教程(Python版)](http://dblab.xmu.edu.cn/blog/1709-2/)
- 使用 spark 之前， 首先启动hadoop 
    - start-dfs.sh
    - start-all.sh

1. spark 部署模式:
    - 单机模式
    - 集群部署
        - standalone 模式
        - YARN 模式
        - Mesos模式
        
2. 在pyspark中运行代码
    - pyspark  == pyspark --master local[*]     
      
3. spark-submit 提交应用程序
    ```
   spark-submit 
   --master <msater-url>         # 启动模式
   --deploy-mode <deploy-mode>   # 部署模式
   <application-file>            # python 代码文件
   [application-argumnets]       # 传递给主类的主方法的参数
    ```
   - spark-submit ./wordCount.py 
   - spark-submit --master yarn /home/dosea/workspaces/python_workspaces/god_like/myBigData/Spark/wordCount.py
### Spark core : RDD 编程
1. RDD 创建
    - sc.textFile() 读取数据，在内存中生成RDD
    - sc.parallelize() 在Driver中一个已经存在的集合（数组）上创建
    
2. RDD 操作
    - 转换操作 Transformation: 基于现有的数据集创建一个新的数据集 (惰性操作)， 只记录转换过程，并不发生真正计算
        - map(func): 将每个元素传递到函数func中，并将结果返回为一个新的数据集
        - filter(func) : 筛选出满足函数func的元素，并返回一个新的数据集
        - flatMap(func): 与map()相似，但每个输入元素都可以映射到0或多个输出结果
        - groupByKey(): 应用于(K,V)键值对的数据集时，返回一个新的(K, Iterable)形式的数据集
        - reduceByKey(func): 应用于(K,V)键值对的数据集时，返回一个新的(K, V)形式的数据集，其中的每个值是将每个key传递到函数func中进行聚合
    - 行动操作 Action: 在数据集上进行运算，返回计算值
        - count() : 返回数据集中的元素个数
        - collect() : 以数组的形式返回数据集中的所有元素
        - first(): 返回数据集中的第一个元素
        - take(n): 以数组的形式返回数据集中的前n个元素
        - reduce(func) 通过函数func（输入两个参数并返回一个值）聚合数据集中的元素 
        - foreach(func) 将数据集中的每个元素传递到函数func中运行*

3. RDD 持久化

    RDD采用惰性求值的机制，每次遇到行动操作，都会从头开始执行计算。可以通过持久化（缓存）机制避免这种重复计算的开销
    - persist() 
        - persist(MEMORY_ONLY) 
        - persist(MEMORY_AND_DISK) 
    - cache() == persist(MEMORY_ONLY) 
    - unpersist()：持久化的RDD从缓存中移除。
    
4. 分区

    RDD是弹性分布式数据集， 分区的个数尽量等于集群中的CPU核心（core）数目。
    ```
    array = [1,2,3,4,5]
    rdd = sc.parallelize(array,2) #设置两个分区 
    ```
   - 打印元素
     ```
      rdd.foreach(print)
      rdd.map(print)
      rdd.collect().foreach(print)
      rdd.take(100).foreach(print)
     ```
5. 键值对RDD
    - 创建
        - 文件中加载: sc.textFile()   
        - 通过并行集合（列表）创建RDD : sc.parallelize(list)
    - 转换操作
        - reduceByKey(func)
        - groupByKey()： 对具有相同键的值进行分组
        - keys()： 把键值对RDD中的key返回形成一个新的RDD
        - values()： 把键值对RDD中的value返回形成一个新的RDD
        - sortByKey()： 返回一个根据键排序的RDD。
        - sortBy()： 
            - sortBy(lambda x:x[0], False) 根据key降序 ==  sortByKey(False)
            - sortBy(lambda x:x[1], False) 根据value 降序
        - mapValues(func): 对键值对RDD中的每个value都应用一个函数，key不会发生变化
        - join()
        
6. 共享变量
    - 广播变量（broadcast varibales）: 把变量在所有节点的内存之间进行共享
        - SparkContext.broadcast(v)
    - 累加器(accumulators): 支持在所有不同节点之间进行累加计算（
        - SparkContext.accumulator():  数值型的累加器
7. 数据读写
    - 文件数据读写, file_path 是一个目录，目录下所有文件都会呗读取到RDD中
        - rdd = sc.textFile(file_path)
        - rdd.saveAsTextFile(file_path)

    - 读写Hbase数据       

### Spark SQL : DataFrame 
 RDD是分布式的 Java对象的集合， DataFrame是一种以RDD为基础的分布式数据集，也就是分布式的Row对象的集合，
 DataFrame 比 RDD 效率高， 并且支持SQL查询。
1. DataFrame 创建
    ```
   from pyspark import SparkSession 
   spark=SparkSession.builder.getOrCreate()
   df = spark.read.json()
   df = spark.read.text()
   df = spark.read.parquet()
   
   # 或者
   df = spark.read.fromat("json").load()
   df = spark.read.fromat("text").load()
   df = spark.read.fromat("parquet").load()
    ```
2. DataFrame 操作 
    - df.printSchema() ：  打印模式信息
    - df.select(df.name,df.age + 1).show()  选择多列
    - df.filter(df.age > 20 ).show()  条件过滤
    - df.groupBy("age").count().show() 分组聚合
    - df.sort(df.age.desc()).show() 排序
    - df.sort(df.age.desc(), df.name.asc()).show() 多列排序
    - df.select(df.name.alias("username"),df.age).show() 对列进行重命名
    
3. RDD 转化为DataFrame    
    - 利用反射机制推断RDD模式
    - 使用编程方式定义RDD模式
      
4. Spark SQL 读写数据库
    - pyspark --jars /usr/local/spark/jars/mysql-connector-java-8.0.23.jar --driver-class-path /usr/local/spark/jars/mysql-connector-java-8.0.23.jar 
    - 驱动报错问题： https://blog.csdn.net/u013220482/article/details/106585843
### Spark Streaming : Dstream

1. 编写Spark Streaming程序的基本步骤
    - 通过创建输入DStream来定义输入源
    - 通过对DStream应用转换操作和输出操作来定义流计算。
    - 用streamingContext.start()来开始接收数据和处理流程。
    - 通过streamingContext.awaitTermination()方法来等待处理结束（手动结束或因为错误而结束）。
    - 可以通过streamingContext.stop()来手动结束流计算进程。
2. 创建StreamingContext对象
    ```
    from pyspark import SparkContext, SparkConf
    from pyspark.streaming import StreamingContext
    conf = SparkConf()
    conf.setAppName('TestDStream')
    conf.setMaster('local[2]')
    sc = SparkContext(conf = conf)
    ssc = StreamingContext(sc, 1) 
    # 第二个参数是窗口期时间， 1表示每隔1秒钟就自动执行一次流计算
    ```

3. 高级数据源
    - Kafka: 
        - [真的，Kafka 入门一篇文章就够了](https://segmentfault.com/a/1190000021138998)
        - Broker：Kafka集群包含一个或多个服务器，这种服务器被称为broker
        - Topic：每条发布到Kafka集群的消息都有一个类别，这个类别被称为Topic。（物理上不同Topic的消息分开存储，逻辑上一个Topic的消息虽然保存于一个或多个broker上但用户只需指定消息的Topic即可生产或消费数据而不必关心数据存于何处）
        - Partition：Partition是物理上的概念，每个Topic包含一个或多个Partition.
        - Producer：负责发布消息到Kafka broker
        - Consumer：消息消费者，向Kafka broker读取消息的客户端。
        - Consumer Group：每个Consumer属于一个特定的Consumer Group（可为每个Consumer指定group name，若不指定group name则属于默认的group）
    - Flume
### Spark MLlib
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
### RDD 编程
1. RDD 创建
    - sc.textFile() 读取数据，在内存中生成RDD
    - 
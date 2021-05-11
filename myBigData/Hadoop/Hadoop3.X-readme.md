# Hadoop
## Hadoop 入门，部署
0. 安装与启动
- 启动Hadoop: 
    - start-dfs.sh : 启动HDFS (NameNode + SecondaryNameNode + DataNode)
    - start-yarn.sh : 启动yarn (resourcemanager + nodemanagers)
    - start-all.sh: 一键启动 dfs+ yarn
    - jps: 查看启动的java 进程
    - http://localhost:9870/ ： web 端口
- 关闭HDFS
    - stop-all.sh 关闭所有
    - stop-yarn.sh
    - stop-dfs.sh


1. 常用端口号：
    - Hadoop3.x:
        - HDFS NameNode 内部常用端口: 8020 / 9000/ 9820
        - HDFS NameNode 对用户查询端口: 9870
        - Yarn 查看任务运行情况端口： 8088
        - 历史服务器： 19888
    - Hadoop2.x
        - HDFS NameNode 内部常用端口: 8020 / 9000
        - HDFS NameNode 对用户查询端口: 50070
        - Yarn 查看任务运行情况端口： 8088
        - 历史服务器： 19888  
2. 常用的配置文件
    - Hadoop3.x:
        - core-site.xml
        - hdfs-site.xml
        - yarn-site.xml
        - mapred-site.xml
        - workers
    - Hadoop2.x:
        - core-site.xml
        - hdfs-site.xml
        - yarn-site.xml
        - mapred-site.xml
        - slaves      
        
## HDFS
1. 基本概念
    1. 分块存储Block， 默认128M
    2. 寻址时间， HDFS的BLOCK设置太小，会增加寻址时间， 设置太大，传输时间会明显大于寻址时间，
    3. 寻址时间为传世时间的1%， 为最佳状态
2. HDFS 的Shell操作
    - hdfs dfs (不建议使用)
    - hadoop fs （建议使用 hadoop fs [generic options]）
        1.创建文件夹： hadoop fs -mkdir [路径] 
        2. 上传：
            - 剪切本地文件到hdfs: hadoop fs -moveFromLocal [local路径] [hdfs路径]
            - 复制本地文件到hdfs: hadoop fs -copyFromLocal [local路径] [hdfs路径]
            - 复制本地文件到hdfs： hadoop fs -put [local路径] [hdfs路径]
            - 追加文件到一个已经存在的文件末尾： hadoop fs -appendToFile [local路径] [hdfs路径]
        3. 下载：
            - hadoop fs -copyToLocal [hdfs路径] [local路径] 
            - hadoop fs -get [hdfs路径] [local路径] 
        4. 直接操作
            - hadoop fs -ls [hdfs路径]  
            - hadoop fs -cat  [hdfs路径]
            - hadoop fs -mkdir [hdfs路径]
            - hadoop fs -cp [hdfs路径1] [hdfs路径2]
            - hadoop fs -mv [hdfs路径1] [hdfs路径2]
            - hadoop fs -tail [hdfs路径] ：显示一个文件的末尾的1kb的数据
            - hadoop fs -rm [-r] [hdfs路径] ：删除
            - hadoop fs -du [-s] [-h] [hdfs路径] ：统计文件夹的大小信息
            
             
3. HDFS API 操作
4. HDFS 读写操作
    1. 写操作， chunk , packet, pipline, 一份写入磁盘，一份直接pipline 往下传递
        - 客户端向
    2. 读操作
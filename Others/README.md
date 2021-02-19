# 暂时临时记录

## linux 
### 权限管理
1. 改变文件所有权（chown）
    ```shell script
    sudo chown username myfile       // 将myfile文件的所有权改为username的
   
    chown -R username /files/work    // 加入-R, work后文件夹以及文件夹里的所有文件和子目录所有权都变为username
    ```
   
2. 改变文件的权限（chmod）
    ```shell script
    sudo chmod 777 filename   //  filename 的权限变为 可读可写可执行
 
    sudo chmod -R 754 director   // director文件夹所有文件的权限变为 可读可写可执行
    ```
   - 三个数字顺序分别代表 用户、用户组、其他 
   - 4 可读, 2 可写, 1可执行, 0无权限
   
3. 用户创建 `useradd`
     - `-g`可以设定用户的主要组
     - `-G`可以设定用户的附加组
     
     ```shell script
     useradd -g 组名 用户名              用户建立时为其创建或指定一个组
     useradd -m 用户名                   创建用户,并为用户建立主目录
     ```
   
   
   
## ubuntu 软件多版本管理 update-alternatives
以jdk 为例 [参考连接](https://www.jb51.cc/servers/502715.html)
1. 安装 oracle-jdk1.8 和 open jdk 11
2. 注册
    -  update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-11-openjdk-amd64/bin/java 2222
    -  update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk1.8/jdk1.8.0_261/bin/java 3333
    - 参数解析
        - 第一个参数--install表示向update-alternatives注册服务名
        - 第二个参数是注册最终地址，成功后将会把命令在这个固定的目的地址做真实命令的软链，以后管理就是管理这个软链；
        - 第三个参数：服务名（java），以后管理时以它为关联依据。
        - 第四个参数，被管理的命令绝对路径。
        - 第五个参数，优先级，数字越大优先级越高。
3. 查看已注册列表
    - update-alternatives --display java
4. 修改java 版本
    - update-alternatives --config java
    - 输入对应序号
    - java -version 验证
        
## 协程(Coroutine)
1. 实现方式：
    - greenlet 实现协程
    - yield 关键字
    - asyncio 
    - async & awit 关键字 （py3.5之后推荐）
    
2. 协程函数
    - 定义协程函数： `async def 函数名`
    - 创建协程对象： `协程函数()`
    - 快速上手
        ```python
        import asyncio
        
        
        async def func():
            print("this is Coroutine function")
        
        res = func()
       
        # python 3.7 之前的写法 
        loop = asyncio.get_event_loop()
        loop.run_until_complete(res)
        # python 3.7之后的写法
        asyncio.run(res)
        ```
   
3. await + 可等待的对象
    - 可等待的对象： `协程对象`， `Future对象`, `Task对象` （IO等待）
    - await 就是等待对象的值得到结果后再继续向下走   
        
4. Task 对象： 在事件循环中添加多个任务
    - `asyncio.create_task(协程对象)`
    
5. Future对象


## 哈希

> 参考连接： [什么是 hash？](https://www.zhihu.com/question/26762707/answer/890181997)

1. 什么是Hash
    - 基本原理就是把任意长度的输入，通过Hash算法变成固定长度的输出。（ MD5和SHA ）
    
2. Hash 特点
    - 从hash值不可以反向推导出原始的数据
    - 输入数据的微小变化会得到完全不同的hash值，相同的数据会得到相同的值
    - 哈希算法的执行效率要高效，长的文本也能快速地计算出哈希值
    - hash算法的冲突概率要小
    
3. Hash冲突的解决方案
    - 链地址法 （java的数据结构HashMap， JDK1.8中，针对链表上的数据超过8条的时候，使用了红黑树进行优化）
       - [Java集合之一—HashMap](https://blog.csdn.net/woshimaxiao1/article/details/83661464)
    - 开放地址法
    
4. 应用场景
    - 信息加密
    - 数据校验
    - 负载均衡

# 面试题整理
##  Elasticsearch 
1. Elasticsearch 的索引机制
2. 倒排索引： 主要由两个部分组成：`单词词典` 和 `倒排文件` 。
    - 倒排索引是实现“单词-文档矩阵”的一种具体存储形式，通过倒排索引，可以根据单词快速获取包含这个单词的文档列表。
    - 单词词典: 单词词典是由文档集合中出现过的所有单词构成的字符串集合
    - 倒排列表: 倒排列表记载了出现过某个单词的所有文档的文档列表及单词在该文档中出现的位置信息，
    - 倒排文件：所有单词的倒排列表往往顺序地存储在磁盘的某个文件里，这个文件即被称之为倒排文件
3. 如何调优
    - 动态索引层面： 基于模板+时间+rollover api 滚动创建索引
    - 存储层面： 冷热数据分离存储，对于冷数据不会再写入新数据，可以考虑定期 force_merge 加 shrink 压缩操作，节省存储空间和检索效率。
    - 部署层面： 临时扩容
4. master 节点的选举
    - 确认候选主节点数达标 discovery.zen.minimum_master_nodes；
    - 选举的是排序后的第一个MasterCandidate(即master-eligible node)
    - 排序规则:
       - 当clusterStateVersion越大，优先级越高。这是为了保证新Master拥有最新的clusterState(即集群的meta)，避免已经commit的meta变更丢失。因为Master当选后，就会以这个版本的clusterState为基础进行更新
       - 当clusterStateVersion相同时，节点的Id越小，优先级越高。
5. 详细描述一下 Elasticsearch 索引文档的过程(单文档写入)      
    - 客户向集群某节点1发送写入数据请求（如果没有指定路由/协调节点，请求的节点扮演路由节点的角色。）
    - 节点 1 接受到请求后，使用文档_id 来确定文档属于哪个分片。请求会被转到该分片为主分片所在的节点上（假设3号）。
    - 节点 3 在主分片执行写操作， 如果成功，则将写操作请求并行转发到副本分片所在节点上，等待结果返回。
        所有副本也写成功之后，节点3向协调节点（1）报告成功，协调节点向请求客户端报告写入成功。
    - 文档获取分片的过程？
        - 对文档id 通过hash函数，然后对分片数量取余。
        - shardId = hash(_routing) % num_primary_shards 
6. 详细描述一下 Elasticsearch 搜索的过程        
    - 搜索拆分为两个阶段： query then fetch， query定位，但是不取
        - 查询阶段
             1. 客户端发送请求到协调节点, 协调节点会创建一个大小为 from+size 的空优先队列
             2. 协调节点将请求转发到索引的每个主分片或者副本分片中， 每个分片在本地执行查询，并添加结果到大小为from+size 的本地优先队列
             3. 每个分片返回各自优先队列给协调节点，合并这些值到自己的优先队列中来产生一个全局排序后的结果列表。
             ```
              1. 协调节点广播请求到索引中每一个节点的分片拷贝， 查询请求可以被某个主分片或某个副本分片处理， 所以更多的副本可以增加吞吐量。
              2. 协调节点将在之后的请求中轮询所有的分片拷贝来分摊负载。
              3. 每个分片创建的结果集足够大， 均可以满足全局的搜索请求。
              4. 分片返回一个轻量级的结果列表到协调节点，它仅包含文档 ID 集合以及任何排序需要用到的值，例如 _score 
             ```  
        - 取回阶段
            1. 协调节点辨别出哪些文档需要被取回并向相关的分片提交多个 GET 请求。（multi-get request）
            2. 每个分片加载并 丰富 文档(_source)，如果有需要的话，接着返回文档给协调节点。
            3. 一旦所有的文档都被取回了，协调节点返回结果给客户端。
        - 搜索选项
            - 超时问题timeout： 通常分片处理完它所有的数据后再把结果返回给协同节点，协同节点把收到的所有结果合并为最终结果。
                这意味着花费的时间是最慢分片的处理时间加结果合并的时间。如果有一个节点有问题，就会导致所有的响应缓慢。
                
7. 详细描述-下Elasticsearch更新和删除文档的过程。    
    - 更新和删除 也是写操作， 并不是真正修改原文档    
    - 分片有很多分段，写操作只能写入打开的分段，标记为删除，但是会在结果中被过滤掉。（ 读操作只能读取关闭的分段）     
    
## Spark Hadoop HDFS 
1. Hadoop 有哪些组件？
    - HDFS集群：负责海量数据的存储，集群中的角色主要有 NameNode / DataNode/SecondaryNameNode。
        - HDFS 副本存放机制： 两地三中心（机架感知概念）
        - NameNode 作用：  
            - 管理文件系统的元数据/名字空间/目录树 
            - 管理DataNode汇报的心跳日志/报告
            - 管理数据与节点之间的映射关系（管理文件系统中每个文件/目录的block块信息）
        - DataNode作用
            - 负责数据的读写操作
            - 周期性的向NameNode汇报心跳日志/报告
            - 执行数据流水线的复制  
            
    - YARN集群：负责海量数据运算时的资源调度，集群中的角色主要有 ResourceManager /NodeManager
    - MapReduce：它其实是一个应用程序开发包。

2. HDFS数据写入流程
    - (1)客户端向NameNode发出写文件请求，
    - (2)NameNode 首先会检测元数据的目录树, 检查权限, 检查目标文件是否已存在，父目录是否存在，返回是否可以上传。
    - (3)客户端收到可以上传的响应后， 把待上传文件切块（128M）, 再次给namenode发送请求，上传第一个block块。
    - (4)NameNode，首先会检测其保存的datanode信息，确定该文件块存储在那些节点上；最后，响应给客户端一组datanode节点信息。
    - (5)客户端根据收到datanode节点信息，首先就近与某台datanode建立网络连接；然后该datanode节点会与剩下的节点建立传输通道，通道连通后返回确认信息给客户端；表示通道已连通，可以传输数据。
    - (6)客户端收到确认信息后，通过网络向就近的datanode节点写第一个block块的数据；就近的datanode收到数据后，首先会缓存起来；
      然后将缓存里数据保存一份到本地，一份发送到传输通道,让剩下的datanode做备份(pipeline)    
    - (7)第一个block块写入完毕，若客户端还有剩余的block未上传；则客户端会从（3）开始，继续执行上述步骤；直到整个文件上传完毕
    - 写完数据，关闭输输出流。发送完成信号给NameNode。
    
3. HDFS数据读取流程
    - (1) 客户端向NameNode发起文件读请求， NameNode 检查文件位置,来确定请求文件 block 所在的位置
    - (2) NameNode会视情况返回文件的部分或者全部block列表，对于每个block，NameNode 都会返回含有该 block 副本的 DataNode 地址
    - (3) 这些返回的 DN 地址，会按照集群拓扑结构得出 DataNode 与客户端的距离，然后进行排序，排序两个规则：网络拓扑结构中距离 Client 近的排靠前；
          心跳机制中超时汇报的 DN 状态为 STALE，这样的排靠后；
    - (4) Client 选取排序靠前的 DataNode 来读取 block，如果客户端本身就是DataNode,那么将从本地直接获取数据
    - (5) 当读完列表的 block 后，若文件读取还没有结束，客户端会继续向NameNode 获取下一批的 block 列表
    - (6) 读取完一个 block 都会进行 checksum 验证, 如果读取 DataNode 时出现错误，客户端会通知 NameNode，然后再从下一个拥有该 block 副本的DataNode 继续读。
    
2. 为什么spark要把操作分为transform和action? (转换操作 和 行动操作)
    - 所有的transformation都是采用的惰性机制， 只是将transformation提交是不会执行计算的，计算只有在action被提交的时候才被触发。
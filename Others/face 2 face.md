## 简历项目细节：
1. python 计算引擎 flask

2. jupyterlab

3. java后端

4. 算法 Xgboost and 推荐算法
    
    
## python 面试题
1. 锁 ， 乐观锁，悲观锁   
    - GIL 全局解释性锁：
    - 限制多线程同时执行,保证同一时间只有一个线程执行,所以cpython里的多线程其实是伪多线程
2. 进程、线程、协程， 进程里有线程,线程里有协程.
    - 进程是系统资源分配的最小单位
    - 线程调度执行的最小单位,
    - 协程是一种用户态的轻量级线程,协程的调度完全由用户控制.协程拥有自己的寄存器上下文和栈
    - 多进程适合在CPU密集型操作(CPU指令比较多, 如位数多的浮点运算).
    - 多线程适合在IO密集型操作(读写数据操作较多的, 比如爬虫)
3. Flask: Web框架，  Python Web Server Gateway Interface，缩写为WSGI
    - RESTFUL
    - ORM  对象关系映射Object Relational Mapping
    - Django和Flask有什么区别
4. flask 部署 高可用 gunicorn, Nginx+Gunicorn+Gevent+Supervisor+Flask。
    - Nginx：高性能 Web 服务器+负载均衡
    - Gunicorn：高性能 WSGI 服务器；
    - Gevent：把 Python 同步代码变成异步协程的库；
    - Supervisor：监控服务进程的工具；
    - Flask：一个使用Python编写的轻量级 Web 应用框架
    - 启动： gunicorn --bind 0.0.0.0:5080 --workers 8 --worker-class gevent --max-requests 500 --max-requests-jitter 100 --pid gunicorn.pid run:app
5. Python 中@staticmethod 和@classmethod 的区别
    - 普通方法
    - staticmethod 装饰的静态方法与普通函数相同
6. 正向代理和反向代理，  Client 到 Proxy 到 Server
    - 正向代理，直接访问访问不通，找个proxy, 转发请求，简介访问
    - 反向代理： 访问域名，反向代理转发到其中一个节点，但是我们不知道具体哪个节点
7. docker 
    - 快速交付，测试和部署代码
8. 内存泄漏： 动态分配的堆内存。使用完毕后未释放

9. with 上下文管理器

10. is == 的区别， id(身份标识)、type(数据类型)和value(值)
    - == 比较的是值
    - is 比较的是引用地址
    - 小整数使用对象池存储问题[-5, 256]
    - 字符串常量， intern机制，类似于java的intern, 运行时常量池
11. python 装包和拆包（*args 和 **kwargs）
    - *args：用于接受多余的未命名的参数，元组类型；
	- **kwargs：用于接受形参的命名参数，字典类型；
	- args ： 未拆包，是个元祖， *args进行拆包
	- kwargs 是未拆包的,*kwargs 是进行拆包的
	
12. 迭代器（iterator）
    - 实现了迭代器协议的容器对象,两个方法
        - __ next __ ：返回容器的下一个元素
        - _ iter __ ：返回迭代器本身
13. 生成器（generator）
    - 1. 生成器函数, yield关键字
    - 2. 生成器表达式, 列表推导式[] -> ()
14. 赋值，深拷贝，浅拷贝
    - 对象： id(身份标识)、type(数据类型)和value(值)
    - 类型
        - 可变对象： 列表、字典、集合
        - 不可变对象：数字、字符串、元组
    - 引用：
    - copy.copy 浅拷贝 只拷贝父对象，不会拷贝对象的内部的子对象。
    - copy.deepcopy 深拷贝 拷贝对象及其子对象
15. 构造(__new__)和初始化(__init__)
    - 创建一个类的过程是分为两步的，一步是创建类的对象，还有一步就是对类进行初始化。
    - __new__ 是用来创建类并返回这个类的实例， 通常用于控制生成一个新实例的过程。它是类级别的方法
    - __init__ 只是将传入的参数来初始化该实例。 通常用于初始化一个新实例，控制这个初始化的过程，比如添加一些属性， 做一些额外的操作，发生在类实例被创建完以后。
    
16. python 中 @staticmethod 和 @classmethod有什么区别
    - @staticmethod不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样。
    - @classmethod也不需要self参数，但第一个参数需要是表示自身类的cls参数。    
17. python 垃圾回收， python采用的是引用计数机制为主，标记-清除和分代收集两种机制为辅的策略。引用计数的缺陷是循环引用的问题。
    - 引用计数 Reference Counting
    - refchain, 环状双向链表
    - 标记清除， 分代回收
        - 标记清除：创建特殊链表专门用于保存 列表、元组、字典、集合、自定义类等对象，之后再去检查这个链表中的对象是否存在循环引用，如果存在则让双方的引用计数器均 - 1 
        - 分代回收: 对标记清除中的链表进行优化，将那些可能存在循引用的对象拆分到3个链表，链表称为：0/1/2三代，每代都可以存储对象和阈值，当达到阈值时，就会对相应的链表中的每个对象做一次扫描，
            除循环引用各自减1并且销毁引用计数器为0的对象。
       
## java 面试题 ： 集合+ 线程 + JVM
### 1. HashMap ConcurrentHashMap
- [HashMap 一遍就懂！！！！](https://blog.csdn.net/qq_40574571/article/details/97612100)
- [史上最全HashMap面试题汇总](https://blog.csdn.net/QGhurt/article/details/107323702)
1. java.util.Map 接口
    - HashMap: 非线程安全
    - HashTable： 承自Dictionary类，并且是线程安全， 任意时间只有一个线程能够写HashTable, 并发性不如ConcurrentHashMap
    - LinkedHashMap: LinkedHashMap是HashMap的一个子类
    - TreeMap: TreeMap实现SortedMap接口，能够把它保存的记录根据键排序，默认是按键值的升序排序
2. HashMap 存储结构: HashMap是数组+链表+红黑树(JDK1.8增加了红黑树部分)
    - HashMap就是使用哈希表来存储的, 哈希冲突解决方法： 开放地址法和链地址法（java）
    - 哈希桶数组 Node[] table 初始化长度16， （2的n次方， 合数）， Load Factor = 0.75， threshold = length * load Factor, size超过threshold 就会扩容， 两倍，
        modCount记录HashMap内部结构变化发生的次数
    - 当链表长度太长（默认超过8）时， 
    
3. 根据key获取哈希桶数组索引位置： (h ^ (h >>> 16)) & (length -1)
    - 取哈希值： h= key.hashCode()
    - 高位运算： h ^ (h >>> 16)
    - 取模运算： h & (length-1)
    -  a % b == (b-1) & a ,当b是2的指数时，等式成立。
    
4. put()的详细执行
    - 当前哈数桶数组是否为null, 否则resize()
    - key 的hash值计算数组索引下标i, 如果数组对应元素null,创建新节点直接插入，否则    
    - 判断首个元素是否相同， 是覆盖， 否则
    - 判断是否是treeNode, 即是否是红黑树， 是红黑树，直接利用红黑树插入键值对， 否则
    - 遍历table[i], 判断列表长度是否大于8， 大于8转化红黑树，在红黑树中执行插入操作，否则链表插入， 遍历过程中，如果相同，覆盖
    - 插入成功后， size++ 与阈值threshold比较，超过则扩容
    
5. 扩容过程resize()
    - 创建一个新的数组,其容量为旧数组的两倍,并重新计算旧数组中结点的存储位置。结点在新数组中的位置只有两种,原下标位置或原下标+旧数组的大小
        - HashMap在进行扩容时，使用的rehash方式非常巧妙，因为每次扩容都是翻倍，与原来计算的 (n-1)&hash的结果相比，只是多了一个bit位，所以结点要么就在原来的位置，要么就被分配到"原位置+旧容量"这个位置。
    - 链表的对象个数如果达到了8个，此时如果数组长度没有达到64，那么HashMap会先扩容解决，如果已经达到了64，那么这个链表会变成红黑树，结点类型由Node变成TreeNode类型

6. ConcurrentHashMap : 线程安全的HashMap
    -  ConcurrentHashMap 底层数据结构: 数组+链表/红黑二叉树
    -  实现线程安全的方式（重要)
        - 在JDK1.7的时候，ConcurrentHashMap（分段锁）, segment, 每一把锁只锁容器其中一部分数据
        - JDK1.8 的时候已经摒弃了Segment的概念, 并发控制使用 synchronized 和 CAS 来操作
        
7. 红黑树
    1. 5个原则
        - 每个结点要么是红的要么是黑的。  
        - 根结点是黑的。  
        - 每个叶结点（叶结点即指树尾端NIL指针或NULL结点）都是黑的。  
        - 如果一个结点是红的，那么它的两个儿子都是黑的。  
        - 对于任意结点而言，其到叶结点树尾端NIL指针的每条路径都包含相同数目的黑结点
    2. 左旋
        
    3. 右旋
    - 利用红黑树快速增删改查的特点提高HashMap的性能 http://blog.csdn.net/v_july_v/article/details/6105630
    - CAS 自旋锁
8. java  集合 collection（）
    - List 接口
        - Vector
        - ArrayList: 数组存储，连续空间，随机访问效率很高，适合多读取, 初始容量10， 1.5倍扩容
        - LinkedList： 双向链表数据结构， 增加和删除效率比较高，而随机访问效率较差
    - Map接口  
        - Hashmap
        - LinkedHashMap： 链表来维护元素的次序
        - TreeMap
        - HashTable
        - ConcurrentHashMap
    - Set 接口
        - HashSet
        - 
9. 线程
    1. 线程池： 创建线程和销毁线程的花销是比较大的，这些时间有可能比处理业务的时间还要长， 线程池作用就是限制系统中执行线程的数量
        - newSingleThreadExecutor： 单线程化的线程池
        - newFixedThreadPool： 可控制线程最大并发数，超出的线程会在队列中等待
        - newCachedThreadPool： 可缓存线程池，如果线程池长度超过处理需要，可灵活回收空闲线程，若无可回收，则新建线程
        - newScheduledThreadPool：创建一个定长线程池，支持定时及周期性任务执行
    2. 线程池核心参数
        - corePoolSize： 线程池核心线程数最大值
        - maximumPoolSize： 线程池最大线程数大小
        - keepAliveTime： 线程池中非核心线程空闲的存活时间大小
        - unit： 线程空闲存活时间单位
        - workQueue： 存放任务的阻塞队列
            - ArrayBlockingQueue
            - LinkedBlockingQueue
            - SynchronousQuene
            - PriorityBlockingQueue
        - threadFactory： 用于设置创建线程的工厂，可以给创建的线程设置有意义的名字，可方便排查问题。
        - handler： 线程池的饱和策略事件，主要有四种类型
        
10. JVM (类加载、运行时数据区、执行引擎)
    - 运行时数据区： PC计数器， 虚拟机栈， 本地方法栈， 方法区， 堆
    - 堆： 新生代（eden + s0 + s1， 8：1:1） + 老年代， 
    - jdk1.8之前 新生代和老年代 和 永久代 （方法区）物理上连续，逻辑上分离， 
    - jdk1.8之后，方法区的实现为： 元空间 （不是在jvm内存中，而是在本地内存(Native memory)）
    - 垃圾定位： 引用计数， 根可达法 GCRoot ()，直接引用，间接引用
    - GC Algorithms 垃圾回收算法, JVM 分代回收策略
        - 标记清除 Mark-Sweep， 根可达法， 产生空间碎片
        - 标记压缩 Mark-Compact， old GC 又称Full GC
        - 复制算法， 运行高效；不足之处是占用内存多， young GC ，
    - 对象分配的过程： 能够放入栈， 是否大对象 ， 能否 线程本地分配(Thread Local Allocation Buffer)
        - 栈上分配
        - 线程本地分配
        - 老年代
    - GC 回收器， Stop-The-World”状态
        - young GC    Full GC
        - serial (复制算法)<==>serial old  采用了标记 - 整理（Mark-Compact）算法
        - ParNew （Serial GC 的多线程版本）<==> CMS, 基于标记 - 清除（Mark-Sweep）算法, 
        - Parallel Scavenge  <==> Parallel Old   并行运行；作用于老年代；标记-整理算法；吞吐量优先  
        - G1 垃圾回收器， 内部是类似棋盘状的一个个 region 组成。
        
    - jvm 调优工具 
        - jps主要用来输出JVM中运行的进程状态信息
        - jstat  持续观察虚拟机内存中各个分区的使用率以及GC的统计数据
        - jmap 查看堆内存的使用详情
        - jstack 看Java进程内的线程堆栈信息
        - 内存查看工具 ，JConsole 和 Java VisualVM 
    
11. 锁
    - 死锁是指多个进程在执行的过程中，因为竞争资源而造成互相等待的现象，若无外力作用，它们都无法推进下去。
    - 避免死锁
        - 尽量使用trylock的方法， 设置超时时间，主动退出
    -  死锁产生必须满足的4个必要条件
        - 互斥条件， 互斥使用： 资源被一个线程使用时，别的线程不可使用
        - 请求和保持条件， 占有且等待： 资源请求者在请求其他资源时，保持对原有资源的占有
        - 不剥夺条件， 不可抢占： 资源请求者不能强制从资源占有者手里夺取资源
        - 环路等待条件， 循环等待： 形成环路
    
1. String, StringBuffer, StringBuilder
    - String final类型修饰， 不可边对象
    - StringBuffer, StringBuilder 都是在原有对象上操作
    - StringBuffer线程安全的可变字节。StringBuilder线程不安全
    - StringBuilder > StringBuffer > String
2. IOC容器的思路
    - 解析类，招到注解的类，Spring管理
    - 找到注解类的信息和属性的注解信息（反射），set赋值
3. IO流， 字节流，字符流， 缓冲区   
    - 四大基类 
        - InputStream
        - outputStream
        - Reader
        - Writer 
4.  Java反射
    - JAVA反射机制是在运行状态中，对于任意一个类，都能够知道这个类的所有属性和方法；对于任意一个对象，都能够调用它的任意一个方法；这种动态获取的信息以及动态调用对象的方法的功能称为java语言的反射机制
5. 动态代理
    - JDK 对有接口的
    - CGLIB  无接口的
    
           
1. 线程池thread pool executor
2. 垃圾回收，分带回收，GC算法
3. Java反射，泛型编程 
4. 序列化问题
5. ThreadLocal
6. 线程池处理字符串
7. 动态代理
8. classloader，
9. 异常与error，常见的异常
10. lock与synchronized
11. generator与iterator
12. hashMap concurrent hash map,是否允许null
13. collection
14. 网络模型七层模型
15. spring IOC
16. AOP   

      
## Mysql  
1. 数据库事务： 事务是一个不可分割的数据库操作序列，其执行的结果必须使数据库从一种一致性状态变到另一种一致性状态。事务是逻辑上的一组操作，要么都执行，要么都不执行。
2. 四大特性ACID
    - 原子性（基础）： 事务是最小的执行单位，不允许分割。事务的原子性确保动作要么全部完成，要么完全不起作用；
    - 一致性（约束条件）： 执行事务前后，数据保持一致，多个事务对同一个数据读取的结果是相同的；
    - 隔离性（手段）： 并发访问数据库时，一个用户的事务不被其他事务所干扰，各并发事务之间数据库是独立的；
    - 持久性（目的）： 一个事务被提交之后。它对数据库中数据的改变是持久的，即使数据库发生故障也不应该对其有任何影响。
3. 四个隔离级别：为了解决并发情况下数据安全性问题
    - read uncommitted: 读未提交， 脏读，不可重复读，幻读
    - read committed 读已提交
    - repeatable read：可重复读
    - serializable: 串行化

## 网络协议
应用层协议： HTTP
传输层协议： TCP， UDP
    - TCP 提供可靠传输协议，传输前建立连接，面向字节流，传输慢
        - 三次握手协议
        - 四次挥手
    - UDP 无法保证可靠传输，无需建立连接，以报文的方式传输，效率高
  
## ElasticSearch
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

- [24道进阶必备Elasticsearch 面试真题](https://zhuanlan.zhihu.com/p/102500311)
 1. elasticsearch 了解多少，说说你们公司 es 的集群架构，索引数据大小，分片有多少，以及一些调优手段     
    - 3个节点，保证了最基本的高可用， 
    - 分片设置了3， 索引数据量，每天只有几百，很少， 主要是给专家算法提供的
    - 一个index, 十来个字段
    - 设计阶段调优：
    - 写入调优： 
 2. 
    
    
    
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

## Redis 面试题
- [几率大的Redis面试题（含答案）](https://blog.csdn.net/Butterfly_resting/article/details/89668661)
1. redis支持的数据类型
    - String 字符串： set key value, get key 
        - 
    - Hash 哈希 ： hmset name  key1 value1 key2 value2    , hget key filed
        - HashMap
    - List列表：  lpush  name  value，   rpush  name  value, lrange key start end 
        - 双向链表， 增删快
    - Set 集合，sadd key member， smembers key 
        - 哈希表实现，元素不重复， 复杂度 O(1), 共同好友，好友推荐
    - Zset 有序集合 zadd key score member , zrangebyscore key start end
        - zset 和 set 一样也是string类型元素的集合,且不允许重复的成员。每个元素都会关联一个double类型的分数, 通过分数来为集合中的成员进行从小到大的排序
2. 什么是Redis持久化？Redis有哪几种持久化方式？优缺点是什么？    
    - 持久化就是把内存的数据写到磁盘中去，防止服务宕机了内存数据丢失。
    - 两种持久化方式:RDB（默认） 和AOF 
        - RDB (Redis DataBase)： rdbSave-> RDB文件， rdbLoad -> 文件加载内存 
        - AOF (Append-only file): 每次操作都会调用 flushAppendOnlyFile 函数 ，都会执行以下两个操作 （AOF 写入保存）
            - WRITE：根据条件，将 aof_buf 中的缓存写入到 AOF 文件
            - 根据条件，调用 fsync 或 fdatasync 函数，将 AOF 文件保存到磁盘中
    - 比较
        1、aof文件比rdb更新频率高，优先使用aof还原数据。
        2、aof比rdb更安全也更大
        3、rdb性能比aof好
        4、如果两个都配了优先加载AOF
3. redis 通信协议 RESP        
4. Redis 有哪些架构模式？讲讲各自的特点
    - 单机版， 优点： 简单， 缺点： 1、内存容量有限 2、处理能力有限 3、无法高可用。
    - 主从模式（master-slave）, 转移master读数据库的压力， 缺点： 无法保证高可用， 没有解决 master 写的压力
    - 哨兵模式（Redis sentinel）: 分布式系统中监控 redis 主从服务器，并在主服务器下线时自动进行故障转移
        - 监控（Monitoring）,不断地检查你的主服务器和从服务器是否运作正常
        - 提醒（Notification）, 当被监控的某个 Redis 服务器出现问题时， Sentinel 可以通过 API 向管理员或者其他应用程序发送通知。
        - 自动故障迁移（Automatic failover）, 当一个主服务器不能正常工作时， Sentinel 会开始一次自动故障迁移操作
        - 特点： 保证高可用， 监控各个节点， 自动故障迁移， 缺点： 主从模式，切换需要时间丢数据，没有解决 master 写的压力 
    - 集群（proxy 型）
        - 支持失败节点自动删除， 后端 Sharding 分片逻辑对业务透明，业务方的读写方式和操作单个 Redis 一致， 
        - 增加了新的 proxy，需要维护其高可用。
    - 集群（直连型）
        - 无中心架构（不存在哪个节点影响性能瓶颈），少了 proxy 层， 可扩展性， 高可用， 实现故障自动failover
        - 资源隔离性较差，容易出现相互影响的情况, 数据通过异步复制,不保证数据的强一致性
5.  使用过Redis分布式锁么，它是怎么实现的？
           
6. 缓存穿透问题， 如何避免， 什么事缓存雪崩， 如何避免
    - 缓存穿透： 一般的缓存系统，都是按照key去缓存查询，如果不存在对应的value，就应该去后端系统查找（比如DB）。一些恶意的请求会故意查询不存在的key,请求量很大，就会对后端系统造成很大的压力。这就叫做缓存穿透。
    - 缓存穿透的避免： 
        -  布隆过滤器， 对一定不存在的key进行过滤。可以把所有的可能存在的key放到一个大的Bitmap中，查询时通过该bitmap过滤。  
        - 对空结果也进行缓存， 时间设置短一点即可
    - 缓存雪崩： 当缓存服务器重启或者大量缓存集中在某一个时间段失效，这样在失效的时候，会给后端系统带来很大压力。导致系统崩溃
        - 简单地办法，将缓存缓存失效时间分散开，不同的key，设置不同的过期时间，让缓存失效的时间点尽量均匀
        - 系统设计时，在缓存失效后，通过加锁或者队列来控制读数据库写缓存的线程数量。比如对某个key只允许一个线程查询数据和写缓存，其他线程等待
7. 单线程的redis为什么这么快
    - 纯内存操作
    - 单线程操作，避免了频繁的上下文切换
    - 采用了非阻塞I/O多路复用机制

## 算法题
1. 快速排序
2. 如何检查环形链表



## 面经
1. 03.31 百度ACG

2. 04.01 拥有网络

3. 04.06 MX Player
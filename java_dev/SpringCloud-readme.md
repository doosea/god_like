# SpringCloud 学习笔记
## 1. maven 父子项目
1. 父工程配置
    1. new project, maven,父工程name
    2. 字符编码， setting, editor file encoding
    3. 注解生效激活
    4. java 编译选择 1.8 
    5. file type 文件过滤
    6. 删掉父工程下的src, 只保留一个pom.xml
    7. 父工程的pom.xml packing 设置为
        - <packaging>pom</packaging>
    8. maven 中的 dependencyManagement 
        - 定义jar版本， 后面子项目需要jar包，还要子项目中引入
2. 微服务子模块的建立
    1. 建立module 
    2. 改pom
    3. 写yml
    4. 主启动    
    5. 业务类
    
    
## 2. Apollo 统一配置中心
1. Apollo支持4个维度管理Key-Value格式的配置：
    1. application (应用)
    2. environment (环境)
    3. cluster (集群)
    4. namespace (命名空间)   
2. Apollo目前支持以下环境：
    - DEV : 开发环境
    - FAT : 测试环境 ， 提测环境
    - UAT : 集成环境 ， 预生产环境
    - PRO : 生产环境 
   
##3. 服务注册与发现  
### 1.Zookeeper 
1. 开源的分布式协调框架
    - 强一致性， （锁机制）
    - 最终一致性 
2. CAP 原则
    - C Consistency 一致性，指的是强一致性 
    - A Availability 可用性 
    - P Partition tolerance 分区容错性
3. 事务4个特征，分别是原子性、一致性、隔离性和持久性，简称事务的ACID特性；
    - 原子性（atomicity)：一个事务要么全部提交成功，要么全部失败回滚，不能只执行其中的一部分操作，这就是事务的原子性
    - 一致性（consistency)： 　事务的执行不能破坏数据库数据的完整性和一致性，一个事务在执行之前和执行之后，数据库都必须处于一致性状态。
    - 隔离性（isolation）： 
    - 持久性（durability）
4. zookeeper 
    1. 三种角色
        - leader: 负责集群的写请求， 并发起投票， 超过半数的节点同意后才提交该请求
        - follower： 处理读请求， 响应结果， 选举leader过程中参与投票
        - observer： 没有投票能力的follower, 协助follower 处理读请求
    2. 两种模式
        - 恢复模式： 服务启动红着leader崩溃后， 选举leader, leader 选出后，与其机器数据同步，大多数server 完成和leader 同步后，恢复模式结束
        - 广播模式：  leader 和 多数的follower 进行了状态同步后，进入广播模式。 
    3. zxid 64 Long, 高32 表示一个纪元epoch, 低32表示事务标识 xid 
    4. 数据结构
        - Znode节点类型
            - 持久化目录节点 persistent
            - 临时目录节点 ephemeral
    5. zookeeper 使用 
        - 启动 cd /opt/zookeeper/bin
            - 服务端: ./zkServer.sh start 
            - 客户端： ./zkCli.sh
    6. 指令
        - 查看
            - ls ZNodePath
            - ls2 ZNodePath
            
        - 创建节点 ： create ZNodePath data
        - 获取节点的值： get ZNodePath 
        - 设置或更新节点的值: set ZNodePath newData        
        - 查看节点状态： stat ZNodePath 
        - 删除节点： delete ZNodePath
        - 递归删除： rmr ZNodePath
    7. watch 机制
        - ls -w ZNodePath : 监听路径的变化
        - get -w ZNodePath: 监听节点值的变化
    8. api 使用 
5. zookeeper 使用场景
    - 配置中心
    - 负载均衡
    - 命名服务
    - DNS 服务
    - 集群管理
    - 分布式锁
        - 数据库实现分布式锁
        - redis 实现分布式锁
        - zookeeper 实现分布式锁： 有序临时节点 + watch监听
            - 为每一个执行的线程都去创建一个有序的临时节点，为了确保有序性，在创建完节点，会在获取全部节点，再重新进行一次排序， 判断自己的临时节点序号是否是最小的，
                如果是最小，获得锁， 执行相关操作，释放锁
                如果不是最小的，会监听他的前一个节点， 前一个节点被删除的时候，获得锁。 
    - 分布式队列
    
### 2. Eureka
### 3. consul
## 4. 服务调用
### 1. ribbon: 负载均衡 LoadBalance
### 2. openfeign

   
##5. 服务降级 
### 1. Hystrix (停更)
1. 作用
    - 服务降级 fallback 
        - 程序运行异常
        - 超时
        - 服务熔断触发服务降级
        - 线程池，信号量打满也会导致服务降级
        
    - 服务熔断 break
        - 达到最大服务访问后，直接拒绝访问 
        - 
        
    - 服务限流 flowlimit
    - 接近实时的监控
### 2. resilience4j (国外用的多)
### 3. 


SpringCloud Alibaba
#java 基础
## 1. 多线程
1. 基本概念
    - 程序： 静态的代码
    - 进程： 程序的一次执行过程， 运行的程序， 有生命周期
    - 线程： 程序内部的一条执行路径
    - 单核CPU： 假的多线程， 一个时间单元内， 只能执行一个线程
    - 多核CPU： 更好发挥多线程的效率
    - java 程序至少三个线程： main 主线程，gc垃圾回收线程， 异常处理线程
    - 并行：多个CPU同时执行多个任务
    - 并发： 一个CPU，同时执行多个任务（采用时间片）， 比如秒杀
2. java 线程的创建四种方式
    1. 继承Thread类, 重写 run 方法, 创建Thread子类的对象, 调用start()
        - 调用 start(), 不是run()
        - 不可以再启动一个start的线程
    2. 实现Runnable接口， 实现run方法
       
    3. 实现Callable 接口
        
    -  比较 继承Thread 和 实现Runnable (推荐)
            - 单继承，多接口， 实现Runnable 没有单继承的局限性
            - 实现的方式更适合用来处理多个线程共享数据的情况       
        
    3. 实现Callable接口
    4. 线程池方式
    
3.  Thread 方法
        - run() 重写方法
        - start() 启动当前线程
        - currentThread():静态方法, 当前线程
        - getName() 
        - setName()
        - yield(): 释放当前cpu的执行权
        - join(): 线程a 中调用线程b的join(), 此时a阻塞, 直到b执行完之后, a 才结束阻塞状态
        - stop() 过时
        - sleep(long millionsec) : 阻塞指定时间
        - isAlive(): 判断当前线程是否还存活
4. 线程调度
    - 时间片策略
    - 抢占式： 优先级高的线程抢占CPU
    - Thread.getPriority()
    - Thread.setPriority()
        - Thread.MAX_PRIORITY     10 
        - Thread.NORMAL_PRIORITY  5 
        - Thread.MIN_PRIORITY     1
5. 线程的生命周期 
    - 新建: new Thread()
    - 就绪: 调用start()， sleep() 时间到， join()结束,获取同步锁,  notify() /notiyAll(), resume()
    - 运行: 获取CPU执行权
    - 阻塞: sleep， join, 等待同步锁， wait(), suspend() 挂起
    - 死亡: 执行完run, 或者调用stop， 或者异常没有处理
6. 线程安全问题
    - 同步代码块 synchronized(同步监视器， 俗称锁){ 同步代码 }
    - 同步方法： 所在方法上加上 synchronized        
        - 静态的同步方法，锁对象是当前类本身， .class
        - 非静态的同步方法， 锁对象是当前对象本身， this
    - Lock 方式       
## 2. 枚举类和注解

## 3. java 集合

## 4. 泛型

## 5. IO流

## 6. 网络编程

## 7. 反射

## 8. jdk 8 其他特性 jdk8+新特性

1. for(),forEach(),stream(),parallelSteam()效率对比
    ```java
        //for循环
        for (int i=0;i<stringList.size();i++){
            TestMethod();
        }
       
        //增强for循环
        for(String s:stringList){
            TestMethod();
        }
    
        //forEach循环
        stringList.forEach(s -> TestMethod());
    
        //Stream
        stringList.stream().forEach(s -> TestMethod());
    
        //parallelStream
        stringList.parallelStream().forEach(s -> TestMethod()); 
    ```

# Alibaba - java 规范
1. alibaba java coding guidelines 插件
2. 分层领域模型规约：POJO是DO/DTO/BO/VO的统称，禁止命名成xxxPOJO
    - DO（ Data Object）：与数据库表结构一一对应，通过DAO层向上传输数据源对象。
    - DTO（ Data Transfer Object）：数据传输对象，Service或Manager向外传输的对象。
    - BO（ Business Object）：业务对象。 由Service层输出的封装业务逻辑的对象。
    - AO（ Application Object）：应用对象。 在Web层与Service层之间抽象的复用对象模型，极为贴近展示层，复用度不高。
    - VO（ View Object）：显示层对象，通常是Web向模板渲染引擎层传输的对象。
    - POJO（ Plain Ordinary Java Object）：在本手册中， POJO专指只有setter/getter/toString的简单类，包括DO/DTO/BO/VO等。
    - Query：数据查询对象，各层接收上层的查询请求。 注意超过2个参数的查询封装，禁止使用Map类来传输。
 

# rdfa   
## 1. Apollo配置重心
0. 简介： Apollo（阿波罗）是携程框架部门研发的开源配置管理中心， 
    1. 四个维度管理Key-Value格式的配置
        - application (应用)
        - environment (环境)
        - cluster (集群)
        - namespace (命名空间)  
    2. 配置文件的多种加载方式
        - 程序内部hard code
        - 配置文件 application.properties / yml
        - 环境变量 ENV 
        - 启动参数 jar xxx.jar --jvm
        - 基于数据库 
1. 接入apollo
    0. 权限
        - 编辑权限： 只能修改，不能发布
        - 发布权限： 发布是否实时影响线上结果？
    1. rdfa 框架 接入appolo
        - 配置中心新建appId 同名项目，发布application命名空间， 选择关联其他公共命名空间
        - maven 引入依赖 `top.rdfa.framework ： rdfa-cfg-ucm2`
        - 在starter下，application.properties中加入
            ```properties
             # app.id 必须与配置中心项目AppId一致
             app.id = appid-dosea-demo
             apollo.bootstrap.enabled = true
            
             # 将需要加载的配置Namespace，按顺序列在此属性中
             apollo.bootstrap.namespaces = RDFA.db,RDFA.common,<其他配置命名空间...>,application
            ```
        - 使用到数据库的，需要把数据库的配置信息写在配置文件中
        
            
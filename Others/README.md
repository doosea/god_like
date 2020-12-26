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

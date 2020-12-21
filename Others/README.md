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
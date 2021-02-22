# python 操作

## 1. python 线程池
 - [ThreadPoolExecutor线程池](https://www.jianshu.com/p/b9b3d66aa0be)
 简单使用： 
    ```python 
    from concurrent.futures import ThreadPoolExecutor
    import time
    
    
    # 参数times用来模拟网络请求的时间
    def get_html(times):
        time.sleep(times)
        print("get page {}s finished".format(times))
        return times
    
    
    executor = ThreadPoolExecutor(max_workers=2)
    # 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
    task1 = executor.submit(get_html, 3)
    task2 = executor.submit(get_html, 2)
    # done方法用于判定某个任务是否完成
    print(task1.done())
    # cancel方法用于取消某个任务,该任务没有放入线程池中才能取消成功
    print(task2.cancel())
    time.sleep(4)
    print(task1.done())
    # result方法可以获取task的执行结果
    print(task1.result())
    ```
 - `ThreadPoolExecutor` 构造实例的时候，传入 `max_workers` 参数来设置线程池中最多能同时运行的线程数目。
 - 使用 `submit` 函数来提交线程需要执行的任务（函数名和参数）到线程池中，并返回该任务的句柄（类似于文件、画图），注意`submit()`不是阻塞的，而是立即返回。
 - 通过`submit`函数返回的任务句柄，能够使用`done()`方法判断该任务是否结束。上面的例子可以看出，由于任务有2s的延时，在task1提交后立刻判断，task1还未完成，而在延时4s之后判断，task1就完成了。
 - 使用`cancel()`方法可以取消提交的任务，如果任务已经在线程池中运行了，就取消不了。这个例子中，线程池的大小设置为2，任务已经在运行了，所以取消失败。如果改变线程池的大小为1，那么先提交的是task1，task2还在排队等候，这是时候就可以成功取消。
 - 使用`result()`方法可以获取任务的返回值。查看内部代码，发现这个方法是阻塞的。

## 2. python with 上下文
1. open 
    - 文件读取发生异常，但没有进行任何处理；
    - 可能忘记关闭文件句柄；
2. with
    0. 基本语法
        ```
        with context_expression [as target(s)]:
            with-body 
       
        with open("file_path") as f:
            f.read()
        ```
    1. 概念
        - 上下文管理协议(Context ManagementProtocol)： 包含方法enter() 和 exit(), 支持该协议的对象要实现这两种方法
        - 上下文管理器（context Manager）: 支持上下文管理协议的对象, 这种对象实现了 enter() 和 exit() 方法。 通常使用with 语句调用上下文管理器
        - 运行时上下文（runtime context）： 
        - 上下文表达式（Context Expression）：该表达式要返回一个上下文管理器对象。
        - 语句体（with-body): with 语句包裹起来的代码块，在执行语句体之前会调用上下文管理器的 enter() 方法，执行完语句体之后会执行 exit() 方法。
        - open 对象实现了上线问管理协议
    2. with 执行原理
        - 一旦获取的上下文对象，就会调用它的 enter() 方法，将完成 with语句 块执行前的所有准备功能工作。
        - 如果with 语句后面跟了 as 语句，则用 enter() 方法的返回值来赋值；
        - 当with语句块结束时，无论是正常结束，还是由于异常，都会调用上下文对象的__exit__()方法，exit()方法有3个参数，如果with语句正常结束，三个参数全部都是 None；如果发生异常，三个参数的值分别等于调用sys.exc_info()函数返回的三个值：类型（异常类）、值（异常实例）和跟踪记录（traceback），相应的跟踪记录对象
    
## 3. yield， 迭代器， 生成器
1. 迭代器
    - 迭代器协议：对象提供next()方法， 要么返回迭代中的下一项， 要么引起一个StopIteration异常，姨终止迭代
    - 可迭代对象： 实现了迭代器协议的对象
    - Python的内置工具(如for循环，sum，min，max函数等)使用迭代器协议访问对象
    
2. 生成器: 提供延迟操作， 需要的时候才产生, 减少内存使用，还能够提高代码可读性
    - Python有两种不同的方式提供生成器
        - 1. 生成器函数, 使用yield语句而不是return语句返回结果
        - 2. 生成器表达式, 类似于列表推导，但是，生成器返回按需产生结果的一个对象，而不是一次构建一个结果列表
            ```
              a = [x**2 for x in range(5)],  列表推导，将会一次产生所有结果：
              b = (x**2 for x in range(5)) , 将列表推导的中括号，替换成圆括号，就是一个生成器表达式：
            ```
    - 生成器只能遍历一次!
    
3. yield 
4. range: range 对象是可迭代的， 但是却不是迭代器。 迭代器只能使用一次，  range 对象被遍历而不「消耗」， 有长度，且可以被索引。
    
## 4. 装饰器

## 5. 进行、 线程、 协程
1. 多任务
2. 线程，进程 概念


## 6. 死锁
死锁是指多个进程在执行的过程中，因为竞争资源而造成互相等待的现象，若无外力作用，它们都无法推进下去。

1. 产生死锁的原因
    - 竞争资源
    - 进程间推进顺序非法

2. 死锁产生必须满足的4个必要条件
    - 互斥条件， 互斥使用： 资源被一个线程使用时，别的线程不可使用
    - 请求和保持条件， 占有且等待： 资源请求者在请求其他资源时，保持对原有资源的占有
    - 不剥夺条件， 不可抢占： 资源请求者不能强制从资源占有者手里夺取资源
    - 环路等待条件， 循环等待： 形成环路
3. 解决死锁的基本方法
    -  预防死锁：(破坏4个必要条件之1) 
        1. 资源一次性分配：一次性分配所有资源，这样就不会再有请求了：（破坏请求条件）
        2. 只要有一个资源得不到分配，也不给这个进程分配其他的资源：（破坏请保持条件）
        3. 可剥夺资源：即当某进程获得了部分资源，但得不到其它资源，则释放已占有的资源（破坏不可剥夺条件）
        4. 资源有序分配法：系统给每类资源赋予一个编号，每一个进程按编号递增的顺序请求资源，释放则相反（破坏环路等待条件）
"""
子线程创建步骤：
    1. 导入模块 threading
    2. 使用threading.Thread() 创建线程对象

    3. 使用子线程执行分支
    4. 启动子线程  线程对象.start()

线程数量：threading.enumerate()
当前线程：threading.current_thread()

线程参数：
    1. 使用元组传参 args=()
        - thread_sing = Thread(target=sing, name="sing", args=(1,2,3))
    2. 通过字典传参：
        - thread_sing = Thread(target=sing, name="sing", kwargs={"a":1, "b":2, "c":3})
    3. 混合使用， args, kwargs
        -  thread_sing = Thread(target=sing, name="sing", args=(1, ), kwargs={"b": 2, "c": 3})

线程的执行顺序
    - 执行顺序是无序的，由CPU调度

守护线程
    - 当所有的非守护线程结束时，程序也就终止了，同时会杀死进程中的所有守护线程。反过来说，只要任何非守护线程还在运行，程序就不会终止。
       thread_sing.setDaemon(True)
    - 必须在线程运行前确认是否为守护线程
        thread_rap.setDaemon(True)
        thread_rap.start()
    - 守护线程创建的新线程也是守护线程


"""

from threading import Thread
import threading
import time


def sing(a, b, c):
    print(a, b, c)
    for _ in range(5):
        print("唱", threading.current_thread())
        time.sleep(1)


def jump():
    for i in range(5):
        print("跳")
        time.sleep(1)


def rap():
    for i in range(5):
        print("rap")
        time.sleep(1)


if __name__ == '__main__':

    # 创建子线程
    # thread_sing = Thread(target=sing, name="sing", args=(1, 2, 3))
    # thread_sing = Thread(target=sing, name="sing", kwargs={"a": 1, "b": 2, "c": 3})
    thread_sing = Thread(target=sing, name="sing", args=(1, ), kwargs={"b": 2, "c": 3})
    thread_jump = Thread(target=jump)
    thread_rap = Thread(target=rap)

    # 设置子线程守护
    thread_sing.setDaemon(True)
    thread_jump.setDaemon(True)
    thread_rap.setDaemon(True)

    thread_sing.start()
    thread_jump.start()
    thread_rap.start()

    # for i in range(5):
    #     # 查看线程数量
    #     print(threading.enumerate())
    #     time.sleep(1)

    # 查看线程数量
    time.sleep(2)
    print(threading.enumerate())
    exit()

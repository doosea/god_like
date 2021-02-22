"""
子线程创建步骤：
    1. 导入模块 threading
    2. 使用threading.Thread() 创建线程对象
    3. 使用子线程执行分支
    4. 启动子线程  线程对象.start()

    线程数量：threading.enumerate()
    当前线程：threading.current_thread()
"""

from threading import Thread
import threading
import time


def sing():
    for i in range(5):
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

    # 查看线程数量
    print(threading.enumerate())


    # 创建子线程
    thread_sing = Thread(target=sing, name="sing")
    thread_jump = Thread(target=jump)
    thread_rap = Thread(target=rap)

    thread_sing.start()
    thread_jump.start()
    thread_rap.start()

    for i in range(5):
        # 查看线程数量
        print(threading.enumerate())
        time.sleep(1)

    # 查看线程数量
    time.sleep(1)
    print(threading.enumerate())

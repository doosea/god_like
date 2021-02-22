from contextlib import contextmanager


class MyFile(object):
    def __init__(self, file_name, file_mode):
        self.file_name = file_name
        self.file_mode = file_mode

    def __enter__(self):
        """ 上文打开对象，并返回文件资源"""
        print("进入上文")
        self.file = open(file=self.file_name, mode=self.file_mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("进入下文")
        print(exc_type)
        print(exc_val)
        print(exc_tb)
        """下文关闭文件句柄 ， 处理异常 """
        self.file.close()


@contextmanager
def myopen(file_name, file_mode):
    # 1. 上文，打开资源
    print("进入上文")
    file = open(file=file_name, mode=file_mode)
    #
    yield file

    # 下文 关闭资源
    print("进入下文")
    file.close()


if __name__ == '__main__':
    # 1. 通过class 方式，实现上下文管理器， 进行with操作
    with MyFile("./README.md", "r") as f:
        f.read()

    # 2. 通过contextmanager 装饰器， 装饰myOpen方法， 实现上下文管理
    with myopen("./README.md", "r") as f:
        print(f.read())

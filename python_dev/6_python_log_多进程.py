'''
 java 格式：
    - [%d{yyyy-MM-dd HH:mm:ss.SSS}] [%level] [%thread] %logger{36} %L - %msg%xEx%n
        %c{参数} 或 %logger{参数}  ##输出日志名称
        %L - java源码行数
        %m 或 %msg 或 %message ##输出错误信息
        %xEx 错误调用栈
        %n - 换行


对应的python 格式
    - '[%(asctime)s] [%(levelname)s] [%(threadName)s] %(name)-36s  %(lineno)d %(message)s'
        %(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
        %(levelname)s 文本形式的日志级别
        %(threadName)s 线程名。可能没有
        %(name)s Logger的名字
        %(lineno)d 调用日志输出函数的语句所在的代码行
        %(message)s用户输出的消息

    - 所有的配置
        %(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
        %(name)s Logger的名字
        %(levelno)s 数字形式的日志级别
        %(levelname)s 文本形式的日志级别
        %(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
        %(filename)s 调用日志输出函数的模块的文件名
        %(module)s 调用日志输出函数的模块名
        %(funcName)s 调用日志输出函数的函数名
        %(lineno)d 调用日志输出函数的语句所在的代码行
        %(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
        %(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
        %(thread)d 线程ID。可能没有
        %(threadName)s 线程名。可能没有
        %(process)d 进程ID。可能没有
        %(message)s用户输出的消息
'''

import os
import re
import sys
import time
import logging
import logging.handlers
import socket
from concurrent_log import ConcurrentTimedRotatingFileHandler

APP_ID = os.environ.get('APP_ID', '-undefinedappid')
HOST_NAME = socket.gethostname()
LOG_FILE_PATH = '/data/logs/' + APP_ID + os.sep + HOST_NAME


class GetLogger:

    def __init__(self, logs_dir=None, logs_level=logging.INFO):
        self.logs_dir = logs_dir  # 日志路径
        self.log_name = r'app.log'  # 日志名称
        self.logs_level = logs_level  # 日志级别
        # 日志的输出格式
        self.log_formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(threadName)s] %(name)-36s  %(lineno)d %(message)s')

        if logs_dir is None:
            self.logs_dir = LOG_FILE_PATH  # 设置日志保存路径

        # 如果logs文件夹不存在，则创建
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回"""
        # 实例化root日志对象
        log_logger = logging.getLogger('logger')

        # 设置日志的输出级别
        log_logger.setLevel(self.logs_level)
        if not log_logger.handlers:  # 避免重复日志
            # 创建一个handler，用于输出到cmd窗口控制台
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)  # 设置日志级别
            console_handler.setFormatter(self.log_formatter)  # 设置日志格式
            log_logger.addHandler(console_handler)

            # 建立一个循环文件handler来把日志记录在文件里
            file_handler = ConcurrentTimedRotatingFileHandler(
                filename=self.logs_dir + os.sep + self.log_name,  # 定义日志的存储
                when="s",  # 按照日期进行切分when = D： 表示按天进行切分,or self.when == 'MIDNIGHT'
                interval=10,  # interval = 1： 每天都切分。 比如interval = 2就表示两天切分一下。
                backupCount=24,  # 最多存放日志的数量
                encoding="UTF-8",  # 使用UTF - 8的编码来写日志
                delay=False,
                utc=False  # 使用UTC + 0的时间来记录 （一般docker镜像默认也是UTC + 0）
            )
            file_handler.suffix = "%Y-%m-%d.log"
            # # need to change the extMatch variable to match the suffix for it
            file_handler.extMatch = re.compile(r"^\d{8}$")
            file_handler.setLevel(logging.DEBUG)  # 设置日志级别
            file_handler.setFormatter(self.log_formatter)  # 设置日志格式
            file_handler.doRollover()
            log_logger.addHandler(file_handler)

        return log_logger


logger = GetLogger().get_logger()

if __name__ == "__main__":
    # 对上面代码进行测试
    logger = GetLogger().get_logger()

    # 在具体需要的地方
    logger.info('INFO日志打印...')
    logger.error('ERROR日志打印...')

    # # 打印日志保存路径
    # sep = os.sep
    # set_log_path = os.path.abspath(
    #     os.path.join(__file__, f"..{sep}..{sep}logs{sep}"))
    # print('测试Log路径：', set_log_path)

    import time

    while True:
        logger.info('每隔X打印一下')
        time.sleep(2)

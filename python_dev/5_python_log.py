import logging
import sys
import time
import logging.handlers
import os

logger = logging.getLogger("myLogger")
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(threadName)s] %(name)-36s  %(lineno)d %(message)s')

handler_console = logging.StreamHandler(sys.stdout)
handler_console.setLevel(logging.DEBUG)
handler_console.setFormatter(formatter)

# file handler
handler_file = logging.FileHandler(filename='handler_file.log')
handler_file.setLevel(logging.DEBUG)
handler_file.setFormatter(formatter)

# 按日志大小滚动
RotatingFileHandler_file = logging.handlers.RotatingFileHandler(filename='RotatingFileHandler_file.log', mode='a',
                                                                maxBytes=1000, backupCount=2)
'''
maxBytes：控制单个日志文件的大小，单位是字节，也就是当单个文件大小超过这个数值时，就创建一个新的文件。
backupCount：用于控制日志文件的数量，如果创建的日志文件数量多于这个数值，就删除最老的。
'''
RotatingFileHandler_file.setLevel(logging.DEBUG)
RotatingFileHandler_file.setFormatter(formatter)

# 按时间滚动
TimedRotatingFileHandler_file = logging.handlers.TimedRotatingFileHandler(filename='TimedRotatingFileHandler_file.log',
                                                                          when='S', interval=15,
                                                                          backupCount=3, encoding='utf-8')
TimedRotatingFileHandler_file.setLevel(logging.DEBUG)
TimedRotatingFileHandler_file.setFormatter(formatter)

logger.addHandler(handler_console)
logger.addHandler(handler_file)
logger.addHandler(RotatingFileHandler_file)
logger.addHandler(TimedRotatingFileHandler_file)
logger.setLevel(logging.DEBUG)  # 这里决定日志记录的最低level
'''
两个setLevel()方法
    - logger.setLevel: 记录器的级别决定了消息是否要传递给处理器。
    - handler.setLevel: 每个处理器的级别决定了消息是否要分发。
'''
for i in range(1000):
    logger.info("zzzz")
    time.sleep(1)

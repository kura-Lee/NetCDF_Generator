'''
Author: zhongxiaowei kura_Lee@163.com
Date: 2024-01-12 20:50:33
LastEditTime: 2024-10-02 22:43:36
FilePath: /Dataset_build/log/__init__.py
Description: 

Copyright (c) 2024 by Zhongxiaowei, All Rights Reserved. 
'''

import os
import sys
import time
import logging
import logging.handlers


class Tee(object):
    """一个同步重定向stdout和stderr输出到指定文件中的类

    Args:
        object (_type_): _description_
    """
    def __init__(self, name, mode='w'):
        self.file = open(name + f"_{time.strftime('%F_%H:%M:%S')}.log", mode)
        self.stdout = sys.stdout
        sys.stdout = self
        self.stderr = sys.stderr
        sys.stderr = self

    def __del__(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        self.file.close()

    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)

    def flush(self):
        self.file.flush()


class FormatterNormal(logging.Formatter):
    def __init__(self, fmt: str = "%(asctime)s %(name)s-[%(levelname)s]:%(message)s",
                 datefmt: str = '%Y-%m-%d %H:%M:%S'):
        super().__init__(fmt, datefmt)


def setup_default_logging(default_level: int = logging.INFO, log_path: str = '', formatter: logging.Formatter = FormatterNormal()):
    """配置root日志记录器

    Args:
        default_level (_type_, optional):       日志器的记录级别. Defaults to logging.INFO.
        log_path (str, optional):               文件日志器的位置, 默认不记录.
        formatter (logging.Formatter, optional):日志输出格式设置, 默认为FormatterNormal的实例
    """
    # 清除原有的handler
    if logging.root.hasHandlers():
        for handler in logging.root.handlers:
            logging.root.removeHandler(handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logging.root.addHandler(console_handler)
    logging.root.setLevel(default_level)
    if log_path:
        file_handler = logging.handlers.RotatingFileHandler(
            log_path, maxBytes=(1024 ** 2 * 2), backupCount=3)
        file_handler.setFormatter(formatter)
        logging.root.addHandler(file_handler)


def get_default_logger(name, log_path=''):
    """获取一个日志器

    Args:
        name (_type_): 日志器的名称
        log_path (str, optional): 日志器的路径. Defaults to ''.
    """
    setup_default_logging(log_path=log_path)
    return logging.getLogger(name)

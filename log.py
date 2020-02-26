#!D:\Program Files (x86)\Python38-32\python.exe
# -*- coding: UTF-8 -*-

' logger module '

__author__ = 'scutxd'

import logging

import os
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
)
LOG_FILE_PATH = os.path.dirname(__file__) + '/log/'
LOG_FILE_NAME = 'log.log'
LOG_FILE = LOG_FILE_PATH + LOG_FILE_NAME

console_handler = logging.StreamHandler()  # 输出到控制台的handler
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)  # 设置控制台日志级别为ERROR

file_handler = logging.FileHandler(LOG_FILE)  # 输出到文件的handler
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)  # 设置文件日志级别为DEBUG

logging.basicConfig(level=logging.INFO,
                    handlers=[console_handler, file_handler])
logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)

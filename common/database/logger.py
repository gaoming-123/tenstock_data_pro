# -*- coding: UTF-8 -*-
# date:
# editor: gmj
import logging


class MyLog(object):
    def __init__(self, name, log_path):
        # 返回用户的登录名
        # self.user = getpass.getuser()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        ####  日志文件名
        self.logFile = log_path
        self.formatter = logging.Formatter('%(asctime)s -%(name)s -%(levelname)s -%(message)s')

        ####  日志显示到屏幕上并输出到日志文件内
        self.logHand = logging.FileHandler(self.logFile, encoding='utf8')
        # 为logHand以formatter设置格式
        self.logHand.setFormatter(self.formatter)
        # 只有错误才被记录到logfile中
        # self.logHand.setLevel(logging.DEBUG)

        # 返回StreamHandler类的实例，如果stream被确定，使用该stream作为日志输出，反之，使用
        # self.logHandSt = logging.StreamHandler()
        # 为logHandSt以formatter设置格式
        # self.logHandSt.setFormatter(self.formatter)
        # self.logHandSt.setLevel(logging.DEBUG)

        # 添加特定的handler logHand到日志文件logger中
        self.logger.addHandler(self.logHand)
        # 添加特定的handler logHandSt到日志文件logger中
        # self.logger.addHandler(self.logHandSt)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


logger = MyLog('default', f'./default_db.log')

if __name__ == '__main__':
    mylog = MyLog('test', './test.txt')
    mylog.info("I'm info")
    mylog.warning("I'm warn")
    mylog.error(u"I'm error 测试中文")
    mylog.critical("I'm critical")

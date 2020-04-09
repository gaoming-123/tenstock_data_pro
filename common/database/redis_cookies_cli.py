# -*- coding: UTF-8 -*-
# Date   : 2020/1/17 9:39
# Editor : gmj
# Desc   :
import time
from redis import StrictRedis
from .logger import logger

# redis配置
REDIS_COOKIE_CONFIG = {
    'HOST': '106.13.63.136',
    'PORT': 6379,
    'PWD': 'gmj760808',
    'DB': 5,
}


class CookieRedisClient(object):
    def __init__(self, my_config=REDIS_COOKIE_CONFIG):
        self.config = my_config
        self.cli = self.connect()
        self.set_key = ''

    def connect(self):
        return StrictRedis(host=self.config['HOST'],
                           port=self.config['PORT'],
                           db=self.config['DB'], )

    def clear(self):
        for e in self.cli.keys():
            self.cli.delete(e)

    def read(self, key):
        return [i.decode() for i in self.cli.lrange(key, 0, -1)]

    def add(self, key, index, value):
        self.cli.lset(key, index, value)

    def getKeys(self):
        return [i.decode() for i in self.cli.keys()]

    def add_account(self, key, values):
        self.cli.rpush(key, *values)

    def set_pwd(self, key, value):
        self.cli.lset(key, 0, value)

    def set_total(self, key, value: int):
        org = self.cli.lrange(key, 2, 2)[0]
        self.cli.lset(key, 2, int(org) + value)
        num = self.cli.lrange(key, 1, 1)[0]
        if value < int(num) / 2:
            self.set_status(key, f'封号状态{int(time.time())}')

    def set_cookie_key(self, key, value):
        self.cli.lset(key, 3, value)

    def set_cookie(self, key, value):
        self.cli.lset(key, 4, value)

    def delete(self, key):
        self.cli.delete(key)

    def set_status(self, key, value):
        self.cli.lset(key, 5, value)

    def check(self):
        for key in self.getKeys():
            data = self.read(key)
            total = int(data[2])
            if (total > 90 and total < 120) or (total > 450 and total < 520):
                try:
                    self.delete(key)
                    logger.info(f'账户{key}今天请求次数:{total}次')
                except:
                    pass


if __name__ == '__main__':
    redis_cli = CookieRedisClient()
    ss = redis_cli.getKeys()
    for s in ss:
        redis_cli.set_status(s, '正常')
    #     if s not in phones:
    #         ll=redis_cli.read(s)
    #         print(ll)

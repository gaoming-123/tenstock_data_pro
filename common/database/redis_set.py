# -*- coding: UTF-8 -*-
# Date   : 2020/1/17 9:39
# Editor : gmj
# Desc   :
import hashlib
from redis import StrictRedis
from .db_config import REDIS_CONFIG


class RedisClient(object):
    def __init__(self, my_config=REDIS_CONFIG):
        self.config = my_config
        self.set_key = self.config['SET_KEY']
        self.cli = self.connect()

    def connect(self):
        return StrictRedis(host=self.config['HOST'],
                           port=self.config['PORT'],
                           # pwd=self.config.get('PWD'),
                           db=self.config['DB'],
                           )

    def change_key(self, key):
        self.set_key = key

    def add(self, value):
        self.cli.sadd(self.set_key, value)

    def exist(self, value):
        return self.cli.sismember(self.set_key, value)

    def existence(self, value):
        # 校验是否存在这个值
        result = self.exist(value)
        if not result:
            self.add(value)
        return result

    def hash_md5(self, txt):
        m = hashlib.md5()
        m.update(txt.encode('utf-8'))
        return m.hexdigest()

    def delete(self, value):
        self.cli.smove(self.set_key, 'delete_member', value)


redis_client = RedisClient()

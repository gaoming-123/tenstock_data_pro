# -*- coding: UTF-8 -*-
# Date   : 2020/1/17 9:38
# Editor : gmj
# Desc   :
import pymysql
from .db_config import BD_MYSQL_CONFIG
from .logger import logger


class MysqlConnect(object):
    def __init__(self, my_config=BD_MYSQL_CONFIG):
        self.config = my_config
        self.cnn = self.connect()
        self.cursor = self.cnn.cursor()
        self.logger = logger
        self.set_default_cursor()

    def connect(self):
        return pymysql.connect(
            host=self.config['HOST'],
            port=self.config['PORT'],
            user=self.config['USER'],
            password=self.config['PWD'],
            db=self.config['DB'],
            charset='utf8',
        )

    def set_logger(self, my_logger):
        self.logger = my_logger

    def update(self, sql):
        self.execute(sql)
        self.commit()

    def set_default_cursor(self):
        self.cursor = self.cnn.cursor(pymysql.cursors.DictCursor)

    def set_cursor(self, cursor):
        self.cursor = self.cnn.cursor(cursor=cursor)

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.logger.error(e)
            self.logger.error(sql)
            raise Exception('数据保存失败，请检查sql')

    def fetchall(self, sql, params=None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def query_number_result(self, theme, sql):
        self.cursor.execute(sql)
        res = self.cursor.fetchall()[0]
        self.logger.info(f'{theme} : {res["count(*)"]} 条')

    def executemany(self, save_sql, save_data):
        self.cursor.executemany(save_sql, save_data)

    def rollback(self):
        self.cnn.rollback()
        self.cnn.commit()

    def save_many(self, save_sql, save_data):
        try:
            self.cursor.executemany(save_sql, save_data)
            self.cnn.commit()
        except Exception as ee:
            self.logger.error(f'保存出错：{save_data}')
            self.logger.error(ee)
            self.cnn.commit()

    def commit(self):
        self.cnn.commit()

    def close(self):
        self.commit()
        self.cursor.close()
        self.cnn.close()

    def bakeUp(self, table_name, version):
        sql = f'create table {table_name}_{version} as SELECT * from {table_name} where is_deal=0'
        self.execute(sql)

    def count(self, sql_txt):
        try:
            return self.fetchall(sql_txt)[0]['count(*)']
        except:
            raise Exception('sql中需要使用count(*),用于统计数量')

    def getSchemaTab(self, table):
        sql = f"select COLUMN_NAME,COLUMN_COMMENT from information_schema.COLUMNS where TABLE_SCHEMA = (select database()) and TABLE_NAME='{table}'"
        return self.fetchall(sql)

    def get_save_sql(self, destination_tables, destination_table):
        des_table = destination_tables[destination_table]
        save_sql = 'insert into ' + destination_table + f'(`{"`,`".join(des_table.keys())}`) ' + f' values({",".join(["%s"] * len(des_table.keys()))})'
        return save_sql

    def create_sql(self, destination_table, data: dict):
        save_sql = ' insert into ' + destination_table + f'(`{"`,`".join(data.keys())}`) ' + f' values({",".join(["%s"] * len(data.keys()))})'
        return save_sql

    def create_insert_sql_include_data(self, destination_table, data: dict):
        save_sql = 'insert into ' + destination_table + f'(`{"`,`".join(data.keys())}`)  values (' + ','.join(
            ["%s"] * len(data.keys())) + ")"
        return save_sql % tuple(data.values())

    def get_update_sql(self, table_name, data: dict, conditions: dict, double=False):
        if double:
            part1 = ' , '.join([f'`{k}`="%s"' for k in data.keys()])
            part2 = ' and '.join([f'`{k}`="%s"' for k in conditions.keys()])
        else:
            part1 = ' , '.join([f'`{k}`=\'%s\'' for k in data.keys()])
            part2 = ' and '.join([f'`{k}`=\'%s\'' for k in conditions.keys()])
        sql = f'update {table_name} set {part1} where {part2}'
        return sql % tuple(list(data.values()) + list(conditions.values()))

    def update_data(self, table_name, data: dict, conditions: dict, double=False):
        sql = self.get_update_sql(table_name, data, conditions, double=double)
        self.update(sql)

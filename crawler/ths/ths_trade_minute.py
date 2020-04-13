# -*- coding:utf-8 -*-
# editor: gmj
# Date: 2020-04-12 21:19
# desc:

import time

header = {
    'Referer': 'http://stockpage.10jqka.com.cn/HQ_v4.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}
import requests
import json
import re
from random import random
from common.crawl_utils.simple import get_by_proxy
from common.database.mysql import MysqlConnect
from common.database.db_config import BD_MYSQL_CONFIG
from common.database.redis_set import RedisClient

bd_cnn = MysqlConnect(BD_MYSQL_CONFIG)
redis_cli = RedisClient()


def request_all_stocks_minutes_data():
    stocks = bd_cnn.fetchall('select symbol from stocks_a_stocks')
    redis_cli.change_key('a_stocks_minutes_trade')
    number = 0
    while len(stocks) != number:
        for stock in stocks:
            symbol = stock['symbol']
            hash_txt = redis_cli.hash_md5(symbol)
            if redis_cli.exist(hash_txt):
                continue
            try:
                res = request_trade_day_minute(symbol)
                bd_cnn.save_many(
                    f'insert into stocks_minutetrade(trade_time,close,money,average,amount,symbol) values (%s,%s,%s,%s,%s,%s)',
                    res)
                redis_cli.add(hash_txt)
                time.sleep(5 * random())
            except:
                pass
        number = redis_cli.count()


def request_trade_day_minute(symbol):
    """
    请求个股每日的分钟级别数据
    :param code: 示例 'hs_000021' hs_6位代码
    :return:  列表[(分钟，收盘价，成交额，均价，成交量),] 例如: ('202004030930', '7.77', '5436669', '7.770', '699700')
    """
    code = f'hs_{symbol}'
    # url = f'http://d.10jqka.com.cn/v6/time/{code}/last.js'
    url = f'http://d.10jqka.com.cn/v6/time/{code}/defer/last.js'
    res = get_by_proxy(url, headers=header)
    # print(res.text)
    trade_data = re.findall('({.*})', res.text)[0]
    trade_data = json.loads(trade_data)
    trade_day = trade_data[code]['date']
    trade_data = trade_data[code]['data']
    minutes = trade_data.split(';')
    result = []
    for line in minutes:
        line_data = line.split(',')
        line_data[0] = trade_day + line_data[0]
        line_data.append(symbol)
        # 分钟，收盘价，成交额，均价，成交量
        result.append(tuple(line_data))
    return result


if __name__ == '__main__':
    request_all_stocks_minutes_data()
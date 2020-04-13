# -*- coding:utf-8 -*-
# editor: gmj
# Date: 2020-04-08 23:01
# desc: 从东方财富网更新融资融券数据全量更新，应该是日更新
import re
import time
from common.crawl_utils.simple import get_url, get_json
from crawler import bd_mysql_cnn

# 从东方财富网获取个股融资融券数据
def get_rongzirongquan_from_dfcf(code, stock_id, last_date):
    """从东方财富网获取个股融资融券数据 并解析"""
    # data = {
    #     "date": '日期',
    #     "scode": "601166",  # code
    #     "spj": '收盘价',  #
    #     "market": "融资融券_沪证",
    #     "secname": "兴业银行",  # 名称
    #     "zdf": '涨跌幅%',  #
    #
    #     "rzmre": '融资买入额(亿)',
    #     "rzche": '融资偿还额(亿)',
    #     "rzjme": '融资净买入(亿)',
    #     "rzye": '融资余额(亿)',
    #
    #     "rqmcl": '融券卖出量(股)',
    #     "rqchl": '融券偿还量(股)',
    #     "rqjmg": '融券净卖(股)',
    #     "rqyl": '融券余量(股)',
    #     "rqye": '融券余额(元)',
    #
    #     "rzrqye": '融资融券余额(亿)',
    #     "rzyezb": '余额占流通市值比%',
    #     "rzrqyecz": '融资融券余额差值(亿)',
    #
    #     # "sz": 345228341928.120000,  #
    #     # "kcb": 0,
    #     "rqmcl3d": '融券卖出量3d',
    #     "rzmre3d": '融资买入额3d',
    #     "rqjmg3d": '融券净卖股3d',
    #     "rqchl3d": '融券偿还量3d',
    #     "rzche3d": '融资偿还额3d',
    #     "rzjme3d": '融资净买额3d',
    #     "rchange3dcp": '3日涨跌幅',
    #
    #     "rzmre5d": '融资买入额5d',
    #     "rqmcl5d": '融券卖出量5d',
    #     "rqjmg5d": '融券净卖股5d',
    #     "rqchl5d": '融券偿还量5d',
    #     "rzjme5d": '融资净买额5d',
    #     "rzche5d": '融资偿还额5d',
    #     "rchange5dcp": '5日涨跌幅',
    #
    #     "rqjmg10d": '融券净卖股10d',
    #     "rzche10d": '融券偿还量10d',
    #     "rqchl10d": '融券偿还量10d',
    #     "rqmcl10d": '融券偿还量10d',
    #     "rzjme10d": '融资净买额10d',
    #     "rzmre10d": '融资买入额10d',
    #     "rchange10dcp": '10日涨跌幅',
    #
    # }
    # todo 请求接口已更新 返回结果需要正则提取 并lower函数处理
    url = f'http://datacenter.eastmoney.com/api/data/get?type=RPTA_WEB_RZRQ_GGMX&sty=ALL&source=WEB&p=1&ps=50&st=date&sr=-1&var=uBrzlcAb&filter=(scode="{code}")'
    # url = f'http://api.dataide.eastmoney.com/data/get_rzrq_ggmx?code={code}&orderby=date&order=desc&pageindex=1&pagesize=50'
    # res = get_url(url)
    res_new = get_url(url)
    json_text = re.findall("uBrzlcAb=(\{.*\})", res_new.text)[0]
    data_json = get_json(json_text.lower())['result']
    # data_json = get_json(res.text)
    if not data_json:
        # print(f'{code} 融资融券无数据')
        return
    max_page = data_json['pages']
    # page = data_json['pageindex']
    page = 1
    res_data = data_json['data']
    while (not last_date) and (page < max_page):
        url = url.replace(f'pageindex={page}', f'pageindex={page+1}')
        url = url.replace(f'p={page}', f'p={page+1}')
        res = get_url(url)
        json_text = re.findall("uBrzlcAb=(\{.*\})", res.text)[0]
        data_json = get_json(json_text.lower())['result']
        # print(data_json['data'][0])
        res_data.extend(data_json['data'])
        # print(f'get page {page}  success')
        page += 1
        time.sleep(0.3)
    last_res_data = []
    for one_d in res_data:
        res_one = {}
        res_one['trade_date'] = one_d['date'].split(' ')[0]
        # res_one['s_code'] = stock_id
        try:
            res_one['spj'] = round(one_d['spj'], 2)
        except:
            res_one['spj'] = 0
            # res_one['secname'] = one_d['secname']
        try:
            res_one['zdf'] = round(one_d['zdf'], 2)
        except:
            res_one['zdf'] = 0
        try:
            res_one['rzyezb'] = round(one_d['rzyezb'], 2)
        except:
            res_one['rzyezb'] = 0
        try:
            res_one['rzmre'] = round(one_d['rzmre'] / 100000000, 4)
        except:
            res_one['rzmre'] = 0
        try:
            res_one['rzche'] = round(one_d['rzche'] / 100000000, 4)
        except:
            res_one['rzche'] = 0
        try:
            res_one['rzjme'] = round(one_d['rzjme'] / 100000000, 4)
        except:
            res_one['rzjme'] = 0
        try:
            res_one['rzye'] = round(one_d['rzye'] / 100000000, 4)
        except:
            res_one['rzye'] = 0
        try:
            res_one['rzrqye'] = round(one_d['rzrqye'] / 100000000, 4)
        except:
            res_one['rzrqye'] = 0
        try:
            res_one['rzrqyecz'] = round(one_d['rzrqyecz'] / 100000000, 4)
        except:
            res_one['rzrqyecz'] = 0
        try:
            res_one['rqye'] = round(one_d['rqye'] / 100000000, 4)
        except:
            res_one['rqye'] = 0
        res_one['rqmcl'] = one_d['rqmcl'] if one_d['rqmcl'] else 0
        res_one['rqchl'] = one_d['rqchl'] if one_d['rqchl'] else 0
        res_one['rqjmg'] = one_d['rqjmg'] if one_d['rqjmg'] else 0
        res_one['rqyl'] = one_d['rqyl'] if one_d['rqyl'] else 0
        try:
            res_one['rqpjcb'] = round(one_d['rqye'] / one_d['rqyl'], 3)  # 融券平均成本
        except:
            res_one['rqpjcb'] = 0
        last_res_data.append(res_one)
    result = []
    for da in last_res_data:
        if last_date and (da['trade_date'] == last_date):
            break
        da['stock_id'] = stock_id
        da['is_delete'] = 0
        timeArray = time.localtime(time.time())
        otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
        da['create_time'] = otherStyleTime
        da['update_time'] = otherStyleTime
        result.append(tuple(da.values()))
    sql = 'insert into stocks_rzrq(`trade_date`,`spj`,`zdf`,`rzyezb`,`rzmre`,`rzche`,`rzjme`,`rzye`,`rzrqye`,`rzrqyecz`,`rqye`,`rqmcl`,`rqchl`,`rqjmg`,`rqyl`,`rqpjcb`,`stock_id`,`is_delete`,`create_time`,`update_time`)  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    bd_mysql_cnn.save_many(sql, result)
    # print(f'更新-{code}-融资融券成功')
    return True



def get_all_stocks_rzrq():
    stocks = bd_mysql_cnn.fetchall('SELECT  id,symbol from stocks_a_stocks')
    for stock in stocks:
        stock_id = stock['id']
        code = stock['symbol']
        filter_stocks = bd_mysql_cnn.fetchall(
            f'select * from stocks_rzrq where stock_id={stock_id} order by trade_date desc limit 1')
        last_date = None
        if filter_stocks:
            last_date = str(filter_stocks[0]['trade_date'])
        get_rongzirongquan_from_dfcf(code, stock_id, last_date)


if __name__ == '__main__':
    # get_rongzirongquan_from_dfcf('002701', 1151, '2020-04-09')
    # get_rongzirongquan_from_dfcf('000004', 3, None)
    get_all_stocks_rzrq()

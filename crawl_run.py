# -*- coding:utf-8 -*-
# editor: gmj
# Date: 2020-04-12 21:53
# desc: 数据爬虫的运行文件

import schedule
import time
from crawler.dfcf.rzrq import get_all_stocks_rzrq
from crawler.ths.ths_trade_minute import request_all_stocks_minutes_data


def trade_minute():
    request_all_stocks_minutes_data()


def dfcf_rzrq():
    get_all_stocks_rzrq()


def main():
    # schedule.every(10).minutes.do(job)
    # schedule.every().hour.do(job)
    schedule.every().day.at("19:30").do(trade_minute)
    schedule.every().day.at("20:45").do(dfcf_rzrq)
    # schedule.every(5).to(10).days.do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
    # trade_minute()

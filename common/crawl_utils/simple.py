# -*- coding: UTF-8 -*-
# Date   : 2020/3/20 13:26
# Editor : gmj
# Desc   :
import json
from lxml import etree
import requests

simple_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
}


# 获取代理ip
def get_proxy():
    res = requests.get("http://106.13.63.136:5010/get/")
    res = json.loads(res.text)
    if 'code' in res:
        return None
    return res['proxy']


def get_by_proxy(url, data=None, headers=simple_header, verify=True):
    res = ''
    while not res:
        proxyIp = get_proxy()
        try:
            res = requests.get(url, proxies={'http': f'http://{proxyIp}'}, data=data, headers=headers, verify=verify,
                               timeout=10)
        except:
            try:
                res = requests.get(url, proxies={'https': f'https://{proxyIp}'}, data=data, headers=headers,
                                   verify=verify, timeout=10)
            except:
                pass
    return res


def post_by_proxy(url, data=None, headers=simple_header):
    res = ''
    while not res:
        proxyIp = get_proxy()
        try:
            res = requests.post(url, proxies={'http': f'http://{proxyIp}'}, data=data, headers=headers, timeout=10)
        except:
            try:
                res = requests.post(url, proxies={'https': f'https://{proxyIp}'}, data=data, headers=headers,
                                    timeout=10)
            except:
                pass
    return res


def get_url(url, data=None, headers=simple_header):
    return requests.get(url, data=data, headers=headers)


def get_json(txt):
    return json.loads(txt)


def get_html(txt):
    return etree.HTML(txt)

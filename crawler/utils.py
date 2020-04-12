# -*- coding:utf-8 -*-
# editor: gmj
# Date: 2020-04-11 21:57
# desc:

import time


def get_create_time():
    timeArray = time.localtime(time.time())
    return time.strftime("%Y--%m--%d %H:%M:%S", timeArray)

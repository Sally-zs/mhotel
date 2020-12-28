# Author:wanzi
# -*- coding: utf-8 -*-
#coding:utf-8
from datetime import datetime,timedelta

nowtime = datetime.now()

# print (nowtime)
print (nowtime.strftime("%y-%m-%d %H:%M:%S"))
print (nowtime+timedelta(hours =1))
# Author:wanzi
# -*- coding: utf-8 -*-
#coding:utf-8
from datetime import datetime,timedelta
#
# nowtime = datetime.now()
# print (nowtime)
# print (nowtime.strftime("%y-%m-%d %H:%M:%S"))
# print (nowtime+timedelta(hours =1))

#input的使用
#1.input默认输入为字符串
# password = eval(input("请输入你的密码："))
# print(password)
# print(type(password))

# #2.input强制修改输入为int类型
# age = int(input("请输入你的年龄:"))
# print(age)

# favorite_foods = input("请输入你最爱的水果：")
# # if favorite_foods in "草莓":
# #     print("你最爱的水果是草莓")
# # elif favorite_foods in "芒果":
# #     print("你最爱的水果是芒果")
# # else:
# #     print("你输入有误")


# name = "测试"
# # name1 = "丸子"
# # print("我的名字:%s"%name)
# # print("我的名字:%s %s"%(name,name1))
# #
# # age = 18
# # age1 =19
# # print("你的年龄:%d"%age)
# # print(type("你的年龄:%d"%age))
# # print("你的年龄:%d 还是 %d ？"%(age,age1))
# #
# #
# # now_time = 13.14
# # now_time1 = 13.15
# #
# # print("现在的时间:%f"%now_time)
# # print("现在的时间:%f %f"%(now_time,now_time1))
# # print("现在的时间:%.2f"%now_time)
# #
# #
# # a = 1
# # b = 2
# # print("a={} b={}".format(a,b))
# # print(type("a={} b={}".format(a,b)))
# #
# # c = "1"
# # d = "2"
# # print("c={} d={}".format(c,d))
# # print(type("c={} d={}".format(c,d)))

# #首字母大写
# name = "mango"
# print(name.capitalize())

#统计有多少个a
# name = "mango"
# print(name.count("a"))
#
# #将name居中打印，前后用-表示
# name = "mango"
# print(name.center(50,"-"))
# #
# #判断结尾是否以go结尾
# name = "mango"
# print(name.endswith("go"))
#
#查找字符串索引
# name = "mango"
# print(name.find("g"))
#
# #判断是否有中文或字母或数字
# name="mango芒果123"
# print(name.isalnum())
#
# #判断是否纯英文字符
# name="mango123"
# name1="mango"
# print(name.isalpha())
# print(name1.isalpha())
#
# #是否合法标识符/变量名
# name = "mango"
# print(name.isidentifier())
#
# #判断是不是小写
# name = "mango"
# print(name.islower())
#
# #判断是不是数字
# name = "mango"
# print(name.isnumeric())
#
# #判断是不是空格
# name = "mango"
# print(name.isspace())
#
#
# #判断是不是首字母大写
# name = "mango"
# print(name.istitle())
#
#
# #判断是不是大写
# name = "MAngo"
# print(name.isupper())
#
# #把大写变成小写
# name = "MANGO"
# print(name.lower())
#
# #把小写变成大写
# name = "mango"
# print(name.upper())

#去掉右边空格或换行
# name = "  mango ---" \
#        ""
# print(name.rstrip())
#
#去掉左边空格或换行
name = "  mango " \
       ""
print(name.lstrip())
#
#替换  入参（“原字符”，“目标字符”）
name = "mango"
print(name.replace("go","goo"))

#
#按照关键字分割字符串
name = "mango"
print(name.split("n"))

#字符串连接
str = "---"
name = ("mango","test")
print(str.join(name))
















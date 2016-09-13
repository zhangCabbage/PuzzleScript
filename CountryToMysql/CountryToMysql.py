#coding: utf-8
import sys
import os
import re
from pypinyin import lazy_pinyin
import chardet
import MySQLdb
import requests
import json


pattern = re.compile(r'\t+|\-{2}|\n')
clearPattern = re.compile(r'\s+$')
numPattern = re.compile(r'\d+')
countryID = 0
provinceID = 0
country = ""
province = ""

"""
待完善：
1、需要一个进度条来显示进度
2、运行时如果能选择看或者不看打印的日志就更好了
"""

conn = MySQLdb.connect(host='120.24.42.115', user='root', passwd='secsmarts', db='secsmarts', port=3306, charset='utf8')
# this should set charset as utf8

def getFieldID(field, fieldType):
    """ 找 field 在 mysql 中对应的ID"""
    try:
        cur = conn.cursor()
        sql = "select id from location where text='"+field+"' and type = " + `fieldType`
        print "sql => ", sql
        cur.execute(sql)
        res = cur.fetchone()
        if res is None:
            print "在Mysql中找不到对应ID..."
            return 0

        if fieldType == 0:
            global countryID
            countryID = int(res[0])
        elif fieldType == 1:
            global provinceID
            provinceID = int(res[0])
            global province
            province = field

        print "获取到[{0}]对应ID为：{1}".format(field, int(res[0]))
        return int(res[0])
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def insertOrUpdateMysql(firstName, englishName, chineseName, fieldType):
    """ 插入或更新数据库 """
    resID = 0
    try:
        cur=conn.cursor()

        sql = ""
        # 插入之前先检查，表中是否已经存在
        if getFieldID(chineseName, fieldType) is not 0:
            print "已存在"
        else:
            if fieldType == 1:
                print "正在插入省级ing..."
                sql = "insert into location(initial, name, text, type, parent_id) values('" + firstName + "', '" + englishName + "','" + chineseName + "', 1, " + `countryID` + ")"
            elif fieldType == 2:
                print "正在插入地级市ing..."
                lng, lat, englishName = googleLngLatService(country + province + chineseName, englishName)
                if(lng == 88888 and lat == 88888):
                    print "================================"
                    print "sorry，google也找不到，肿么办呀主人"
                    print "================================"
                    return
                print englishName
                print type(englishName)

                if isinstance(englishName, unicode):
                    englishName = englishName.encode("utf-8")

                print "google查询[{2}]的经纬度为 --> ({0}, {1})".format(lng, lat, englishName)

                sql = "insert into location(initial, name, text, latitude, longitude, type, parent_id) values('" + firstName + "', '" + englishName + "', '" + chineseName + "', " + `lat` + ", " + `lng` + ", 2, " + `provinceID` + ")"

            print "sql => ", sql
            res = cur.execute(sql)
            conn.commit()
            getFieldID(chineseName, fieldType)

    except MySQLdb.Error,e:
        conn.rollback()
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

# 省 type -- 1
# 市 type -- 2
def readFile(path):
    with open(path, 'r') as f:
        for line in f.readlines():
            print "\n\n"
            typeIndex = 0
            line = clearPattern.sub("", line)
            while(line[typeIndex] == '\t'):
                typeIndex += 1
            global pattern
            names = pattern.split(line)
            print names
            names = [x for x in names if x != '']

            if len(names) == 1:
                if typeIndex == 0:
                    print "[{0}]省级城市必须手动提供中英名称".format(names[0])
                    print "程序终止..."
                    return
                else:
                    chineseName = names[0]
                    englishName = ""
            else:
                chineseName, englishName = names[0:2]

            print "中英文名 --> ", chineseName, englishName

            firstName = getFirstName(chineseName)
            print "首字母 --> ", str(firstName)

            print "插入更新操作..."
            insertOrUpdateMysql(str(firstName), englishName, chineseName, typeIndex+1)


def googleLngLatService(city, englishName):
    """
    返回对应城市的经纬度
    google lng and lat service
    关于 python requests 库使用proxies代理的问题
    1) zsh: no matches found: requests[security] => pip install 'requests[security]'
    2) Missing dependencies for SOCKS support => pip install PySocks
    """
    proxies = {
        'http': 'socks5://@127.0.0.1:1080',
        'https': 'socks5://@127.0.0.1:1080'
        }
    param = {"address": city, "key": "AIzaSyD1Mhz9x43rDOb4ul-9HLEsPUEBggwKwvk"}
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params = param, proxies = proxies)

    if r.status_code == 200:
        print "google map service url => ", r.url
        res = json.loads(r.content)["results"]
        if len(res) > 0:
            """ google查的到的话 """

            location = res[0]["geometry"]["location"]
            if englishName == "":
                englishName = res[0]["address_components"][0]["long_name"]
            return location["lng"], location["lat"], englishName
        else:
            return 88888, 88888, ""
    else:
        return 88888, 88888, ""

def getFirstName(name):
    return lazy_pinyin(name.decode(chardet.detect(name)['encoding']))[0][0].upper()

if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print "请传入参数"
    else:
        path = sys.argv[1]
        if os.path.isfile(path):
            global country
            country = os.path.split(path)[1]
            print country
            print "--- ok, let's begin our work ---"
            getFieldID(country, 0)
            readFile(path)
            conn.close()
        else:
            print "--- Hey, wrong file path, please check it again! ---"

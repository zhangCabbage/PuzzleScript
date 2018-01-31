#coding:utf-8
"""
Campus Network Check
this script uses to check my computer is online every half an hour
if PC is not online, login
"""
import subprocess
import requests
import re

def checkConnect():
    check = subprocess.call('ping -c 2 baidu.com',shell=True)
    # if the windows it should be ping -n 2 baidu.com
    if check != 0:
        # ping不通，未联网，直接模拟登陆就可以
        url = "http://10.3.8.211/"
        r = requests.post(url, data={"DDDDD":"你的学号#####", "upass":"你的密码#####", "0MKKey":""})
        res = re.search("Msg=(\d+)\;", r.content)
        if res and int(res.group(1)) is 2:
            print "now two ip is online"
            reUrl = "http://10.3.8.211/a11.htm"
            r = requests.post(reUrl, data={"DDDDD":"2015110718", "upass":"158919", "passplace:":"", "AMKKey":""})
        print "Online"
    else:
        print "Online"

if __name__ == '__main__':
    checkConnect()

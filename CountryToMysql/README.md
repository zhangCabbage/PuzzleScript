# CountryToMySQL
Because of business need that we need the province and country all over the world and it's firstName, chineseName, englishName, longitude and latitude, then storage to MySQL. The bad new is that I am in China, so I can not visit Google directly.
So first time I try some way API of baidu or tencent，but it can not get the info fo foreign cities. Finally, I once again put Google's embrace.
In the project, I use the [Google Maps API](https://developers.google.com/maps/?hl=zh-cn) and use [python](https://www.python.org/) coding this script. Without a doubt, I use some certain ineffable technology to visit [google](https://www.google.com/) --- [shadowsocks](https://shadowsocks.com/) or [Lantern](https://getlantern.org/) is ok. And use the agent in the program.

## Library used
'pypinyin'、'MySQLdb'、[requests(for humans)](http://docs.python-requests.org/en/master/)maybe your need to install 'requests[security]' and dependencies Library 'PySocks'

## Quick Start
the province and the province-level municipality should get the chineseName and it's englishName and use two line to Separate, for the normal city should back one tab after it's parent province and it's englishName is not necessary. Finally, this file should name it's country name, Just like example of Korea. Then put these two files in the same directory, and run 'python CountryToMySQL.py 韩国'

## CreateTime
2016/09/07 11:28

## UpdateTime
2016/09/08 15:30

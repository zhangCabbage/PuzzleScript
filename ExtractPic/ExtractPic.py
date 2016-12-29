# -*- coding:utf-8 -*-

from elasticsearch import Elasticsearch
import threading, multiprocessing

import requests
import json
import os


def googleImageSearch1():
    """
    can not to use!!
    """
    service = build("customsearch", "v1", developerKey="AIzaSyAn_PAkGYezs8865Hj0waHr6qps1sb-47o")
    res = service.cse().list(
        q='中国移动',
        cx='000596965311184922162:jnt-pgjnbfe',
        searchType='image',
        num=35,
        imgType='clipart',
        safe= 'off'
    ).execute()

    if not 'items' in res:
        print 'No result !!\nres is: {}'.format(res)
    else:
        for item in res['items']:
            print('{}:\n\t{}'.format(item['title'], item['link']))


def googleImageSearch2():
    url = 'https://www.googleapis.com/customsearch/v1'

    def loop(*trademarks):
        """
        """
        proxies = {
            'http': 'socks5://@127.0.0.1:1080',
            'https': 'socks5://@127.0.0.1:1080'
        }
        param = {
            'key': 'AIzaSyD1Mhz9x43rDOb4ul-9HLEsPUEBggwKwvk',  #每个key每24小时，最多请求100次
            'cx': '000596965311184922162:jnt-pgjnbfe',
            'searchType': 'image',
            'q': '',
            'start': '',
        }

        for trademark in trademarks:
            if not os.path.exists(trademark):
                os.makedirs(trademark)

            for i in xrange(5):
                start = 10 * i + 1
                param['q'] = trademark
                param['start'] = start
                print param

                try:
                    r = requests.get(url, params = param, proxies = proxies)
                    resJson = json.loads(r.content)["items"] #每次返回十个
                    for item in resJson:
                        picUrl = item['link']
                        print picUrl
                        r = requests.get(picUrl, stream=True)

                        with open(trademark + os.path.sep +`start` + '.' + picUrl.split("/")[-1].split(".")[-1], 'wb') as f:
                            for chunk in r.iter_content(chunk_size=1024): 
                                if chunk: # filter out keep-alive new chunks
                                    f.write(chunk)
                        start += 1
                except Exception as e:
                    print "Error at【{}_{}】.".format(trademark.encode("utf8"), i)

    trademarks = readTrademarks()[40:60]
    print trademarks
    cpu_nums = multiprocessing.cpu_count()
    print "cpu_nums --> ", cpu_nums
    lens = len(trademarks) / cpu_nums + (1 if len(trademarks) % cpu_nums != 0 else 0)
    start = 0
    for _ in xrange(cpu_nums):
        end = start + lens if start + lens < len(trademarks) else len(trademarks)
        thread = threading.Thread(target=loop, args=(trademarks[start : end]))
        thread.start()

        if end == len(trademarks):
            break
        start = end

def readTrademarks():
    """
    读取es中商标信息
    """
    es = Elasticsearch("http://221.122.108.130:9200")
    response = es.search(index="goodsite", doc_type='goodsite', size=120)
    trademarks = []
    for hit in response['hits']['hits']:
        sitename = hit["_source"]["sitename"]
        trademarks.append(sitename)
    return trademarks

if __name__ == '__main__':
    googleImageSearch2()



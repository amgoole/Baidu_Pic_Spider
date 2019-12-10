# -*- coding: utf-8 -*-
"""
Author  : Lamadog
Time    : 2019/12/10
Email   : xwen.xi@icloud.com
"""
import os
import re
import threading
import time
from urllib import request, parse
import multiprocessing
from config import *


class Spider(object):

    def __init__(self, word):
        self.word = word
        if not os.path.exists(f'./{self.word}'):
            os.makedirs(f'./{self.word}')

    def start_img(self):
        urls = []
        k = 0
        req = request.Request(url.format(parse.quote(self.word)), headers=headers)
        print(url.format(self.word))
        while True:
            if k == 0:
                try:
                    html = request.urlopen(req, timeout=30).read().decode('utf-8')
                except ConnectionError as ex:
                    raise ex
                for item in [url1, url2]:
                    urls.extend(re.findall(item, html))
                urls = list(set(urls))
            yield urls[k]
            k += 1
            k = 0 if k >= len(urls) else k

    def down(self, pre_down, who):
        page = 0
        pic_url = pre_down.send(None)
        while True:
            print(f'Thread-{who}', pic_url)
            req = request.Request(pic_url, headers=headers)
            try:
                res = request.urlopen(req, timeout=30)
                time.sleep(2)
            except ConnectionError as ex:
                pre_down.close()
                raise print(ex)
            with open(f'./{self.word}/{page}.jpg', 'wb') as fp:
                fp.write(res.read())
                fp.flush()
                fp.close()
                page += 1
            pic_url = pre_down.send('finish!')


if __name__ == "__main__":
    spider = Spider('刘亦菲')
    for i in range(multiprocessing.cpu_count()):
        t = threading.Thread(target=spider.down, args=(spider.start_img(), i))
        t.start()

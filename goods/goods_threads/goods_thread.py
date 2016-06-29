#!usr/bin/env python

import threading
from ..goods_spider.spider import GoodsListSpider
from ..utils.const_value import WEB_NAME


class GoodsThread(threading.Thread):
    def __init__(self, lock, all_goods, keywords, web):
        threading.Thread.__init__(self)
        self.lock = lock
        self.keywords = keywords
        self.web = web
        self.all_goods = all_goods

    def run(self):
        goods_list_spider = GoodsListSpider(self.keywords)
        if self.web in WEB_NAME.values():
            result = goods_list_spider.fetch_goods()[self.web]()
            if result:
                self.append_data(result)

    def append_data(self, data):
        self.lock.acquire()
        self.all_goods.extend(data)
        self.lock.release()

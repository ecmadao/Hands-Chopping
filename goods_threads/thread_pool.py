import threading
from .goods_thread import GoodsThread

WEBS = ('jd', 'taobao')

threads = []
lock = threading.Lock()
all_goods = []


def build_thread(keywords):
    global all_goods
    for web in WEBS:
        goods_thread = GoodsThread(lock, all_goods, keywords, web)
        threads.append(goods_thread)
        goods_thread.start()


def export_date():
    for thread in threads:
        if thread:
            thread.join()
    return all_goods

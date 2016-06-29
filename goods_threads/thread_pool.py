import threading
from .goods_thread import GoodsThread

threads = []
lock = threading.Lock()
all_goods = []


def build_thread(keywords, webs):
    """build thread by target web & put them into a thread pool

    :param keywords: search target
    :param webs: target shopping site
    :return:
    """
    global all_goods
    for web in webs:
        goods_thread = GoodsThread(lock, all_goods, keywords, web)
        threads.append(goods_thread)
        goods_thread.start()


def export_date():
    """finish all thread & get result data

    :return: search result
    """
    for thread in threads:
        if thread:
            thread.join()
    return all_goods

import threading
from .goods_thread import GoodsThread


class Threads(object):

    def __init__(self):
        self._goods = []
        self._lock = threading.Lock()
        self._threads = []

    def build(self, keywords, webs):
        """build thread by target web & put them into a thread pool

        :param keywords: search target
        :param webs: target shopping site
        :return:
        """
        for web in webs:
            goods_thread = GoodsThread(self._lock, self._goods, keywords, web)
            self._threads.append(goods_thread)
            goods_thread.start()

    @property
    def goods(self):
        """finish all thread & get result data

        :return: search result
        """
        for thread in self._threads:
            if thread:
                thread.join()
        return self._goods

threads = Threads()
# def build_thread(keywords, webs):
#     """build thread by target web & put them into a thread pool
#
#     :param keywords: search target
#     :param webs: target shopping site
#     :return:
#     """
#     global all_goods
#     for web in webs:
#         goods_thread = GoodsThread(lock, all_goods, keywords, web)
#         threads.append(goods_thread)
#         goods_thread.start()
#
#
# def export_date():
#     """finish all thread & get result data
#
#     :return: search result
#     """
#     for thread in threads:
#         if thread:
#             thread.join()
#     return all_goods

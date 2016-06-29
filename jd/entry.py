#!usr/bin/env python
from colorama import Fore
from prettytable import PrettyTable
from .spiders import GoodsListSpider
from utils.message import colorful_text

TABLE_TITLE = ('编号', '简介', '价格', '邮费', '购买人数', '所属')
ITEM_KEY = ('index', 'intro', 'price', 'delivery', 'sales', 'belong')


def get_goods(goods_keywords):
    """get keywords and search in taobao

    :param goods_keywords: input keywords
    :return: None
    """
    assert isinstance(goods_keywords, list)
    key_words = '+'.join(goods_keywords)
    goods_list_spider = GoodsListSpider(key_words)
    search_result = goods_list_spider.open_in_selenium()
    if search_result:
        print_goods(search_result)


def print_goods(search_result):
    """use validate search result to print a table

    :param search_result: search result in taobao
    :return: None
    """
    goods_table = PrettyTable(TABLE_TITLE)
    for goods in search_result:
        goods_row = [goods[item] for item in ITEM_KEY]
        goods_table.add_row(goods_row)
    print(colorful_text('ready to hands chopping?', Fore.CYAN))
    print(goods_table)

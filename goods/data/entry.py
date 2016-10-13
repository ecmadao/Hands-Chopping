#!usr/bin/env python
"""
get data and print table package
"""
import webbrowser
from operator import itemgetter
from colorama import Fore
from prettytable import PrettyTable
from ..utils.message import colorful_text, error_message
from ..threads.core import threads


TABLE_TITLE = ('编号', '简介', '价格', '邮费', '购买人数', '所属')
ITEM_KEY = ('index', 'intro', 'price', 'delivery', 'sales', 'belong')


def get_goods(goods_keywords, webs):
    """get keywords and search

    :param goods_keywords: input keywords
    :param webs: webs which will be search
    :return: None
    """
    try:
        assert isinstance(goods_keywords, list)
    except AssertionError:
        error_message('expect to receive a list')
    key_words = '+'.join(goods_keywords)
    threads.build(key_words, webs)
    print_goods(threads.goods)


def print_goods(search_result):
    """use validate search result to print a table

    :param search_result: search result in taobao and jd
    :return: None
    """
    search_result = sort_by_money(search_result)

    goods_table = PrettyTable(TABLE_TITLE)
    for index, goods in enumerate(search_result):
        goods["index"] = index
        goods_row = [goods[item] for item in ITEM_KEY]
        goods_table.add_row(goods_row)
    print(colorful_text('ready to hands chopping?', Fore.CYAN))
    print(goods_table)
    open_detail_page(search_result)


def sort_by_money(search_result):
    result = sorted(search_result, key=itemgetter('price'), reverse=True)
    return result


def open_detail_page(filtered_goods):
    """expect a number or a string which joined by ','
    to open the target goods url in a browser window

    :param filtered_goods
    :return: None
    """
    print(colorful_text('which do you prefer? type it\'s index', Fore.MAGENTA))
    print(colorful_text('if many, use \',\' to split them', Fore.MAGENTA))
    print(colorful_text('use \'control + c\' to exit.', Fore.RED))
    try:
        index = input('goods index: ')
        result_goods = filter(get_target_goods(
            index.split(',')), filtered_goods)
        goods_list = [goods for goods in result_goods]

        if len(goods_list):
            for goods in goods_list:
                goods_url = goods["url"]
                if goods_url[0] == '/':
                    goods_url = 'https:{}'.format(goods_url)
                webbrowser.open_new(goods_url)
        else:
            error_message('no such index')
            open_detail_page(filtered_goods)
    except KeyboardInterrupt:
        error_message('exit')


def get_target_goods(indexs):
    """search in filtered_goods by user's input indexs

    :param indexs: user's input indexs
    :return: if is validate
    """
    def filter_goods(goods):
        return str(goods["index"]) in indexs
    return filter_goods

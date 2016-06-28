#!usr/bin/env python

from colorama import Fore
import webbrowser
from prettytable import PrettyTable
from .spiders import GoodsListSpider
from utils.message import colorful_text, error_message

TABLE_TITLE = ('编号', '简介', '价格', '邮费', '购买人数', '所属')
ITEM_KEY = ('index', 'intro', 'price', 'delivery', 'sales', 'belong')


def get_goods(goods_keywords):
    assert isinstance(goods_keywords, list)
    key_words = '+'.join(goods_keywords)
    goods_list_spider = GoodsListSpider(key_words)
    search_result = goods_list_spider.fetch_goods()
    if search_result:
        print_goods(search_result)


def filter_target_data(search_result):
    return [{
            'index': index,
            'intro': result["raw_title"],
            'price': result["view_price"],
            'delivery': colorful_text(result["view_fee"], Fore.RED)
            if float(result["view_fee"]) > 0 else result["view_fee"],
            'sales': result["view_sales"],
            'belong': colorful_text("天猫", Fore.CYAN) if result["shopcard"]["isTmall"] else "淘宝",
            'url': result["detail_url"]
            } for index, result in enumerate(search_result)]


def print_goods(search_result):
    goods_table = PrettyTable(TABLE_TITLE)
    filtered_goods = filter_target_data(search_result)
    for goods in filtered_goods:
        goods_row = [goods[item] for item in ITEM_KEY]
        goods_table.add_row(goods_row)
    print(colorful_text('ready to hands chopping?', Fore.CYAN))
    print(goods_table)
    open_detail_page(filtered_goods)


def open_detail_page(filtered_goods):
    print(colorful_text('which do you prefer? type it\'s index', Fore.MAGENTA))
    print(colorful_text('if many, use \',\' to split them'))
    try:
        index = input('goods index: ')
        result_goods = filter(get_target_goods(index.split(',')), filtered_goods)
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
    def filter_goods(goods):
        return str(goods["index"]) in indexs
    return filter_goods

#!usr/bin/env python

"""

Usage:
    entry.py [-j | -t] <goods>

Options:
    -h --help  显示帮助菜单
    -goods     关键字
    -j         京东
    -t         淘宝

Examples:
    entry.py 移动硬盘
    entry.py 硬盘-东芝
"""
from docopt import docopt
from goods_data import entry
from utils.const_value import WEB_NAME


def get_input():
    """get input from comment line

    :return: None
    """
    arguments = docopt(__doc__, version="beta 0.1")
    goods_keywords = arguments['<goods>'].split('-')
    webs = [WEB_NAME[web] for web in WEB_NAME.keys() if arguments[web]]
    if not len(webs):
        webs = WEB_NAME.values()
    entry.get_goods(goods_keywords, webs)


if __name__ == '__main__':
    get_input()

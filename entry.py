#!usr/bin/env python

"""

Usage:
    entry.py <goods>

Options:
    -h --help  显示帮助菜单
    -goods     关键字

Examples:
    entry.py 移动硬盘
"""
from docopt import docopt
from taobao import entry


def get_input():
    arguments = docopt(__doc__, version="beta 0.1")
    goods_keywords = arguments['<goods>'].split('-')
    entry.get_goods(goods_keywords)


if __name__ == '__main__':
    get_input()

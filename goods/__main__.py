#!usr/bin/env python
"""
Usage:
    $ goods [--site= all | jd | tb]

Options:
    --site: 要搜索的网站，jd-京东，tb-淘宝，默认全部

Example:
    $ goods --site=jd
    $ goods
"""

import click
from .data import entry
from .utils.const_value import WEB_NAME


@click.command()
@click.option('--goods', prompt='what do you wanna search')
@click.option('--site', type=click.Choice(['all', 'jd', 'tb']), default='all')
def main(goods, site):
    """get input from comment line

    :param goods
    :param site
    :return: None
    """
    goods_keywords = goods.split(' ')
    webs = WEB_NAME.get(site, WEB_NAME['all'])
    entry.get_goods(goods_keywords, webs)
    exit(0)


if __name__ == '__main__':
    main()

#!usr/bin/env python

from datetime import date


TAOBAO_SEARCH = 'https://s.taobao.com/search?q={keywords}imgfile=&js=1' \
                '&stats_click=search_radio_all%3A1&initiative_id=staobaoz_{date}&ie=utf8'


def get_goods(goods):
    assert isinstance(goods, list)
    key_words = '+'.join(goods)
    search_date = ''.join(str(date.today()).split('-'))
    search_url = TAOBAO_SEARCH.format(keywords=key_words, date=search_date)
    print(search_url)

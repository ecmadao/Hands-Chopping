import ssl
import re
import json
from datetime import date
from colorama import Fore
from urllib import request, error
from fake_useragent import UserAgent
from ..utils.message import notice, error, colorful_text
from .base import BaseSpider

ssl._create_default_https_context = ssl._create_unverified_context

TAOBAO_SEARCH = 'https://s.taobao.com/search?q={keywords}&imgfile=&js=1' \
                '&stats_click=search_radio_all%3A1&initiative_id=staobaoz_{date}&ie=utf8'


class TaobaoSpider(BaseSpider):

    def __init__(self, keywords):
        super().__init__(keywords)

    def __fetch_goods__(self):
        super().__fetch_goods__()
        search_date = ''.join(str(date.today()).split('-'))
        url = TAOBAO_SEARCH.format(keywords=self.keywords, date=search_date)
        req = request.Request(url, headers=self.headers)
        response = request.urlopen(req).read().decode('UTF-8')

        re_result = re.findall(
            r'g_page_config\s*=\s*(.*);', str(response))[0]
        json_result = json.loads(re_result)
        return self.__data_parser__(json_result)

    def __data_parser__(self, data):
        if data['mods']['itemlist']['data']['auctions']:
            search_results = data['mods']['itemlist']['data']['auctions']
            return [{
                    'intro': result["raw_title"],
                    'price': float(result["view_price"]),
                    'delivery': colorful_text(result["view_fee"], Fore.RED)
                    if float(result["view_fee"]) > 0 else result["view_fee"],
                    'sales': int(result["view_sales"].split('人')[0]),
                    'belong': colorful_text("天猫", Fore.CYAN)
                    if result["shopcard"] and result["shopcard"].get('isTmall', False) else "淘宝",
                    'url': result["detail_url"]
                    } for result in search_results]
        error('Ops, get no goods..')
        return []

    @property
    def goods(self):
        notice('get taobao goods...')
        return self.__fetch_goods__()

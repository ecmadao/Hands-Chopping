import ssl
import re
import json
from datetime import date
from colorama import Fore
from urllib import request, error, parse
from fake_useragent import UserAgent
from ..utils.message import notice, error, colorful_text

ssl._create_default_https_context = ssl._create_unverified_context

TAOBAO_SEARCH = 'https://s.taobao.com/search?q={keywords}&imgfile=&js=1' \
                '&stats_click=search_radio_all%3A1&initiative_id=staobaoz_{date}&ie=utf8'


class TaobaoSpider(object):

    def __init__(self, keywords):
        self.keywords = parse.quote(keywords)
        self.headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': None
        }

    def __fetch_goods__(self):
        ua = UserAgent()
        search_date = ''.join(str(date.today()).split('-'))
        url = TAOBAO_SEARCH.format(keywords=self.keywords, date=search_date)
        self.headers['User-Agent'] = ua.random
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

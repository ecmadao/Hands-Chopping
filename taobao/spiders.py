#!usr/bin/env python

import re
import ssl
import json
from datetime import date
from urllib import request, error, parse
from utils import message

ssl._create_default_https_context = ssl._create_unverified_context

TAOBAO_SEARCH = 'https://s.taobao.com/search?q={keywords}&imgfile=&js=1' \
                '&stats_click=search_radio_all%3A1&initiative_id=staobaoz_{date}&ie=utf8'


class GoodsListSpider(object):
    def __init__(self, keywords):
        keywords = parse.quote(keywords)
        search_date = ''.join(str(date.today()).split('-'))
        self.url = TAOBAO_SEARCH.format(keywords=keywords, date=search_date)
        self.headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11',
            'GET': self.url
        }

    def fetch_goods(self):
        search_result = None
        try:
            req = request.Request(self.url, headers=self.headers)
            response = request.urlopen(req).read().decode('UTF-8')
            re_result = re.findall(r'g_page_config\s*=\s*(.*);', str(response))[0]
            json_result = json.loads(re_result)

            # with open('./taobao/taobao.html', encoding='utf-8') as f:
            #     response = f.read()
            # re_result = re.findall(r'g_page_config\s*=\s*(.*);', str(response))[0]
            # json_result = json.loads(re_result)

            if json_result['mods']['itemlist']['data']['auctions']:
                search_result = json_result['mods']['itemlist']['data']['auctions']
            else:
                message.error_message('没有搜索到商品')
        except (error.HTTPError, error.URLError, error.ContentTooShortError):
            message.error_message()
        except UnicodeEncodeError:
            message.error_message('encoding error')
        finally:
            return search_result

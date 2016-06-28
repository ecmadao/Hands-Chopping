#!usr/bin/env python
import re
import ssl
import json
from urllib import request, error
from utils import message

ssl._create_default_https_context = ssl._create_unverified_context


class GoodsListSpider(object):
    def __init__(self, url):
        self.url = url
        self.headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11',
            'GET': url
        }

    def fetch_goods(self):
        try:
            req = request.Request(self.url, headers=self.headers)
            response = request.urlopen(req).read().decode('UTF-8')
            re_result = re.findall(r'g_page_config\s*=\s*(.*);', str(response))[0]
            json_result = json.loads(re_result)
            if json_result['mods']['itemlist']['data']['auctions']:
                return json_result['mods']['itemlist']['data']['auctions']
            else:
                return message.error_message('没有搜索到商品')
        except (error.HTTPError, error.URLError, error.ContentTooShortError):
            return message.error_message()

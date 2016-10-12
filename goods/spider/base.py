from fake_useragent import UserAgent
from urllib import parse


class BaseSpider(object):

    def __init__(self, keywords):
        self.keywords = parse.quote(keywords)
        self.headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': None
        }

    def __fetch_goods__(self):
        us = UserAgent()
        self.headers['User-Agent'] = us.random

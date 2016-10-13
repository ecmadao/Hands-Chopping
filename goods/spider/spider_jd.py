from selenium import webdriver
from lxml import etree
from random import randrange
from colorama import Fore
from .base import BaseSpider
from ..utils.message import error, notice, colorful_text

JD_SEARCH = 'https://search.jd.com/Search?keyword={}&enc=utf-8&suggest=1.def.0&wq={}'


class JdSpider(BaseSpider):

    def __init__(self, keywords):
        super().__init__(keywords)

    def __fetch_goods__(self):
        url = JD_SEARCH.format(self.keywords, self.keywords)
        driver = webdriver.PhantomJS()
        driver.set_window_size(1024, 2000)
        driver.get(url)
        driver.implicitly_wait(randrange(1, 3))
        js = "document.body.scrollTop=100000"
        driver.execute_script(js)
        return self.__data_parser__(driver.page_source)

    def __data_parser__(self, data):
        html = etree.HTML(data)
        search_results = []
        for li in html.xpath('//li[@class="gl-item"]'):
            try:
                div = li.xpath('.//div[contains(@class, "p-img")]')[0]
                search_results.append({
                    'url': div.xpath('./a/@href')[0],
                    'intro': div.xpath('./a/@title')[0],
                    'price': float(li.xpath('.//div[@class="p-price"]')[0]
                                   .xpath('./strong/i/text()')[0].strip()),
                    'delivery': 'none',
                    'sales': li.xpath('.//div[@class="p-commit"]')[0]
                    .xpath('./strong/a/text()')[0].strip(),
                    'belong': colorful_text('京东', Fore.CYAN)
                })
            except (IndexError, ValueError) as e:
                error()
        return search_results

    @property
    def goods(self):
        notice('get jd goods..')
        return self.__fetch_goods__()

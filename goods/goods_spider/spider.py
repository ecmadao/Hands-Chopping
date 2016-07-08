#!usr/bin/env python
import ssl
import re
import json
from datetime import date
from urllib import request, error, parse
from colorama import Fore
from bs4 import BeautifulSoup
from selenium import webdriver
from ..utils.message import colorful_text, error_message

ssl._create_default_https_context = ssl._create_unverified_context

JD_SEARCH = 'https://search.jd.com/Search?keyword={}&enc=utf-8&suggest=1.def.0&wq={}'
TAOBAO_SEARCH = 'https://s.taobao.com/search?q={keywords}&imgfile=&js=1' \
                '&stats_click=search_radio_all%3A1&initiative_id=staobaoz_{date}&ie=utf8'


class GoodsListSpider(object):
    def __init__(self, keywords):
        keywords = parse.quote(keywords)
        self.keywords = keywords
        self.headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11',
        }
        self.url = None

    def fetch_goods(self):
        """web spider object creator

        :return: A object which contains different web spider
        """
        return {
            'jd': self.jd_spider,
            'taobao': self.taobao_spider
        }

    def jd_spider(self):
        self.url = JD_SEARCH.format(self.keywords, self.keywords)
        driver = webdriver.PhantomJS()
        driver.set_window_size(1024, 2000)
        driver.implicitly_wait(7)
        print(colorful_text('open jd search page....', color=Fore.RED))
        driver.get(self.url)
        return self.fetch_jd_goods(driver.page_source)

    @staticmethod
    def fetch_jd_goods(response):
        print(colorful_text('fetching goods from jd....', color=Fore.RED))
        search_result = None
        try:
            soup = BeautifulSoup(response, 'lxml')
            j_goods_list = soup.find('div', id="J_goodsList").find_all('li', attrs={"class": "gl-item"})

            if j_goods_list:
                search_result = []
                for j_goods_item in j_goods_list:
                    if j_goods_item.find('div', attrs={"class": "p-img"}):
                        j_goods = {
                            'url': j_goods_item.find('div', attrs={"class": "p-img"}).a.attrs["href"],
                            'intro': j_goods_item.find('div', attrs={"class": "p-name"}).a.attrs["title"],
                            'price': float(j_goods_item.find('div', attrs={"class": "p-price"})
                                           .find('strong').find('i').string.strip()),
                            'delivery': 'none',
                            'sales': int(j_goods_item.find('div', attrs={"class": "p-commit"})
                            .find('strong').find('a').string.strip()),
                            'belong': colorful_text('京东', Fore.CYAN)
                        }
                        search_result.append(j_goods)
            else:
                error_message('没有搜索到商品')
        except (error.HTTPError, error.URLError, error.ContentTooShortError):
            error_message()
        except UnicodeEncodeError:
            error_message('encoding error')
        finally:
            return search_result

    def taobao_spider(self):
        search_date = ''.join(str(date.today()).split('-'))
        self.url = TAOBAO_SEARCH.format(keywords=self.keywords, date=search_date)
        self.headers['GET'] = self.url
        fetch_taobao_result = self.fetch_taobao_goods()
        if fetch_taobao_result:
            return self.filter_taobao_data(fetch_taobao_result)
        else:
            return None

    def fetch_taobao_goods(self):
        """taobao spider

        :return: None or search result
        """
        search_result = None
        print(colorful_text('fetching goods from taobao....', color=Fore.MAGENTA))
        try:
            req = request.Request(self.url, headers=self.headers)
            response = request.urlopen(req).read().decode('UTF-8')
            re_result = re.findall(r'g_page_config\s*=\s*(.*);', str(response))[0]
            json_result = json.loads(re_result)

            # with open('./goods/goods_spider/taobao.html', encoding='utf-8') as f:
            #     response = f.read()
            # re_result = re.findall(r'g_page_config\s*=\s*(.*);', str(response))[0]
            # json_result = json.loads(re_result)

            if json_result['mods']['itemlist']['data']['auctions']:
                search_result = json_result['mods']['itemlist']['data']['auctions']
            else:
                error_message('没有搜索到商品')
        except (error.HTTPError, error.URLError, error.ContentTooShortError):
            error_message()
        except UnicodeEncodeError:
            error_message('encoding error')
        finally:
            return search_result

    @staticmethod
    def filter_taobao_data(search_result):
        """get target data in search result

        :param search_result
        :return: validate data list
        """

        return [{
                'intro': result["raw_title"],
                'price': float(result["view_price"]),
                'delivery': colorful_text(result["view_fee"], Fore.RED)
                if float(result["view_fee"]) > 0 else result["view_fee"],
                'sales': int(result["view_sales"].split('人')[0]),
                'belong': colorful_text("天猫", Fore.CYAN)
                if result["shopcard"] and result["shopcard"].get('isTmall', False) else "淘宝",
                'url': result["detail_url"]
                } for result in search_result]

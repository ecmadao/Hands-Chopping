import ssl
from urllib import request, error, parse
from colorama import Fore
from bs4 import BeautifulSoup
from selenium import webdriver
from utils import message

JD_SEARCH = 'https://search.jd.com/Search?keyword={}&enc=utf-8&suggest=1.def.0&wq={}'

ssl._create_default_https_context = ssl._create_unverified_context

# ITEM_KEY = ('index', 'intro', 'price', 'delivery', 'sales', 'belong')


class GoodsListSpider(object):
    def __init__(self, keywords):
        keywords = parse.quote(keywords)
        self.url = JD_SEARCH.format(keywords, keywords)
        self.headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11',
            'GET': self.url
        }

    def open_in_selenium(self):
        driver = webdriver.PhantomJS()
        driver.set_window_size(1024, 2000)
        driver.implicitly_wait(20)
        print(message.colorful_text('driver fetch page....', color=Fore.RED))
        driver.get(self.url)
        return self.fetch_jd_goods(driver.page_source)

    @staticmethod
    def fetch_jd_goods(response):
        print(message.colorful_text('fetching goods from jd....', color=Fore.RED))
        search_result = None
        try:

            soup = BeautifulSoup(response, 'lxml')
            j_goods_list = soup.find('div', id="J_goodsList").find_all('li', attrs={"class": "gl-item"})

            if j_goods_list:
                search_result = []
                for index, j_goods_item in enumerate(j_goods_list):
                    if j_goods_item.find('div', attrs={"class": "p-img"}):
                        j_goods = {
                            'index': index,
                            'url': j_goods_item.find('div', attrs={"class": "p-img"}).a.attrs["href"],
                            'intro': j_goods_item.find('div', attrs={"class": "p-name"}).a.attrs["title"],
                            'price': j_goods_item.find('div', attrs={"class": "p-price"})
                            .find('strong').find('i').string.strip(),
                            'delivery': 'none',
                            'sales': j_goods_item.find('div', attrs={"class": "p-commit"})
                            .find('strong').find('a').string.strip(),
                            'belong': 'jd'
                        }
                        search_result.append(j_goods)
            else:
                message.error_message('没有搜索到商品')
        except (error.HTTPError, error.URLError, error.ContentTooShortError):
            message.error_message()
        except UnicodeEncodeError:
            message.error_message('encoding error')
        finally:
            return search_result

import ssl
from urllib import request, error, parse
from colorama import Fore
from bs4 import BeautifulSoup
from utils import message
from pprint import pprint

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

    def fetch_jd_goods(self):
        print(message.colorful_text('fetching goods from jd....', color=Fore.RED))
        search_result = None
        try:
            print(self.url)
            req = request.Request(self.url, headers=self.headers)
            response = request.urlopen(req).read().decode('UTF-8')

            # with open('./jd/jd_skirt.htm', encoding='utf-8') as f:
            #     response = f.read()

            soup = BeautifulSoup(response, 'lxml')
            j_goods_list = soup.find('div', id="J_goodsList").find_all('li', attrs={"class": "gl-item"})
            # with open('./jd/jd_html.html', 'w') as f:
            #     f.write(j_goods_list)
            pprint(j_goods_list)
            if j_goods_list:
                # print(len(j_goods_list))
                search_result = []
                for index, j_goods_item in enumerate(j_goods_list):
                    if j_goods_item.find('div', attrs={"class": "p-img"}):
                        if index == 4:
                            print(j_goods_item)
                            # print(index)
                            # print(j_goods_item.find('div', attrs={"class": "p-img"}).a.attrs["href"])
                            # print(j_goods_item.find('div', attrs={"class": "p-name"}).a.attrs["title"])
                            # print(j_goods_item.find('div', attrs={"class": "p-price"})
                            #       .find('strong').attrs["data-price"])
                            # p_commint = j_goods_item.find('div', attrs={"class": "p-commit"})
                            # print(p_commint)
                            # print(p_commint.find('strong'))
                            # print(p_commint.find('strong').find('a'))
                            # print(p_commint.find('strong').find('a').string.strip())
                        j_goods = {
                            'index': index,
                            'url': j_goods_item.find('div', attrs={"class": "p-img"}).a.attrs["href"],
                            'intro': j_goods_item.find('div', attrs={"class": "p-name"}).a.attrs["title"],
                            'price': j_goods_item.find('div', attrs={"class": "p-price"})
                            .find('strong').attrs["data-price"]
                            if j_goods_item.find('div', attrs={"class": "p-price"})
                            .find('strong').attrs["data-price"] else '0.00',
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

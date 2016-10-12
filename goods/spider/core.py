from .spider_jd import JdSpider
from .spider_taobao import TaobaoSpider
from ..utils.const_value import WEB_NAME


def fetch_goods(keywords, web):
    if web not in WEB_NAME['all']:
        return []
    spider = {
        'jd': JdSpider,
        'taobao': TaobaoSpider
    }
    return spider[web](keywords).goods

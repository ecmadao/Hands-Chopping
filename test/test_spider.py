import random
from goods.spider.core import fetch_goods

GOODS = ('冰与火之歌', '权力的游戏', '移动硬盘-东芝', '海贼王',
         'python', 'psv', 'ps4-港版', 'iphone6-32G-港版')


def convert_keywords(keywords):
    goods_keywords = keywords.split('-')
    assert isinstance(goods_keywords, list)
    key_words = '+'.join(goods_keywords)
    return key_words


def test_get_goods():
    random_index = random.randrange(0, len(GOODS))
    assert random_index < len(GOODS)
    goods = GOODS[random_index]
    assert goods in GOODS
    return convert_keywords(goods)


def get_goods(keywords, web):
    return fetch_goods(keywords, web)


# def test_taobao():
#     goods = test_get_goods()
#     result = fetch_goods(goods, 'taobao')
#     assert result is not None
#     assert len(result) > 1
#
#
# def test_jd():
#     goods = test_get_goods()
#     result = fetch_goods(goods, 'jd')
#     assert result is not None
#     assert len(result) > 1

## Hands-Chopping 剁手党

作为剁手党，必须得有个方便的工具来愉快的剁手~

### Rely

python 3.5+

[click](http://click.pocoo.org/6)

[prettytable](https://pypi.python.org/pypi/PrettyTable)

[bs4](https://pypi.python.org/pypi/beautifulsoup4)

[selenium](www.seleniumhq.org/)

### Install

**通过pip3**

```bash
$ sudo pip3 install hands_chopping
```

**或者本地安装**

```bash
$ git clone https://github.com/ecmadao/Hands-Chopping
$ cd Hands-Chopping-master
$ sudo python3 setup.py install
```

### Usage

```bash
$ goods
# example
$ goods —site=jd # 仅搜索京东
$ goods —site=tb # 仅搜索淘宝
```

### Help

```python
Usage:
    $ goods [--site= all | jd | tb]

Options:
    --site: 要搜索的网站，jd-京东，tb-淘宝，默认全部

Examples:
    $ goods --site=jd
    $ goods
```

### Notes

- 目前支持淘宝/京东的搜索
- 输入goods会提示输入关键字，多个关键字之间使用空格分隔
- 搜索完成后可进入下一步操作，根据提示，输入商品编号。多个编号间使用`,`链接，则可打开浏览器窗口进入到商品详情页

### TODO

- [x] ~~测试得加上，目前CI一直爆。但仅仅因为没有测试，实际没有影响~~
- [ ] 商品排序(按照金额等)
- [ ] 现阶段只抓取了第一页的商品。之后考虑抓取多页
- [ ] more unittest
- [ ] 容错
  - [ ] 没有数据
  - [ ] 数据结构有变
- [ ] 更多配置
  - [ ] 爬取速度
  - [ ] 爬取页数

## Hands-Chopping 剁手党

作为剁手党，必须得有个方便的工具来愉快的剁手~

### Rely

python 3.5+

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
$ goods [想要搜索的商品关键字，各个关键字之间使用-链接]
# example
$ goods psp
# $ goods psp-港版
# $ goods -j psp 仅搜索京东
# $ goods -t psp 仅搜索淘宝
```

![search psp](./example.png)

### Help

```python
Usage:
    goods [-j | -t] <goods>

Options:
    -h --help  显示帮助菜单
    -goods     关键字
    -j         京东
    -t         淘宝

Examples:
    goods 移动硬盘
    goods -j 移动硬盘
    goods 硬盘-东芝
```

### Notes

- 目前支持淘宝/京东的搜索
- 搜索完成后可进入下一步操作，根据提示，输入商品编号。多个编号间使用`,`链接，则可打开浏览器窗口进入到商品详情页

### TODO

- 测试得加上，目前CI一直爆。但仅仅因为没有测试，实际没有影响
- 商品排序(按照金额等)
- 现阶段只抓取了第一页的商品。之后考虑抓取多页
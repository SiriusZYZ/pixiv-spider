
[English Intro](<#pixiv-spider [en]>)  
[简体中文简介](<#pixiv-spider [zh-cn]>)  
[changelog](<#changelog>)  
[future plan](<#future-plan>)  
Contact me at `sirius.zhouyz@gmail.com`, your feedbacks will be appreciated.

# pixiv-spider [en]
Fetch contents from pixiv.  
This module is still **under development**. Supported features includes:
- fetch the title, `illustid`, date, tags, author and other metadata of the listed artworks in [trending page](https://www.pixiv.net/ranking.php). 
- given the `illustid` of an artwork, fetch the art content url (original size).

>**Notice:**  
This module may be refactored in the future. The names of defined objects and methods may change.

## Dependencies
This module use `requests`. Nothing third-party else (Currently).  
Use the following command in your CLI to install `requests`.
```shell
pip install requests
```

## How to Use

1. import the module from `./pixivSpider`. You can rename this module in your project later if you want.
```python
import pixivSpider
```

2. Use `pixivSpider.rankingSession` to fetch stuff from the [trending page](https://www.pixiv.net/ranking.php).
```python
rs = pixivSpider.rankingSession()
rs.set_proxies(7890)    # if needed. apply for both http and https.

valid_modes = ("", "daily", "weekly", "monthly", "rookie")
valid_contents = ("", "illust", "ugoira", "manga")
rs.get_ranking_page(
    mode = "",          # Optional parameter.
    content = "illust", # Optional parameter.
    date = "20240101",  # Optional parameter. format (YearMonthDay)
    page = 1            # Optional parameter. each page has 50 artworks, pageNum starts from 1.
)   # see help(pixivSpider.rankingSession) for more info
rs.get_ranking_page(
    mode = "",          
    content = "illust", 
    date = "20240101",  
    page = 2
)

print(rs.log)           # show log
for idx, item in enumerate(rs.resolve()):   # .resolve() return the fetched results in a list of item dict.
    print(idx, item)

rs.reset()              # reset proxy setting and clear all the result.
```
3. Use `pixivSpider.illustpageSession` to fetch the url of original-size images from a given `illustid`
```python
ips = pixivSpider.illustpageSession()
ips.set_proxies(7890)

ips.get_illust_page(
    illust_id = 84421525    # https://www.pixiv.net/artworks/{illustid}
)
ips.get_illust_page(
    illust_id = 93341155
)

for idx, item in enumerate(ips.resolve()):   # .resolve() return the fetched results in a list of item dict.
    print(idx, item)
ips.reset()     # reset proxy setting and clear all the result.
``` 

# pixiv-spider [zh-cn]
抓取 pixiv 内容   
目前模块仍在**开发中**, 支持的功能如下:
- 抓取[排行榜](https://www.pixiv.net/ranking.php)中艺术作品的标题, `illustid`, 日期, 标签, 作者等元数据
- 抓取指定`illustid`艺术作品的原图url

>**注意:**  
模块可能会进行重构, 各定义的对象及方法名也可能因此改变.

## 依赖
目前只用到了`requests` 第三方模块.  
使用以下命令行命令安装:
```shell
pip install requests
```
## 使用方式

1. 从 `./pixivSpider`中导入模块. 如果需要可以在自己的项目中更改此模块名
```python
import pixivSpider
```

2. 使用 `pixivSpider.rankingSession` 获取[排行榜](https://www.pixiv.net/ranking.php)中的内容.
```python
rs = pixivSpider.rankingSession()
rs.set_proxies(7890)    # 设置proxy, 面向http和https

valid_modes = ("", "daily", "weekly", "monthly", "rookie")
valid_contents = ("", "illust", "ugoira", "manga")
rs.get_ranking_page(
    mode = "",          # 可选参数.
    content = "illust", # 可选参数.
    date = "20240101",  # 可选参数. 格式为 (年月日)
    page = 1            # 可选参数. 每页50个作品, 页面数从1开始.
)   # 更多信息请 help(pixivSpider.rankingSession)
rs.get_ranking_page(
    mode = "",          
    content = "illust", 
    date = "20240101",  
    page = 2
)

print(rs.log)           # 打印log
for idx, item in enumerate(rs.resolve()):   # .resolve() 以列表形式返回爬取到的所有结果, 列表中每一个dict对应一个列出的作品
    print(idx, item)

rs.reset()              # 重置proxy设置并清空结果
```
3. 使用 `pixivSpider.illustpageSession` 来获取 `illustid` 作品的所有原始大小图片url
```python
ips = pixivSpider.illustpageSession()
ips.set_proxies(7890)

ips.get_illust_page(
    illust_id = 84421525    # https://www.pixiv.net/artworks/{illustid}
)
ips.get_illust_page(
    illust_id = 93341155
)

for idx, item in enumerate(ips.resolve()):   # .resolve() 以列表形式返回爬取到的所有结果, 列表中每一个dict对应一个执行过的每一个illust_id
    print(idx, item)
ips.reset()             # 重置proxy设置并清空结果
``` 

# Changelog
> **0.2.0** &emsp; 2024 Apr 7  
> - change this repo development from scrips-oriented to module-oriented.
> - api changes. add `rankingSession`, `illustpageSession` to support different features.
> - add a demo.
> - `README.md` support English now.
> - archived `digest.py`

> 0.1.2 &emsp; 2020 Mar 25   
> - fix possible AttributeError when using CLI.
  
> 0.1.1 &emsp; 2020 Mar 19   
> - `digest.py` support socks now. 

> 0.1.0 &emsp; 2020 Mar 18   
> - repo base.

# Future Plan
- support new trending sub-pages for original, ai-generate content, popular in male/female.
- add a downloader.
- add resolvers for [a single artist](https://www.pixiv.net/users/11) and [a single tag](https://www.pixiv.net/tags/%E3%82%A4%E3%83%A9%E3%82%B9%E3%83%88).
- better logs
# pixiv-spider🕷
📣 &emsp;**Working on engish version**  
📣 &emsp;**对于中国大陆用户需要带Socks的科学上网方式** 
<br> <br> 
<small>README最后更新: 2020/03/25 GMT+8 17:05 </small><br>
<small>by siriuslalalala</small><br>
<small>版本 :&emsp;0.1.2</small><br>
<br>
目录
* [🔐依赖](#依赖)
* [📃简介](#简介)
* [🍴使用方法](#使用方法)
* [❗注意事项](#注意事项)
* [✏用户自定义](#用户自定义)
* [🧾更新日志](#更新日志)
* [📈未来计划](#未来计划)
* [☕chat](#chat)


## 🔐依赖
-----------------------
Python 3.6.5 及以上  
1.  使用Socks代理时需要 PySocks  
安装 PySocks:
```
 pip install PySocks
```
1. 在改装&nbsp;`digest.py`&nbsp;令其可以保存爬取结果至本地`csv`时需要pandas：  
安装pandas:
```
 pip install pandas
```
<div align="right"><a href ='#pixiv-spider'>🔝</a></div>  

##  📃简介 
-----------------------
适用于 Python3   
**无登录**&nbsp;状态爬取pixiv榜单,并多线程下载榜单中所有图片(包含多页漫画)  

+  内容分类
    *  综合
    *  插画
    *  漫画  
<br>  

+  模式分类  
&emsp;⚠某些模式可能在特定内容下不可用
    *  每日
    *  每周
    *  每月  
    *  新人
    *  原创
    *  受男性欢迎
    *  受女性欢迎

+ 页面日期  
&emsp;支持从 <kdb>2010-11-01</kdb>到现时（但不是当天）的页面爬取  
<br> 
<div align="right"><a href ='#pixiv-spider'>🔝</a></div>    

##  🍴使用方法 
----------------------- 
```python
python digest.py
```
<br> 
<div align="right"><a href ='#pixiv-spider'>🔝</a></div>  

##  ❗注意事项   
-----------------------   
1.  请先将&emsp; **digest.py** &emsp;放在一个&nbsp;**独立的文件夹**&nbsp;中运行，并赋予其运行权限。
2.  在proxy设置中，如果你使用shadowsocks,端口可能为1080，如果你使用V2rayN，端口可能为10808。
3.  直接使用全局路由时请不要设置代理。
4.  因为 **没有写登录** 所以没有办法爬🔞 ~~各位选模式时选男性将就下~~
5.  有同名覆写问题，正在维修
<br>
<div align="right"><a href ='#pixiv-spider'>🔝</a></div> 

## ✏用户自定义
---------------------
修改于 `digest.py` 中位于代码头的全局变量：

| 变量             | 用途                  | 变量类型 | 初始值 |
| :--------------- | :-------------------- | :------: | :----: |
| RESOLVE_THREAD   | 解析url线程数         |   int    |   10   |
| DOWNLOAD_THREADS | 下载图片线程数        |   int    |   15   |
| DOWNLOAD_ALL     | 下载漫画所有页/仅封面 |   bool   |  True  |
| SEPARATE_FOLDER  | 是否独立存放每本漫画  |   bool   |  True  |
| DATA_PATH        | 储存所有数据基文件夹  |  string  | 'data' |
|DEFAULT_PROXY     | 默认Socks代理端口     |    int   |  1080  |

强烈建议: 令`DOWNLOAD_ALL`与`SEPARATE_FOLDER`设置相同的值 

<br>
<div align="right"><a href ='#pixiv-spider'>🔝</a></div>  





## 🧾更新日志
-------------
> <big>v 0.1.0</big>   
> ➕2020-03-18 GMT+8 21:26 &emsp;发布了 `digest.py`  
> 🔧2020-03-18 GMT+8 22:02 &emsp;`digest.py` 现在支持手动修改自定义设置了  
    
> <big>v 0.1.1</big>  
>🔧2020-03-19 GMT+8 10:01 &emsp;`digest.py` 现在支持Socks代理端口的设置了  

> <big>v 0.1.2</big>  
>🔧2020-03-25 GMT+8 17:00 &emsp;`digest.py` 修复了控制台下执行时可能出现的AttributeError
  
<div align="right"><a href ='#pixiv-spider'>🔝</a></div>  


## 📈未来计划 
-----------
+ 改成英语版本   
✅ 支持Socks代理  
+ 支持登录?  
+ 写好保存csv支持  
+ 更好的Exception支持 
+ 🐞[b000001]防止同名覆写
+ 爬取画师所有作品功能
<div align="right"><a href ='#pixiv-spider'>🔝</a></div>  

## ☕chat
-------------
没什么经验，请多多批评

<div align="right"><a href ='#pixiv-spider'>🔝</a></div> 
 


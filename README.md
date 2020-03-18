# pixiv-spider🕷
📣 &emsp;**English version on progress 2020-March-18**  
📣 &emsp;**对于中国大陆用户需要带全局路由的科学上网方式** 
<br> <br> 
<small>最近更新: 2020/03/18 10:00 pm</small><br>
<small>by siriuslalalala</small><br>
<small>版本 :&emsp;0.1</small><br>

##  简介 
-----------------------
适用于 Python3   
**无登录**&nbsp;状态爬取pixiv榜单,并多线程下载榜单中所有图片(包含漫画)  

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

##  使用方法 
----------------------- 
```python
python digest.py
```
<br> 

##  注意事项   
-----------------------   
1. 请先将&emsp; **digest.py** &emsp;放在一个&nbsp;**独立的文件夹**&nbsp;中运行，并赋予其运行权限
2. 将你的科学上网方式设置为全局模式(global)
3. 因为没有写登录所以没有办法爬🔞 ~~各位同学模式选男性将就下~~
<br>

## 用户自定义
---------------------
修改于 `digest.py` 中位于代码头的全局变量：  
  

 + `RESOLVE_THREAD` = 10     &emsp;&emsp;解析线程数
 + `DOWNLOAD_THREADS` = 15   &emsp;&emsp;下载图片线程数
 + `DOWNLOAD_ALL` = True     &emsp;&emsp;下载漫画中的所有页(True),只下载封面(False)
 + `SEPARATE_FOLDER` = True  &emsp;&emsp;将同属一个漫画的保存在同一文件夹下，推荐使用`DOWNLOAD_ALL`相同的设置
 + `DATA_PATH` = 'data'&emsp;&emsp;储存所有爬取数据的文件夹名

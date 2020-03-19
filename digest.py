import os,re,html,time,concurrent
import urllib.request as req

#config
RESOLVE_THREADS = 10            #解析地址线程数，过多导致电脑变卡，太少解析变慢
DOWNLOAD_THREADS = 15           #下载图片线程数，同上
DOWNLOAD_ALL = True   #False    #对漫画下载全部或者仅封面（多于一页的插画视为漫画）
SEPARATE_FOLDER = True #False   #以文件夹保存漫画,推荐与DOWNLOAD_ALL设置相同值
DATA_PATH = 'data'              #保存所有爬取数据的文件夹
DEFAULT_PROXY = 1080           #默认socks代理端口
#

'''
#modify the scripts if you want to save the result of Dig() as .csv:
import pandas as pd  
def Save_csv(dic,work_path):
    
    csv_path = os.path.join(work_path,'pixiv.csv')
    pd.DataFrame(dic).to_csv(csv_path,encoding='utf-8') 
    return csv_path
'''

def ns_time(ns):
    
    '''
    conver ns to time
    '''

    s = ns/10**9
    if s < 0.1: return '<0.1s'
    if s//60:
        m = s//60
        s = s % 60

        if m//60:
            h = m//60
            m = m % 60
            return '{:0.0f}h {:1.0f}m {:2.0f}s'.format(h,m,s)
        else:   return '{:0.0f}m {:1.1f}s'.format(m,s)
    else:   return '%.2fs' % s  


def time_stamp():

    '''
    return local time in string:'YYYY-MM-DD' 
    '''

    return time.strftime("%Y-%m-%d", time.localtime())


def Fetch_html(url,store_path,folder_name):
    '''
    fetch html on the target url, and place it as 'pixiv.html' under store_path.
    return the path of the dir and html, seperately. 
    '''
    #info
    s = time.time_ns()
    print('[info] fetch html: start')
    print('[info] fetch html: url='+ url)
    current_path = os.path.join(store_path,folder_name)                    #dir 
    current_html = os.path.join(current_path,'pixiv.html')        

    #make dir
    if not os.path.isdir(current_path):                                     #create dir with time labled name, if not exist
        print("[info] fetch html: makedir: "+ current_path)
              
        os.makedirs(current_path)
    else:
        print('[info] fetch html: dir '+ current_path+' exists, move on')
    
    #info
    print('[info] fetch html: fetch')
  
    #build request headers
    opener=req.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    req.install_opener(opener)

    #download html
    try:
        r = req.urlopen(url,timeout= 10)
        #print('[info] fetch html: html headers:',r.headers )
    except ValueError as e:
        print('[Error] fetch html: ',e )
        return -1
    except req.HTTPError as e:
        print('[Error] fetch html: ',e )
        return -1
    except req.URLError as e:
        print('[Error] fetch html: ',e)
        print('[info] fetch html: check your Internet connection or proxy setting ')
        return -1
        

    #write to local file
    file = open(current_html, 'wb') 
    try:
        file.write(r.read())
        print('[info] fetch html: html saved as '+current_html )
    except :
        print('[Error] fetch html: Exception occured when trying to write .html'+ e)
    file.close()

    
    #info
    print('[info] fetch html: finish (%s)' % ns_time(time.time_ns()-s))

    #return folder path, file path
    return current_path,current_html


def Dig(html_path):
    
    '''
    find elements in the html, return [{},..]
    '''
    #info
    s = time.time_ns()
    print('[info] Dig: start')
    print('[info] Dig: read html on ',html_path)
    
    #read html into memory
    try:
        file = open(html_path,mode='r',encoding='utf-8')
        script = file.read()                    #whole html
        file.close()
    except :
        print('[Error] Dig: attempted to read html, but failed')
        return [{},]

    #match html labels
    print('[info] Dig: match html labels')
    ul_level = re.findall(r'''<section id="(.*?)</section>''',script,re.S|re.M)

    rank_dict = []

    for i in ul_level:
        card = {}
        h2_level = re.findall(r'''<h2>(.*?)</h2>''',i,re.S|re.M).pop()

        card['rank'] = int(re.findall(r'''data-rank="(.*?)"''',i,re.S|re.M).pop())
        card['title'] = html.unescape(re.findall(r'''data-title="(.*?)"''',i,re.S|re.M).pop())
        card['date'] = re.findall(r'''data-date="(.*?)"''',i,re.S|re.M).pop()   
        card['author'] = re.findall(r'''data-user-name="(.*?)"''',i,re.S|re.M).pop()
        card['multiple'] = bool(re.search(r'''multiple''',i,re.S|re.M))
        
        #if there are multiple pages
        try:
            #pages_level = re.findall(r'''<div class="page-count">(.*?)</a>''',i,re.S|re.M).pop()
            card['pages'] = int(re.findall(r'''<span>(.*?)</span>''',i,re.S|re.M).pop())
        except:
            card['pages'] = 1
        
        card['webpage_url'] = r'https://www.pixiv.net'+ re.findall(r'''<a href="(.*?)"''',h2_level,re.S|re.M).pop()

        rank_dict.append(card)
    
    #info
    print('[info] Dig: %d units found' % len(rank_dict))
    print('[info] Dig: finish (%s)' % ns_time(time.time_ns()-s))

    
    return rank_dict


def Book(rank,image_path,pool_size,download_multiple, separate_folder):
    
    '''
    resolve image urls from [rank], and return [{'Referer':,'img_url':,'path':},..] as download tasks queue.
    if separate_folder is true, make dirs for the manga pages. 
    '''

    s = time.time_ns()
    finish = [0]
    bar_length = 30
    work = len(rank)

    #resolver 
    def resolvor(url,title,path,num = 1):
        
        #fetch webpage
        try:
            webpage = req.urlopen(url).read().decode('utf-8')
        except:
            return {'state':-1,'url':url,'content':None}

        #find image url
        img_url_style = re.findall(r'''"original":"(.*?)"''',webpage,re.S|re.M).pop()   #the common style of pics in this page

        img_bundle = []

        #form a task dict, and append to the img_bundle
        for i in range(num):
            wrapper = {}
            wrapper['Referer'] = url #fake headers
            wrapper['img_url'] = re.sub(r'''_p(.*?).''','_p'+str(i),img_url_style) #compile url
            
            image_suffix = os.path.splitext(wrapper['img_url'])[1]      #后缀名

            #if resolve 1 image, then dont add any index. else, add index
            index =  '' if num == 1 else ('-p'+ str(i))                 
            name = title + index + image_suffix

            wrapper['path'] = os.path.join(path,name)

            img_bundle.append(wrapper)

        return {'state':1,'url':url,'content':img_bundle}
    

    #callback function
    def R_Callback(res):
        res = res.result()
        finish[0] += 1
        if res['state'] == -1: print('[Error] Book task: resolve failed on ',res['url'])
        else: book.extend(res['content'])


    #info
    print('[info] Book: start')
    print('[info] Book: save images at :',image_path)

    if download_multiple:   print('[info] Book: resolve all pages of mangas')
    else:   print('[info] Book: only resolve cover of mangas ')
    
    if separate_folder: print('[info] Book: save mangas in separate folders under - ',image_path)
    else:   print('[info] Book: save all images in one folder - ',image_path)
    
    print('[info] Book: resolve')

    #build thread pool
    print('[info] Book: using',pool_size,'threads')
    resolve_pool = concurrent.futures.ThreadPoolExecutor(10)

    book=[]
    

    #resolve all unit in rank
    for i in rank: 

        url = i['webpage_url']
        title =  re.sub(r'[\\/*<>|?:]','-','-'.join((i['title'],i['author']))) 
        
        #only when download_multiple is true, we download all images in the pages with multiple images
        num = i['pages'] if download_multiple else 1

        #only when download_multiple and seperate_file are both true, as well as resolving a page with multiple images, we update path
        path = title if (separate_folder and download_multiple and bool(num-1)) else ''
        path = os.path.join(image_path,path)
        if bool(path) and not os.path.isdir(path):
            os.makedirs(path)
          
        resolve_pool.submit(resolvor,url,title,path,num).add_done_callback(R_Callback)
        #time.sleep(0.001)
    
    
    #visualize
    while(True):
        finish_bar = int(finish[0]*bar_length/work)
        print('\r[info] Book: [{0:}{1:}] {2:}/{3:} | {4:}'.format(finish_bar*'>',
                                                                  (bar_length-finish_bar)*'-',
                                                                  finish[0],
                                                                  work,
                                                                  ns_time(time.time_ns()-s)),
                                                                  end = '')
        if finish[0] == work:
            break
        time.sleep(0.1)
        

    resolve_pool.shutdown(wait=True)
    print('')
    #info
    print('[info] Book: resolved {0:d}urls'.format(len(book)))
    print('[info] Book: finish (%s)' % ns_time(time.time_ns()-s))

    return book


def Download_task(book,pool_size = 10):
    
    '''
    Download tasks in book[{},..], see function: Book
    '''

    s = time.time_ns()
    state = {'finish':0,'failed':0}
    bar_length = 30
    work = len(book)
    fail_info = []

    #info
    print('[info] Download: start')
    

    #callback function, visualize)
    def D_Callback(res):
        res = res.result()
        state['finish'] += 1
        if res == 0:    state['failed'] += 1


    def Downlaoder(bundle):
        
        #info
        #print('[INFO] Downloader: ',bundle['path'])

        #load infomation
        referer = bundle['Referer']
        url = bundle['img_url']
        path = bundle['path']

        #fake headers    
        opener=req.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'),('Referer',referer)]
        req.install_opener(opener)
        
        #fetch image
        try:
            r = req.urlopen(url,timeout= 30)
            #print('\n[info] loader: size: {:.2f}KB',r.headers['Content-Length']/1024 )
        except:
            #URLError, HTTPError, timeout, etc
            fail_info.append('[Connection Failed]: URL={}, Path={} '.format(url,path))
            return 0

        file = open(path, 'wb') 
        try:
            file.write(r.read())
            file.close()   
            return 1
        except:
            #maybe it's an IOError
            file.close()
            fail_info.append('[Connection Failed]: Path={}, URL={} '.format(path,url))
            return 0


    #create thread pool
    print('[info] Download: using',pool_size,'threads')   
    download_pool = concurrent.futures.ThreadPoolExecutor(pool_size)    #create thread pool
    book_length = len(book)
    print('[info] Download: download %d units' % book_length)
    
    #form queue
    print('[info] Download: download')
    for i in book:
        download_pool.submit(Downlaoder,i).add_done_callback(D_Callback)
        time.sleep(0.001)
    
    #visualize
    s1 = time.time_ns()
    while True:
        finish_bar = int(state['finish']*bar_length/work)
        print('\r[info] Download: [{0:}{1:}] {2:}/{3:} | {4:} Failed | {5:}'.format(finish_bar*'>',
                                                                                (bar_length-finish_bar)*'-',
                                                                                state['finish'],
                                                                                work,
                                                                                state['failed'],
                                                                                ns_time(time.time_ns()-s1)),
                                                                                end = '')
        
        if state['finish'] == work:
            break

        time.sleep(0.1)
    print('')

    for i in fail_info:
        print('[info] Download: '+i)

    print('[info] Download: finish (%s)' % ns_time(time.time_ns()-s))
    download_pool.shutdown(wait=True)


def url_former(mode,content,date):
    
    '''
    recieve 'mode', 'content', 'date', compile them as a url
    '''

    url = r'https://www.pixiv.net/ranking.php'
    tail = []


    if mode   : tail.append('mode='+mode)
    if content: tail.append('content='+content)
    if date:    tail.append('date='+date)   

    return url+'?'+'&'.join(tail)    


def ask_url():
    
    '''
    dont play with this, it tries to understand what your need
    '''

    #translate
    con_trans_zh   = {'normal':'综合','illust':'插画','manga':'漫画'}
    mode_trans_zh  = {'daily':'每日','weekly':'每周','monthly':'每月','rookie':'新人','original':'原创','male':'男性','female':'女性'}
    
    #config
    con_list    = ('normal','illust','manga')
    mode_list   = {'normal':('daily','weekly','monthly','rookie','original','male','female'),
                   'illust':('daily','weekly','monthly','rookie'),
                   'manga' :('daily','weekly','monthly','rookie')}


    #ask
    print('-------爬取内容-------')
    for i, element in enumerate(con_list):
        print(i+1, con_trans_zh[element])
    print('')
    while(True):
        try:
            option = int(input('认真选择: '))
            if 1 <= option <= len(con_list):
                content = con_list[option-1]
                break
            else: continue
        except:
            continue
    
    print('\n\n-------爬取模式-------')
    for i, element in enumerate(mode_list[content]):
        print(i+1, mode_trans_zh[element])
    print('')
    while(True):
        try:
            option = int(input('认真选择: '))
            if 1 <= option <= len(mode_list[content]):
                mode = mode_list[content][option-1]
                break
            else: continue
        except:
            continue

    
    date_now = time.strftime("%Y%m%d", time.localtime())
    print('\n\n-------页面日期-------')
    print('格式:20200202(YYYYMMDD)')
    print('日期要在2010-11-01之后,'+'当日(日本时间)之前')
    print('回车直接获取现时榜单\n')
    while(True):
        option = input('认真输入: ')
        if option == '': 
            date = None
            break
        try:
            if 20101101 <= int(option) < int(date_now) and time.strptime(option,"%Y%m%d") :           
                date = option
                break
        except:
            pass
    
    if content == 'normal': content = None
    return mode,content,date
    

def demo():
    
    '''
    demo
    '''

    #setup socks
    p = input('使用Socks代理?(注意:大陆用户不使用代理无法连接pixiv)[y/n]')
    if p == 'y' or p == 'Y':
        try:
            import socks
            import socket
            print('在你的科学上网中查找代理端口(ss)/监听端口(v2ray)')
            proxy = input('键入Socks代理端口(默认 %d ):' % DEFAULT_PROXY)
            try:
                proxy = int(proxy)
            except:
                proxy = DEFAULT_PROXY
                print('设置为 %d ' % DEFAULT_PROXY)
            
            socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', proxy)
            socket.socket = socks.socksocket

        except:
            print('请先安装PySocks cmd:[ pip install PySocks]')
            
            
    

    #customize url
    mode,content,date = ask_url()
    URL = url_former(mode,content,date)
    
    #record time
    main_s = time.time_ns()
    
    #info
    print('[info] main: url='+ URL)
    print('[info] main: start'+ URL)

    #fetch html
    folder_date = (date if date else time.strftime("%Y%m%d", time.localtime()))
    folder_name = '-'.join((folder_date,content if content else '',mode))
    result = Fetch_html(URL,DATA_PATH,folder_name)
    #if Fatal error
    if result == -1: return 
    else:   WORK_PATH, HTML_PATH = result
    
    #match html labels,save as [{},]
    rank_dict = Dig(HTML_PATH)

    #resovle url to get pics
    book = Book(rank_dict,os.path.join(WORK_PATH,'image'),RESOLVE_THREADS,DOWNLOAD_ALL,SEPARATE_FOLDER)
    
    #download via book
    Download_task(book,DOWNLOAD_THREADS)

    #info
    print('[info] main: finish (%s)' % ns_time(time.time_ns()-main_s))


if __name__ == "__main__":
    
    demo()

    

    

import os, re, html, time
import requests
from typing import Optional, List
import json


class baseSession:

    def __init__(self):
        
        self._log = ""
        self._log_on = True
        self._session = requests.Session()
        self._retry = 3
        self.reset()

    def write_log(func):
        def wrapper(self, *args, **kwargs):
            ret = func(self, *args, **kwargs)
            if self._log_on : self._log += ret + "\n"
            return ret
        return wrapper

    @write_log
    def message(self, msg: str) -> str:
        return msg
    
    @write_log
    def set_proxies(self, port : int) -> str:
        assert port > 0
        self._session.proxies = {
            "http": "http://127.0.0.1:" + str(port),
            "https": "http://127.0.0.1:" + str(port)
        }
        return "[Config] Set proxies port = " + str(port)

    @write_log
    def reset(self) -> str:
        self._session = requests.Session()        
        self._session.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36'}
        self._session.proxies = dict()
        self._retry = 3
        return "[Config] Reset"

    @property
    def retry(self) -> int:
        return self._retry
    
    @retry.setter
    def retry(self, retry_times : int):
        assert retry_times > 0
        self._retry = retry_times
    
    @property
    def log(self) -> str:
        return self._log[:]
    
    @property
    def log_on(self):
        return self.log_on
    
    @log_on.setter
    def log_on(self, on : bool):
        self.log_on = on

    @write_log
    def test_connection(self, url : str = "https://www.pixiv.net") -> str:
        
        t = time.time()
        response = self.__session.get(url, timeout = 5)
        t = int(1000 * (time.time() - t))
        return "[Action] Test Connection on {:}, Response Status: {:} | {:}ms".format(url, response.status_code, t)

    def open(self, url : str, referer : Optional[str] = "") -> Optional[requests.models.Response]:
        if referer:
            self._session.headers['refere'] = referer
        
        times = 0
        while times < self._retry:
            t = time.time()
            try:
                response = self._session.get(url)
            except (requests.exception.ConnectTimeout, requests.exception.ProxyError, requests.exception.SSLError) as E:
                self.message("[Action] Resolve {:} | {:}".format(url, E))
            except:
                self.message("[Action] Resolve {:} | Unexpected Error.".format(url))
            else:
                t = int(1000 * (time.time() - t))
                self.message("[Action] Resolve {:} | Response Status: {:} | {:}ms".format(url, response.status_code, t))
                if response.status_code not in (200, 201, 302, 304):
                    continue
                else: break

            times += 1
            self.message("[Action] Resolve {:} | Rretry Times {:}".format(url, times))

        if response: return response
        
class rankingSession(baseSession):
    def __init__(self):
        super().__init__()
        self.res = list()
    
    def write_log(func):
        def wrapper(self, *args, **kwargs):
            ret = func(self, *args, **kwargs)
            if self._log_on : self._log += ret + "\n"
            return ret
        return wrapper

    def reset(self) -> str:
        super().reset()
        self.res = list()
        return "[Config] Reset"
    
    @write_log
    def get_ranking_page(self, mode : Optional[str] = "", content : Optional[str] = "", date : Optional[str] = "", page : Optional[int] = "") -> str:
        
        try:
            assert mode in ("", "daily", "weekly", "monthly", "rookie")
            assert content in ("", "illust", "ugoira", "manga")
        except AssertionError:
            return "[Action] Get Ranking Page\n[Abort] Invalid Parameters when calling get_ranking_page."
        
        base_url = r"https://www.pixiv.net/ranking.php?"
        suffix = []
        if mode: suffix.append("mode=" + mode)
        if content: suffix.append("content=" + content)
        if date: suffix.append("date=" + date)
        if page: suffix.append("p=" + str(page))
        suffix.append("format=json")

        request_url = base_url + '&'.join(suffix)

        r = self.open(request_url)
        if not r:
            return "[Action] Get Ranking Page on {:} | Failed."
        
        result = response.json()["contents"]

        self.res.extend(result)

        return "[Action] Get Ranking Page on {:} | {:} items found.".format(request_url, len(result))
    
    def resolve(self) -> list:

        self.message("[Action] Resolve, {:} items found.".format(len(self.res)))
        return self.res

class illustPageSession(baseSession):

    def __init__(self):
        super().__init__()
        self.res = list()
    
    def write_log(func):
        def wrapper(self, *args, **kwargs):
            ret = func(self, *args, **kwargs)
            if self._log_on : self._log += ret + "\n"
            return ret
        return wrapper

    def reset(self) -> str:
        super().reset()
        self.res = list()
        return "[Config] Reset"

    @write_log
    def get_illust_page(self, illust_id : int) -> str:

        url = "https://www.pixiv.net/ajax/illust/{:}/pages?lang=en".format(illust_id)

        r = self.open(url, referer = "https://www.pixiv.net/en/artworks/{:}".format(illust_id))
        if not r:
            return "[Action] Get Ranking Page on {:} | Failed."

        illust_page_dict = {"illust_id" : illust_id, "resolved_pics": list()}
        for pics in r.json()["body"]:
            illust_page_dict['resolved_pics'].append(pics["urls"]["original"])
        
        self.res.append(illust_page_dict)
        
        return "[Action] Get Illustwork on {:} | {:} pics found.".format(url, len(illust_page_dict['resolved_pics']))

    def resolve(self) -> list:

        self.message("[Action] Resolve, {:} items found.".format(len(self.res)))
        return self.res

        
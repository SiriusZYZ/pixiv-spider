
import time
import requests
from functools import wraps
from typing import Optional, List

class baseSession:
    '''
    A base class for utils. 
    It contains a requests.Session object and some basic functions, including log writing, setting proxies, reset session, open url, test connection, etc.
    '''
    def __init__(self):
        
        self._log = ""
        self._log_enable = True
        self._session = requests.Session()
        self._retry = 3
        self.message("[Action] Initialize baseSession")
        self.reset()

    def write_log(func):
        '''
        Decorator for log writing.
        '''
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            ret = func(self, *args, **kwargs)
            if self._log_enable and ret: self._log += time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+f"{time.time()%1:.3f} " + ret + "\n"
            return ret
        return wrapper

    @write_log
    def message(self, msg: str) -> str:
        '''
        Send message and write log.
        '''
        return msg
    
    @write_log
    def set_proxies(self, port : int) -> str:
        '''
        Set proxies explicitly.
        Parameters:
            port : int
                Port number for proxies.
        '''
        assert port > 0
        self._session.proxies = {
            "http": "http://127.0.0.1:" + str(port),
            "https": "http://127.0.0.1:" + str(port)
        }
        return "[Config] Set proxies port = " + str(port)

    @write_log
    def reset(self) -> str:
        '''
        Reset Session. This will clear all settings including headers, proxies and retry times.
        '''
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
    def log_is_enable(self):
        return self._log_enable

    @write_log
    def enable_log(self):
        self._log_enable = True
        return "[Config] Enable Log"

    @write_log
    def disable_log(self):
        self._log_enable = False
        return "[Config] Disable Log"

    @write_log
    def test_connection(self, url : str = "https://www.pixiv.net") -> str:
        '''
        Test connection to an url. default as pixiv main page.
        Parameters:
            url : str
                The url to test connection.
        '''
        self.message(f"[Action] Testing Connection on {url}")
        rp = self.open(url)

        if rp and rp.ok:
            return f"[Action] Test Connection on {url}, Response Status: {rp.status_code}"
        else: 
            return "[Error] Connection Failed."

    def open(self, url : str, referer : Optional[str] = "") -> Optional[requests.models.Response]:
        '''
        open an url and return its requests.models.Response.
        Parameters:
            url : str
                The url to open.
            referer : Optional[str]
                The referer of the url. defualt as "".
        '''
        
        if referer:
            self._session.headers['refere'] = referer
        
        self.message(f"[Action] Resolving {url}")

        times = 0
        while times < self._retry:
            t = time.time()
            try:
                response = self._session.get(url)
            except (requests.exception.ConnectTimeout, requests.exception.ProxyError, requests.exception.SSLError) as E:
                self.message(f"[Error] {E}: when resolving {url}")
            except:
                self.message(f"[Error] Unexpected Error occured when resolving {url}")
            else:
                t = int(1000 * (time.time() - t))
                self.message("[Action] {:} resolved | Response Status: {:} | {:}ms".format(url, response.status_code, t))
                if response.status_code not in (200, 201, 302, 304):
                    continue
                else: break

            times += 1
            self.message(f"[Action] Resolve {url} | at {times} retry")

        if response: return response


if __name__ == "__main__":
    print("This file contains cls baseSession")
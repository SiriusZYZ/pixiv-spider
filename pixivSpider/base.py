
import time
import requests
from functools import wraps
from typing import Optional, List
from .logger import Logger

class baseSession:
    '''
    A base class for utils. 
    It contains a requests.Session object and some basic functions, including log writing, setting proxies, reset session, open url, test connection, etc.
    '''
    def __init__(self):
        
        self.logger = Logger
        self._session = requests.Session()
        self._retry = 3
        self.logger.debug("%s initialized", self)
        self._session.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36'}
        self._session.proxies = dict()

    def set_proxies(self, port : int) -> None:
        '''
        Set proxies explicitly.
        Parameters:
            port : int
                Port number for proxies.
        '''
        if port < 0 or port > 65536 or type(port) != int:
            self.logger.error("Invalid port number: %s", port)
            return False

        self._session.proxies = {
            "http": "http://127.0.0.1:" + str(port),
            "https": "http://127.0.0.1:" + str(port)
        }
        self.logger.debug("Proxies set to %s", self._session.proxies)

        return

    def reset(self) -> None:
        '''
        Reset Session. This will clear all settings including headers, proxies and retry times.
        '''
        self._session = requests.Session()        
        self._session.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36'}
        self._session.proxies = dict()
        self._retry = 3
        self.logger.info("Session reset.")
        self.logger.debug("%s Reset\nHeaders: %s \nProxies: %s \nRetry: %s", self, self._session.headers, self._session.proxies, self._retry)
        return

    @property
    def retry(self) -> int:
        return self._retry
    
    @retry.setter
    def retry(self, retry_times : int):
        assert retry_times > 0
        self._retry = retry_times
        self.logger.debug("Retry times set to %d", self._retry)

    def test_connection(self, url : str = "https://www.pixiv.net") -> bool:
        '''
        Test connection to an url. default as pixiv main page.
        Parameters:
            url : str
                The url to test connection.
        '''
        self.logger.debug("Testing Connection on %s", url)
        rp = self.open(url)
        rtt = rp.elapsed.microseconds/1000

        if rp and rp.ok:
            self.logger.info("Connection Succeed, Status Code: %s, RTT: %d", rp.status_code, rtt)
            return True
        else:
            self.logger.error("Connection failed.")
            return False

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
            self._session.headers['referer'] = referer
        
        times = 0
        response = None
        while times < self._retry:
            t = time.time()
            try:
                response = self._session.get(url)
            except (requests.exceptions.ConnectTimeout, requests.exceptions.ProxyError, requests.exceptions.SSLError) as err:
                self.logger.error("%s occurred when resolving %s", err, url)
                self.logger.debug(
                    "Call: @%s.open() -> Url: %s, Error: %s, Attempt times: %d, Headers: %s, Proxies: %s", 
                    self, url, err, times+1, self._session.headers, self._session.proxies)
            except Exception as err:
                self.logger.error("Unexpected %s occurred when resolving %s", err, url)
                self.logger.debug(
                    "Call: @%s.open() -> Url: %s, Error: %s, Attempt times: %d, Headers: %s, Proxies: %s",
                    self, url, err, times+1, self._session.headers, self._session.proxies)
            else:
                rtt = response.elapsed.microseconds/1000
                if response.ok:
                    self.logger.debug(
                        "Call: @%s.open() -> Url: %s, Status Code %s, RTT: %s",
                        self, url, response.status_code, rtt)
                    return response
                else:
                    self.logger.error("Connection failed.")
                    self.logger.debug(
                        "Call: @%s.open() -> Url: %s, Status Code %s, RTT: %s", 
                        self, url, response.status_code, rtt)
            times += 1
            self.logger.info("retry %d", times)


        self.logger.error("Failed to open %s after %d attempts.", url, self._retry)
        return None


if __name__ == "__main__":
    print("This file contains cls baseSession")
from typing import List, Optional
import requests
from .base import baseSession

class rankingSession(baseSession):
    '''
    This class is a subclass of baseSession. It is designed to resolve pixiv's (pixiv.net/ranking) and get illustration items.
    '''
    def __init__(self):
        super().__init__()
        self.res = list()
    
    def write_log(func):
        return baseSession.write_log(func)
    
    def reset(self) -> str:
        '''
        This will clear all settings including headers, proxies and retry times, and reset the result list.
        '''
        super().reset()
        self.res = list()
        return "[Config] Reset"
    
    @write_log
    def get_ranking_page(self, mode : Optional[str] = "", content : Optional[str] = "", date : Optional[str] = "", page : Optional[int] = "") -> str:
        '''
        This function will get ranking page from pixiv.net/ranking, resolve the page to a list of illustration items and append them to the result list.
        Parameters:
            mode : str
                Mode of ranking. Can be "daily", "weekly", "monthly", "rookie".
            content : str
                Content of ranking. Can be "illust", "ugoira", "manga".
            date : str
                Date of ranking. Format: "20210101".
            page : int
                The page number of ranking.
        Returns:
            str : The result of this action.
        '''
        self.message("[Action] Getting Ranking Page")
        try:
            assert mode in ("", "daily", "weekly", "monthly", "rookie")
            assert content in ("", "illust", "ugoira", "manga")
            assert not page or int(page) > 0
        except AssertionError:
            return "[Error] Invalid Parameters. Abort."
        
        base_url = r"https://www.pixiv.net/ranking.php?"
        suffix = []
        if mode: suffix.append("mode=" + mode)
        if content: suffix.append("content=" + content)
        if date: suffix.append("date=" + date)
        if page: suffix.append("p=" + str(page))
        suffix.append("format=json")

        request_url = base_url + '&'.join(suffix)
        self.message(f"[Action] Getting Ranking Page on {request_url}")
        r = self.open(request_url)
        if not r or not r.ok:
            return "[Error] Connection Failed. Abort."
        
        result = r.json()["contents"]

        self.res.extend(result)

        return "[Action] Get Ranking Page on {:} | {:} items found.".format(request_url, len(result))
    
    def resolve(self) -> list:
        '''
        This function returns the result list.
        Returns:
            list : The result list. Each item is a dict of illustration item.
        '''
        self.message("[Action] Resolve, {:} items found.".format(len(self.res)))
        return self.res


class illustPageSession(baseSession):
    '''
    This is a subclass of baseSession. It is designed to resolve the urls of illustration items based on a illustid.
    '''
    def __init__(self):
        super().__init__()
        self.res = list()
    
    def write_log(func):
        return baseSession.write_log(func)

    def reset(self) -> str:
        '''
        This will clear all settings including headers, proxies and retry times, and reset the result list.
        '''
        super().reset()
        self.res = list()
        return "[Config] Reset"

    @write_log
    def get_illust_page(self, illust_id : int) -> str:
        '''
        This function resolve the urls of illustration items based on a illustid.
        Parameters:
            illust_id : int
                The illust id of the illustration.
        Returns:
            str : The result of this action.
        '''
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
        '''
        This function returns the result list.
        Returns:
            list : The result list. Each item is a dict of illustration item.
        '''
        self.message("[Action] Resolve, {:} items found.".format(len(self.res)))
        return self.res
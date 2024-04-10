import time
import requests
from typing import List, Optional
from .base import baseSession

class rankingSession(baseSession):
    '''
    This class is a subclass of baseSession. It is designed to resolve pixiv's (pixiv.net/ranking) and get illustration items.
    '''
    valid_modes = ("", "daily", "weekly", "monthly", "rookie", "original", "daily_ai", "male", "female")
    valid_contents = ("", "illust", "ugoira", "manga")

    def __init__(self):
        super().__init__()
        self.res = list()

    
    def reset(self) -> None:
        '''
        This will clear all settings including headers, proxies and retry times, and reset the result list.
        '''
        super().reset()
        self.res = list()
        self.logger.debug("result list reset, cleared %d items.", len(self.res))
        return
    
    def get_ranking_page(self, mode : Optional[str] = "", content : Optional[str] = "", date : Optional[str] = "", page : Optional[int] = "") -> None:
        '''
        This function will get ranking page from pixiv.net/ranking, resolve the page to a list of illustration items and append them to the result list.
        Parameters:
            mode : str
                Mode of ranking. see rankingSession.valid_modes.
            content : str
                Content of ranking. see rankingSession.valid_contents.
            date : str
                Date of ranking. Format: "20210101".
            page : int
                The page number of ranking.
        Returns:
            str : The result of this action.
        '''
        self.logger.info("getting ranking page.")
        self.logger.debug(
            "%s getting ranking page, mode=%s, content=%s, date=%s, page=%s",
            self,
            mode if mode else 'None',
            content if content else 'None',
            date if date else 'None',
            page if page else 'None')

        try:
            if not mode in self.valid_modes: raise ValueError("Invalid mode")
            if not content in self.valid_contents: raise ValueError("Invalid content")
            if date:
                try:
                    ts_date = time.strptime(date, "%Y%m%d")
                except ValueError:
                    raise ValueError("Invalid date, check format [YYYYMMDD]")
                if ts_date > time.localtime() or ts_date < time.strptime("20070913", "%Y%m%d"): 
                    raise ValueError("Invalid date range, date should be in range [20070913, now]")
                if mode == "daily_ai" and ts_date < time.strptime("20221031", "%Y%m%d"): 
                    raise ValueError("Invalid date range for ai generate content, date should be in range [20221031, now]")
            if page and int(page) < 0: raise ValueError("Invalid page")
        except ValueError as e:
            self.logger.error("%s", e)
            return
        except Exception as err:
            self.logger.error("Unexpected error occurred: %s", err)
            return
        
        base_url = r"https://www.pixiv.net/ranking.php?"
        suffix = []
        if mode: suffix.append("mode=" + mode)
        if content: suffix.append("content=" + content)
        if date: suffix.append("date=" + date)
        if page: suffix.append("p=" + str(page))
        suffix.append("format=json")

        request_url = base_url + '&'.join(suffix)
        self.logger.info(f"opening ranking page on %s", request_url)
        r = self.open(request_url)
        if not r or not r.ok:
            return
        else:
            self.logger.info("ranking page opened.")
        
        result = r.json()["contents"]
        self.res.extend(result)
        self.logger.info("%d items found.", len(result))

        return
    
    def resolve(self) -> list:
        '''
        This function returns the result list.
        Returns:
            list : The result list. Each item is a dict of illustration item.
        '''
        self.logger.debug("%s.resolve(), %d items found.", self, len(self.res))
        return self.res


class illustPageSession(baseSession):
    '''
    This is a subclass of baseSession. It is designed to resolve the urls of illustration items based on a illustid.
    '''
    def __init__(self):
        super().__init__()
        self.res = list()
    
    def reset(self) -> None:
        '''
        This will clear all settings including headers, proxies and retry times, and reset the result list.
        '''
        super().reset()
        self.res = list()
        self.logger.debug("result list reset, cleared %d items.", len(self.res))
        return

    def get_illust_page(self, illust_id : int) -> None:
        '''
        This function resolve the urls of illustration items based on a illustid.
        Parameters:
            illust_id : int
                The illust id of the illustration.
        Returns:
            str : The result of this action.
        '''
        url = "https://www.pixiv.net/ajax/illust/{:}/pages?lang=en".format(illust_id)

        self.logger.info("getting illust page, illust_id=%s", illust_id)

        r = self.open(url, referer = "https://www.pixiv.net/en/artworks/{:}".format(illust_id))
        if not r or not r.ok:
            self.logger.error("Failed to get illust page.")
            return
        self.logger.info("illust page opened.")

        illust_page_dict = {"illust_id" : illust_id, "resolved_pics": list()}
        for pics in r.json()["body"]:
            illust_page_dict['resolved_pics'].append(pics["urls"]["original"])
        
        self.res.append(illust_page_dict)
        self.logger.info("illust page resolved, %d items found.", len(illust_page_dict['resolved_pics']))
        return

    def resolve(self) -> list:
        '''
        This function returns the result list.
        Returns:
            list : The result list. Each item is a dict of illustration item.
        '''
        self.logger.debug("%s.resolve(), %d items found.", self, len(self.res))
        return self.res
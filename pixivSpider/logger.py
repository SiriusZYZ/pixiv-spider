import logging
import os

class pLogger():
    '''
    Please do not use this class directly, use the logger in the main class.
    '''
    def __init__(
            self,
            name: str,
            level: int,
            ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '%(asctime)s @%(name)s:[%(levelname)s] %(message)s')
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(level)
        self.stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stream_handler)

    def DEBUG(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)
    
    def INFO(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)
    
    def WARNING(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)
    
    def ERROR(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)
    
    def CRITICAL(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)
    

Logger = pLogger("pixivSpider", logging.DEBUG)


if __name__ == "__main__":
    pass


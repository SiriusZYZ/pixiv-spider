import logging
import os


level_str_dict = {
    logging.DEBUG: "DEBUG",
    logging.INFO: "INFO",
    logging.WARNING: "WARNING",
    logging.ERROR: "ERROR",
    logging.CRITICAL: "CRITICAL"
}
str_level_dict = {v:k for k,v in level_str_dict.items()}

class pLogger():
    '''
    Please do not use this class directly, use the logger in the main class.
    '''
    def __init__(
            self,
            name: str,
            level: int):


        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '%(asctime)s @%(name)s:[%(levelname)s] %(message)s')
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.INFO)
        self.stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stream_handler)
        self.file_handler = None

        self.debug("Logger initialized.")
        self.debug(
            """Logger name: %s, Logger level: %s, Stream level: %s, Formatter: %s""",
            self.logger.name,
            level_str_dict[level],
            self.stream_handler.level,
            self.formatter)
    
    def set_stream_level(self, level: str):
        if level.upper() not in str_level_dict.keys():
            self.error("Invalid level: %s", level)
            return
        self.stream_handler.setLevel(str_level_dict[level.upper()])
        self.debug("stream level set to %s", level_str_dict[str_level_dict[level.upper()]])

    def silent_stream(self):
        self.set_stream_level("critical")
    
    def verbose_stream(self):
        self.set_stream_level("debug")
    
    def set_file_handler(self, path: str, level: int = logging.DEBUG):
        self.debug("set file handler, path: %s, level: %s", path, level_str_dict[level])
        self.file_handler = logging.FileHandler(path)
        self.file_handler.setLevel(level)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.info("file logging enable at [%s]", path)
    
    def log(self, *args, **kwargs):
        self.logger.log(logging.INFO, *args, **kwargs)

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)
    
    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)
    
    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)
    
    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)
    
    def critical(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)
    

Logger = pLogger("pixivSpider", logging.DEBUG)


if __name__ == "__main__":
    pass


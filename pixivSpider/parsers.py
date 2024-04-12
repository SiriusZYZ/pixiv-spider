import json
from html.parser import HTMLParser

class userPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.res = None
    
    def handle_starttag(self, tag, attrs):
        if tag == "meta" and attrs[0] == ('name', 'preload-data'):
            self.res = json.loads(attrs[2][1])["user"]
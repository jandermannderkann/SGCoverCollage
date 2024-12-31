import time
from bs4 import BeautifulSoup
import re
from urllib import request

ISBNSEARCH_BASE_URL="https://isbnsearch.org/"
ISBNSEARCH_SLUG="isbn/{isbn}"

class isbnSearchPicLoader:
    '''
    Tries to download pictures for ISBN's based on isbnsearch.org
    '''
    
    per_call_break = 0.5 # in seconds

    def __init__(self):
        pass

    def post_request(self):
        # paceing
        time.sleep(self.per_call_break)
        
    def has_captcha(self, soup):
        return soup.find('div',{'class':'g-recaptcha'}) != None

    def get_pic_url(self, isbn:str):
        url = ISBNSEARCH_BASE_URL + ISBNSEARCH_SLUG.format(isbn=isbn)
        dom = self.make_request(url)
        self.post_request()
        soup = BeautifulSoup(dom)
        
        if self.has_captcha(soup):
            exit("Oups we were are rate-limited")

        bookDiv = soup.find('div', id="book")
        if bookDiv == None:
            print(soup)
            exit("Error parsing html")

        imgDiv = bookDiv.find("div", {'class':'image'})
        imgE = imgDiv.find("img")
        print(imgE)
            
        return imgE.text
    
    def make_request(self, url:str):
        req = request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        f = request.urlopen(req)
        return f.read().decode('utf-8')


    def download_pic(self, url:str):
        pass

    def ISBN2Pic(self, isbn: str):
        url = self.get_pic_url(isbn)
        self.download_pic(url)


def isIsbn(str:str):
    return len(str)==13

def isASIN(str:str):
    return len(str)==10 
    
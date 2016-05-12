import urllib
#import aiohttp
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote

def is_valid_url(url:str):
        validateURL = 'https://www.youtube.com/watch?v'
        url = str(url).replace(' ', '')
        urlValidation = url.split('=')
        if urlValidation[0] == validateURL:
            return True
        else:
            return False

def search(myquery):
    elements = []
    url = 'https://www.youtube.com/results?search_query=' + quote(myquery)
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        elements.append('https://www.youtube.com' + vid['href'])
    return elements

def download_url(videourl):
    print(videourl)
    pattern = 'https://youtu.be/'
    downloadurl = pattern + videourl.split('=')[1]
    print(downloadurl)
    return downloadurl

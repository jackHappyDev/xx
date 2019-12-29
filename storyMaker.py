from bs4 import BeautifulSoup
from flask import jsonify
import json
import requests

BaseUrl = 'http://www.okzy.co/'
BASE_FIRSTURL = 'http://www.okzy.co/?m=vod-type-id-1.html'
LocalPath = '/Users/jack/Desktop/123/'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
videos = []

def getStoryList(path):
    response = requests.get(path,headers =headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text)
    info = []
    for v in soup.find_all('span',attrs={'class':'xing_vb4'}):
        x = v.find_all('a')[0]
        dic = {}
        dic['title']= x.text
        dic['url'] = BaseUrl + x['href']
        dic['imgUrl'] = getStoryImg(dic['url'])
        info.append(dic)

    result = json.dumps(info,indent=len(info))
    return result

def getStoryImg(path):
    response = requests.get(path, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text)
    imgUrl = ''
    for v in soup.find_all('div', attrs={'class': 'vodImg'}):
        v = v.find_all('img')[0]
        imgUrl = v['src']
        print(imgUrl)
    return json.dumps(imgUrl)





if __name__ == '__main__':
    getStoryList(BASE_FIRSTURL)
    # getStoryImg()
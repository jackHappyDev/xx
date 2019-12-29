import re
import json
import requests
from  flask import jsonify
from bs4 import BeautifulSoup
BaseUrl = 'http://www.okzy.co/'
BASE_FIRSTURL = 'http://www.okzy.co/index.php'
LocalPath = '/Users/jack/Desktop/123/'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
SimpleSearchUrl = 'http://www.okzy.co//?m=vod-detail-id-24967.html'

def getSraechList(searchContent):
    keyWords = {'m': 'vod-search', 'wd':searchContent, 'submit': 'search'}
    response =requests.post(url=BASE_FIRSTURL,params=keyWords,headers=headers)
    # print(response.text)
    soup = BeautifulSoup(response.text)
    xxlist =[]
    for v in soup.find_all('span',attrs={'class':'xing_vb4'}):
        v = v.find_all('a')[0]
        title = v.string
        url =BaseUrl + v['href']
        xxlist.append({'videoName':title,'videoPlayUrl':url})
        getVideoAddFromPath(url,title)
    return xxlist

def getVideoAddFromPath(path,name):
    response = requests.post(url=path, headers=headers)
    soup = BeautifulSoup(response.text)
    videolist = []
    currentIdx = 1
    for v in  soup.find_all('input',attrs={'name':'copy_sel'}):
        str = v['value']
        dic = {}
        if str.endswith('.m3u8'):
            dic['videoPlayUrl'] = str
            dic['videoName'] = '%s第%d集'%(name,currentIdx)
            currentIdx +=1
            videolist.append(dic)
    print(videolist)
    return videolist


def getVideoCategoryList():
    inDic = {}
    cateList =['m1','m2','m3','m4']
    response = requests.get(url=BaseUrl,headers=headers)
    soup =BeautifulSoup(response.text)
    for i in  range(len(cateList)):
        xxlist = []
        for v in soup.find_all('div',attrs={'id':cateList[i]}):
            for xxx in v.find_all('a'):
                xxxdic = {}
                xxxdic['title'] = xxx.text
                xxxdic['href'] = BaseUrl+xxx['href']
                xxlist.append(xxxdic)
            # print(xxlist)
            # print('***' * 100)
        inDic[cateList[i]] = xxlist
    print(inDic)
    return inDic



if __name__ == '__main__':
    # getSraechList('叶问')
    getVideoCategoryList()

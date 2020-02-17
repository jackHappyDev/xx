import re
import json
import requests
from  flask import jsonify
from bs4 import BeautifulSoup
from sqlalchemy import create_engine,Column,Integer,String,Table,MetaData
import pymysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BaseUrl = 'http://www.okzy.co/'
BASE_FIRSTURL = 'http://www.okzy.co/index.php'
LocalPath = '/Users/jack/Desktop/123/'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
SimpleSearchUrl = 'http://www.okzy.co//?m=vod-detail-id-24967.html'

engine = create_engine('mysql+pymysql://root:jj123456@127.0.0.1/videoInfoList',echo =False)
DBSession = sessionmaker(bind=engine)

session = DBSession()

Base = declarative_base()

metadata =MetaData(engine)

#创建类目 数据库
# MoviesInfo = Table('MoviesInfo',metadata,
#                    Column('id',Integer,primary_key=True,autoincrement=True),
#                    Column('title',String(10)),
#                    Column('href',String(100)),
#                    Column('tp',String(20)),
#                    )
#
# metadata.create_all(engine)


#创建类目下面的类型 数据库 分类装 类型下面的所有地址
# MoviesDetailListInfo =Table('MoviesDetailListInfo',metadata,
#                             Column('id',Integer,primary_key=True,autoincrement=True),
#                             Column('moveType',String(10)),
#                             Column('title',String(100)),
#                             Column('link',String(100)),
#                             Column('did',Integer),
#                             )
# metadata.create_all(engine)

#创建播放信息的视频列表
VideoPlayInfo = Table(
    'VideoPlayInfo',metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('videoName',String(100)),
    Column('videoImg',String(100)),
    Column('videoInfoContent',String(10000)),
    Column('videoPlayAdd',String(200)),
)
metadata.create_all(engine)

#创建电影或者电视剧的m3u8的视频地址列表
VideoM3u8List = Table(
    'VideoM3u8List',metadata,
    Column('id',Integer,primary_key=True,autoincrement=True),
    Column('playAdd',String(100)),
    Column('fzid',Integer),
)
metadata.create_all(engine)




class MoviesInfo(Base):
    __tablename__ = 'moviesInfo'
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(10))
    href =Column(String(200))
    tp = Column(String(20))

class MoviesDetailListInfo(Base):
    __tablename__ = 'moviesDetailListInfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    moveType = Column(String(10))
    title = Column(String(100))
    link = Column(String(200))
    did =Column(Integer)

class VideoPlayInfo(Base):
    __tablename__ = 'videoPlayInfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    videoName = Column(String(100))
    videoImg = Column(String(100))
    videoInfoContent = Column(String(2500))
    videoPlayAdd = Column(String(200))

class VideoM3u8List(Base):
    __tablename__ = 'videoM3u8List'
    id = Column(Integer, primary_key=True, autoincrement=True)
    playAdd = Column(String(100))
    fzid = Column(Integer)


#查
def searchDataInfoById(d):
    infox = session.query(MoviesInfo).filter(MoviesInfo.tp == d).all()
    session.commit()
    ulist = []
    for v in  infox:
        udic = {}
        udic['id'] = v.id
        udic['title'] = v.title
        udic['href'] = v.href
        udic['tp'] = v.tp
        ulist.append(udic)
    # print(ulist)
    # return ulist
    getDataFromCategoryInfoSearch(ulist)

#数据路存储分类信息
def getVideoCategoryList():
    cateList =['m1','m2','m3','m4']
    response = requests.get(url=BaseUrl,headers=headers)
    soup =BeautifulSoup(response.text)
    jdex = 1
    for i in  range(len(cateList)):
        xxlist = []
        for v in soup.find_all('div',attrs={'id':cateList[i]}):
            for xxx in v.find_all('a'):
                jdex += 1
                tpp = cateList[i]
                if tpp in 'm1':
                    tpp = 'DY'
                elif tpp in 'm2':
                    tpp = 'DS'
                elif tpp in 'm3':
                    tpp = 'ZY'
                else:
                    tpp = 'DH'
                dxx = MoviesInfo(id=(jdex+10001),title=xxx.text,href=BaseUrl+xxx['href'],tp=tpp)
                session.add_all([dxx])
                session.commit()



def getDataFromCategoryInfoSearch(list):
    jdx = 0
    for i in range(len(list)):
        url = list[i]['href']
        title = list[i]['title']
        did = list[i]['id']
        bidx = (i+1)*10000
        response = requests.get(url=url,headers=headers)
        soup =BeautifulSoup(response.text)
        for v in soup.find_all('span',attrs={'class':'xing_vb4'}):
            jdx += 1
            info = v.find_all('a')[0]
            # dxx = MoviesDetailListInfo(id=(jdx + bidx), title=info.text, link=BaseUrl + info['href'], moveType=title ,did=did)
            # session.add_all([dxx])
            # session.commit()
            getCurrentVideDetail(BaseUrl + info['href'],jdx)
            # print(info.text,info['href'])


#在线搜索结果
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
    print(xxlist)
    return xxlist



#搜索每个页面的m3u8
def getVideoAddFromPath(path,name):
    response = requests.post(url=path, headers=headers)
    soup = BeautifulSoup(response.text)
    videolist = []
    currentIdx = 1
    videoimg = soup.find(attrs={'class':'lazy'})
    for v in  soup.find_all('input',attrs={'name':'copy_sel'}):
        str = v['value']
        dic = {}
        if str.endswith('.m3u8'):
            dic['videoPlayUrl'] = str
            dic['videoName'] = '%s第%d集'%(name,currentIdx)
            dic['videoImg'] =videoimg['src']
            currentIdx +=1
            videolist.append(dic)
    # print(videolist)
    return videolist




#根据id 查找每个影片对应的信息
def getFilterVideoinfoById(kw):
    infox = session.query(VideoPlayInfo).filter(VideoPlayInfo.videoName.like('%'+kw+'%')).all()
    session.commit()
    rtList =[]
    print(str(len(infox)))
    for v in infox:
        idf = {}
        infoxx = session.query(VideoM3u8List).filter(VideoM3u8List.fzid == v.id).all()
        session.commit()
        addList = []
        idf['videoName'] = v.videoName
        idf['videoImg'] = v.videoImg
        idf['videoInfoContent'] = v.videoInfoContent
        for i in infoxx:
            addList.append(i.playAdd)
        idf['videoPlayAdd'] = addList
        # print(idf,len(addList))
        rtList.append(idf)
    print(rtList)






#获取每一个分类下面的每一行数据的信息
#获取每个页面的详细信息 方便布局以及播放
def getCurrentVideDetail(path,idx):
    response = requests.get(url=path,headers=headers)
    soup =BeautifulSoup(response.text)
    videoInfo = {}
    videoName = ''
    videoImg = ''
    videoDetailContent = ''
    videoPlayAdd = []
    videoDownLoadAdd = ''
    for v in soup.find_all('div',attrs={'class':'vodImg'}):
       xx =  v.find_all('img')[0]
       videoName = xx['alt']
       videoImg = xx['src']
    for v in soup.find_all('input',attrs={'name':'copy_sel'}):
        str = v['value']
        if str.endswith('.m3u8'):
            videoPlayAdd.append(str)
    cc = soup.find(attrs={'class':'vodplayinfo'})
    print(80*'*'+videoName+80*'*')
    if len(videoPlayAdd)>1 :
        dxx = VideoPlayInfo(videoName=videoName, videoImg=videoImg, videoInfoContent=cc.string ,videoPlayAdd='1')
        session.add_all([dxx])
        session.commit()
        for i in range(0,len(videoPlayAdd)):
            print(videoPlayAdd[i])
            dxx1 = VideoM3u8List(playAdd=videoPlayAdd[i],fzid=dxx.id)
            session.add(dxx1)
            session.commit()

    # return  videoInfo


#获取每页数据的说有链接详情全文
def getPerPageToDetailList(path,idx):
    response = requests.post(url=path, headers=headers)
    soup = BeautifulSoup(response.text)
    # print(response.text)
    xxlist = []
    for v in soup.find_all('span', attrs={'class': 'xing_vb4'}):
        v = v.find_all('a')[0]
        title = v.string
        url = BaseUrl + v['href']
        getCurrentVideDetail(url,idx)



#获取所有网站的影片网址列表
def getAllNetReqInfo():
    totalPage = getAllPageSize('http://www.okzy.co/')
    for i in range(1,int(totalPage)):
        perpageUrl = BaseUrl+'/?m=vod-index-pg-'+str(i)+'.html'
        # print(perpageUrl)
        getPerPageToDetailList(perpageUrl,i)


#获取所有的页面的页数
def getAllPageSize(path):
    response = requests.post(url=path, headers=headers)
    soup = BeautifulSoup(response.text)
    for v in soup.find_all('div',attrs={'class':'pages'}):
        list =[]
        for x in v.find_all('a'):
            list.append(x)
        page = list[-1]['href'].split('-')[-1].split('.')[0]
        return page





if __name__ == '__main__':
    # getSraechList('庆余年')
    # getVideoCategoryList()
    # getCurrentVideDetail('http://www.okzy.co//?m=vod-index-pg-1.html','1')
    # searchDataInfoById('DY')
    # getAllPageSize('http://www.okzy.co/')

    #爬取所有页面的数据
    getAllNetReqInfo()
    # getFilterVideoinfoById('大明')
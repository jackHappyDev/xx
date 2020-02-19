from bs4 import BeautifulSoup
from Project import VideoDataBase
import requests

#查
def searchDataInfoById(d):
    infox = VideoDataBase.session.query(VideoDataBase.MoviesInfo).filter(VideoDataBase.MoviesInfo.tp == d).all()
    VideoDataBase.session.commit()
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


def getDataFromCategoryInfoSearch(list):
    jdx = 0
    for i in range(len(list)):
        url = list[i]['href']
        title = list[i]['title']
        did = list[i]['id']
        bidx = (i+1)*10000
        response = requests.get(url=url, headers=VideoDataBase.headers)
        soup = BeautifulSoup(response.text)
        for v in soup.find_all('span',attrs={'class':'xing_vb4'}):
            jdx += 1
            info = v.find_all('a')[0]
            # dxx = MoviesDetailListInfo(id=(jdx + bidx), title=info.text, link=BaseUrl + info['href'], moveType=title ,did=did)
            # session.add_all([dxx])
            # session.commit()
            getCurrentVideDetail(VideoDataBase.BaseUrl + info['href'], jdx)
            # print(info.text,info['href'])







########################################################################################################
########################################################################################################
#数据路存储分类信息
########################################################################################################
########################################################################################################
def getVideoCategoryList():
    cateList =['m1','m2','m3','m4']
    response = requests.get(url=VideoDataBase.BaseUrl, headers=VideoDataBase.headers)
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
                dxx = VideoDataBase.MoviesInfo(id=(jdex + 10001), title=xxx.text, href=VideoDataBase.BaseUrl + xxx['href'], tp=tpp)
                VideoDataBase.session.add_all([dxx])
                VideoDataBase.session.commit()



########################################################################################################
########################################################################################################
#在线搜索结果
########################################################################################################
########################################################################################################
def getSraechList(searchContent):
    keyWords = {'m': 'vod-search', 'wd':searchContent, 'submit': 'search'}
    response =requests.post(url=VideoDataBase.BASE_FIRSTURL, params=keyWords, headers=VideoDataBase.headers)
    # print(response.text)
    soup = BeautifulSoup(response.text)
    xxlist =[]
    for v in soup.find_all('span',attrs={'class':'xing_vb4'}):
        v = v.find_all('a')[0]
        title = v.string
        url = VideoDataBase.BaseUrl + v['href']
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


########################################################################################################
########################################################################################################
#根据关键字 数据库搜索 查找每个影片对应的信息 远程查询关键字派和jsonify
########################################################################################################
########################################################################################################

def getFilterVideoinfoById(kw):
    infox = VideoDataBase.session.query(VideoDataBase.VideoPlayInfo).filter(
    VideoDataBase.VideoPlayInfo.videoName.like('%' + kw + '%')).filter(VideoDataBase.VideoPlayInfo.videoInfoContent.like('%' + kw + '%')).all()
    VideoDataBase.session.commit()
    rtList =[]
    for v in infox:
        idf = {}
        infoxx = VideoDataBase.session.query(VideoDataBase.VideoM3u8List).filter(
        VideoDataBase.VideoM3u8List.fzid == v.id).all()
        VideoDataBase.session.commit()
        addList = []
        idf['videoName'] = v.videoName
        idf['videoImg'] = v.videoImg
        idf['videoInfoContent'] = v.videoInfoContent
        for i in infoxx:
            addList.append(i.playAdd)
        idf['videoPlayAdd'] = addList
        # print(idf,len(addList))
        rtList.append(idf)
    return rtList



########################################################################################################
#####################################数据库采集操作采集远程数据库信息#########################################
########################################################################################################
########################################################################################################

#获取所有网站的影片网址列表
def getAllNetReqInfo():
    totalPage = getAllPageSize('http://www.okzy.co/')
    for i in range(1,int(totalPage)):
        perpageUrl = VideoDataBase.BaseUrl + '/?m=vod-index-pg-' + str(i) + '.html'
        # print(perpageUrl)
        getPerPageToDetailList(perpageUrl,i)

#获取每一个分类下面的每一行数据的信息
#获取每个页面的详细信息 方便布局以及播放 存储数据库
def getCurrentVideDetail(path,idx):
    response = requests.get(url=path,headers=VideoDataBase.headers)
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
        dxx = VideoDataBase.VideoPlayInfo(videoName=videoName, videoImg=videoImg, videoInfoContent=cc.string, videoPlayAdd='1')
        VideoDataBase.session.add_all([dxx])
        VideoDataBase.session.commit()
        for i in range(0,len(videoPlayAdd)):
            print(videoPlayAdd[i])
            dxx1 = VideoDataBase.VideoM3u8List(playAdd=videoPlayAdd[i], fzid=dxx.id)
            VideoDataBase.session.add(dxx1)
            VideoDataBase.session.commit()


#获取每页数据的说有链接详情全文
def getPerPageToDetailList(path,idx):
    response = requests.post(url=path, headers=VideoDataBase.headers)
    soup = BeautifulSoup(response.text)
    # print(response.text)
    xxlist = []
    for v in soup.find_all('span', attrs={'class': 'xing_vb4'}):
        v = v.find_all('a')[0]
        title = v.string
        url = VideoDataBase.BaseUrl + v['href']
        getCurrentVideDetail(url,idx)



#获取所有的页面的页数
def getAllPageSize(path):
    response = requests.post(url=path, headers=VideoDataBase.headers)
    soup = BeautifulSoup(response.text)
    for v in soup.find_all('div',attrs={'class':'pages'}):
        list =[]
        for x in v.find_all('a'):
            list.append(x)
        page = list[-1]['href'].split('-')[-1].split('.')[0]
        return page

########################################################################################################
########################################################################################################
########################################################################################################




def getTest(path):
    response = requests.get(url=path, headers=VideoDataBase.headers)
    soup =BeautifulSoup(response.text)
    videoInfo = {}
    videoName = ''
    videoImg = ''
    videoDetailContent = ''
    videoPlayAdd = []
    videoOnLinePlayAdd = []
    videoDownLoadAdd = []
    actorer = ''
    videoNickName = ''
    Director = ''

    for v in soup.find_all('div',attrs={'class':'vodImg'}):
       xx =  v.find_all('img')[0]
       videoName = xx['alt']
       videoImg = xx['src']
    for v in soup.find_all('input',attrs={'name':'copy_sel'}):
        str = v['value']
        if str.endswith('.m3u8'):
            videoPlayAdd.append(str)
        elif str.endswith('.mp4'):
            videoDownLoadAdd.append(str)
        else:
            videoOnLinePlayAdd.append(str)
    for v in soup.find_all('div',attrs={'class':'vodinfobox'}):
        # print(v.find_all('span'))
        xxlist = v.find_all('span')
        videoNickName = xxlist[0].string
        Director = xxlist[1].string
        actorer = xxlist[2].string
    cc = soup.find(attrs={'class':'vodplayinfo'})
    videoDetailContent = cc.string
    print(videoNickName,'\n',Director,'\n',actorer)
    print(videoName,'\n',videoImg,'\n',videoDownLoadAdd,'\n',videoPlayAdd,'\n',videoDetailContent,'\n',videoOnLinePlayAdd)


if __name__ == '__main__':
    # getSraechList('007')
    # getVideoCategoryList()
    # getCurrentVideDetail('http://www.okzy.co//?m=vod-index-pg-1.html','1')
    # searchDataInfoById('DY')
    # getAllPageSize('http://www.okzy.co/')

    #爬取所有页面的数据
    # getAllNetReqInfo()
    getFilterVideoinfoById('大明')

    # getTest('http://www.okzy.co//?m=vod-detail-id-45018.html')
    # tpInsert()
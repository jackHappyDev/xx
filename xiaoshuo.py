import requests
from bs4 import BeautifulSoup

BaseUrl = "https://www.qb5.tw/"

def getxiaoshuoInfo():
    response =requests.get(BaseUrl)
    response.encoding = 'gbk'
    # print(response.text)
    soup = BeautifulSoup(response.text)

    #抓取头部列表和标题啊
    # tlist = soup.find_all('div', attrs={'class': 'nav_cont'})
    # getTopInfoList(tlist)

    ###各类top1
    # top1list = soup.find_all('div', attrs={'class': 'item'})
    # getEveTop1(top1list)

    ###热门 收藏 全本 最新
    # top1list = soup.find_all('div', attrs={'id': 'mainright'})
    # top1list = top1list[0]
    # xcatoryList = top1list.find_all('div', attrs={'class': 'titletop'})
    # getHotXiaoshuo(xcatoryList[0])


    ######获取最近更新的数据
    tlist = soup.find_all('div', attrs={'class': 'uplist'})
    # print(tlist)
    xnewList = tlist[0].find_all('ul', attrs={'class': 'titlelist'})
    getrecommend(xnewList[0])



##头部列表和标题
def getTopInfoList(arr):
    topInfoArr = []
    for item in arr:
        alist = item.find_all('a')
        for aitem in alist:
            topTitleInfo = {}
            topTitleInfo['title'] = aitem['title']
            topTitleInfo['href'] = aitem['href']
            topInfoArr.append(topTitleInfo)
    print(topInfoArr)


###各类top1
def getEveTop1(arr):
    topInfoArr = []
    for item in arr:
        alist = item.find_all('a')
        clist = item.find_all('dd', attrs={'class': 'info'})
        for aitem in alist:
            topTitleInfo = {}
            topTitleInfo['title'] = aitem['title']
            topTitleInfo['href'] = aitem['href']
            if(aitem.find('img') != None):
                topTitleInfo['src'] = aitem.find('img')['src']
            topTitleInfo['info'] = clist[0].text
            topInfoArr.append(topTitleInfo)
    # print(topInfoArr)

#获取热门小说 收藏 全本 最新
def getHotXiaoshuo(info):
    lilist = info.find_all('li')
    for item in lilist:
        info = {}
        author = item.find_all('small',attrs={'class':'txt-right-gray'})
        info['actor'] =author[0].text
        type = item.find_all('em',attrs={'class':'s1'})
        info['type'] = type[0].text
        content = item.find_all('a')
        info['href'] = content[0]['href']
        info['title'] = content[0]['title']


##获取推荐书本信息
def getrecommend(info):
    tnewList =[]
    for item in info:
        # print(item)
        info = {}
        type = item.find_all('div', attrs={'class': 'lb'})
        info['type'] = type[0].text

        totalLink = item.find_all('div', attrs={'class': 'zp'})[0].find_all('a')[0]['href']

        bookName = item.find_all('div', attrs={'class': 'zp'})[0].find_all('a')[0]['title']

        newComeLink = item.find_all('div', attrs={'class': 'zz'})[0].find_all('a')[0]['href']

        newComeTitle = item.find_all('div', attrs={'class': 'zz'})[0].find_all('a')[0]['title']

        author = item.find_all('div',attrs={'class':'author'})[0].text

        upTime = item.find_all('div',attrs={'class':'sj'})[0].text

        info['totalLink'] =totalLink
        info['bookName'] = bookName
        info['newComeLink'] = newComeLink
        info['newComeTitle'] = newComeTitle
        info['author'] = author
        info['upTime'] = upTime
        tnewList.append(info)
        # print(totalLink)

    # print(tnewList)
    # getNewBookinfoDetail(tnewList[0]['newComeLink'],tnewList[0]['newComeTitle'])
    getAllBookContentInfoByLink(tnewList[0]['totalLink'])
####获取书的最新章节信息
def getNewBookinfoDetail(link,name):
    response =requests.get(link)
    response.encoding = 'gbk'
    soup =BeautifulSoup(response.text)
    contect = soup.find_all('div',attrs={'id':'content'})
    # print(contect[0].text)
    contentArr = contect[0].text.split('最新章节！')
    # print(contentArr[1])
    file_handle = open('%s.txt'%name, mode='w')
    file_handle.write(contentArr[1])
    file_handle.close()
    pass

#####获取所有页面的章节
def getAllBookContentInfoByLink(link):
    response = requests.get(link)
    response.encoding = 'gbk'
    soup = BeautifulSoup(response.text)
    BOOK_id = soup.find_all('script', attrs={'type': 'text/javascript'})
    book_id = 'book_'+ BOOK_id[-1].string.split('("')[1].split('")')[0]+'/'
    contect = soup.find_all('div', attrs={'class': 'zjbox'})
    xxlist = contect[0].find_all('dd')
    xxshowList =[]
    index = 0
    for item in xxlist:
        if(len(item.find_all('a'))>0):
            info = {}
            itema = item.find_all('a')[0]
            # print(itema)
            index +=1
            if(index>12):
                info['href'] =BaseUrl+book_id+itema['href']
                info['title'] =itema.text
                xxshowList.append(info)
    print(xxshowList)



if __name__ == '__main__':
    getxiaoshuoInfo()















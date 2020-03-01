from bs4 import BeautifulSoup
import requests
import random
import string

ippool = []
NETWORK_STATUS = True  # 判断状态变量
msgs = ''

def searchM():
    url = 'https://www.so.com/s'
    while True:
        kw  =getRadomStr()+getRadomStr()
        print(80*'*'+kw+80*'*')
        # kw = input('请输入关键字:>>>')
        pro = ['171.13.201.154:9999',
                   '183.166.138.253:9999',
                   '125.108.120.60:9000',
                   '39.137.69.8:8080',
                   '171.35.143.146:9999',
                   '59.42.89.108:8118',
                   '115.221.240.250:9999',
                   '123.54.47.137:9999',
                   '140.143.53.70:8118',
                   ]
        # pro = xxgetIpPool()
        para = {
            'q': kw,
            'src':'srp',
            'fr' : '360portal',
            'psid' : xxradomStr()
        }
        xx = random.choice(pro)
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  #
        response = requests.get(url, proxies={'http': xx}, headers={'User-Agent': xxradomUA()},params=para,timeout=25)  # 让问这个网页 随机生成一个ip
        # print(response.text)
        try:
            if response.status_code == 200:
                soup = BeautifulSoup(response.content)
                for dd in soup.find_all('dd', attrs={'class': 'so-pdr-bd'}):
                    # print(dd.find_all('a'))
                    for xx in dd.find_all('a'):
                        print(xx.string)

        except requests.exceptions.Timeout:
            global NETWORK_STATUS
            NETWORK_STATUS = False  # 请求超时改变状态

            if NETWORK_STATUS == False:
                '''请求超时'''
                print('*********请求超时********')
                searchM(msgs)




def xxradomStr():
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 34))
    return ran_str

def xxradomUA():
    ua = 'Mozilla/%d.0 (compatible; MSIE %d.%d; Windows NT)' % (random.randint(1, 20),random.randint(1, 20),random.randint(1, 10))
    return ua

def xxgetIpPool():
    global ippool
    url = 'https://www.kuaidaili.com/free/'
    response = requests.get(url,headers={'User-Agent': xxradomUA()})
    print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content)
        list = []
        if len(ippool)>0:
            return ippool
        else:
            for dd in soup.find_all('table', attrs={'class': 'table table-bordered table-striped'}):
                for xx in dd.find_all('td',attrs={'data-title':'IP'}):
                    list.append(xx.string)
                ippool = list
                return list


def getRadomStr():
    first_name_list = [
        '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
        '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
        '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
        '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
        '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
        '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
        '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']
    xx = ''.join(first_name_list)

    return random.choice(xx)


# def getHuiLv():
#     url = 'http://www.flw.ph/forum-169-2.html'
#     pro = ['171.13.201.154:9999',
#                    '183.166.138.253:9999',
#                    '125.108.120.60:9000',
#                    '39.137.69.8:8080',
#                    '171.35.143.146:9999',
#                    '59.42.89.108:8118',
#                    '115.221.240.250:9999',
#                    '123.54.47.137:9999',
#                    '140.143.53.70:8118',
#                    ]
#     xx = random.choice(pro)
#     requests.adapters.DEFAULT_RETRIES = 15  # 增加重连次数
#     s = requests.session()
#     s.keep_alive = False  #
#     response = requests.get(url, proxies={'http': xx}, headers={'User-Agent': xxradomUA()},timeout=25)
#     print(response.text)
#     soup =BeautifulSoup(response.text)
#     for i in soup.find_all('div',attrs={'class':'forumsummary'}):
# #         print(i)
#
#
# def getAllpage():
#     url = 'http://www.flw.ph/forum-169-1.html'
#     pro = xxgetIpPool()
#     xx = random.choice(pro)
#     requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
#     s = requests.session()
#     s.keep_alive = False  #
#     response = requests.get(url, proxies={'http': xx}, headers={'User-Agent': xxradomUA()}, timeout=25)
#     print(response.text)
#     soup =BeautifulSoup(response.text)
#     for i in soup.find_all('div',attrs={'class':'pg'}):
#         print(i)




if __name__ == '__main__':
    # getAllpage()
    # getHuiLv()
    while True:
        searchM()
    # xxradomUA()
    # xxgetIpPool()
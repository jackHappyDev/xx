'''
Created on 2018-4-20

例子:每天凌晨3点执行func方法
'''
import datetime
import threading
from Project import VideoModu

def TMmethod():
    print("haha")
    VideoModu.getAllNetReqInfo()
    #如果需要循环调用，就要添加以下方法
    timer = threading.Timer(10, TMmethod)
    timer.start()

def everyTimeRun():
    # 获取现在时间
    now_time = datetime.datetime.now()
    # 获取明天时间
    next_time = now_time + datetime.timedelta(days=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day
    # 获取明天3点时间
    next_time = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day)+" 10:30:00", "%Y-%m-%d %H:%M:%S")
    # # 获取昨天时间
    # last_time = now_time + datetime.timedelta(days=-1)

    # 获取距离明天3点时间，单位为秒
    timer_start_time = (next_time - now_time).total_seconds()
    # print(timer_start_time)
    # 54186.75975
    VideoModu.getAllNetReqInfo()

    #定时器,参数为(多少时间后执行，单位为秒，执行的方法)
    timer = threading.Timer(timer_start_time, TMmethod)
    timer.start()


# if __name__ == '__main__':
#     everyTimeRun()
#!/usr/bin/python3
#-*- conding: utf-8-
# https://www.jianshu.com/p/a550673a4a25
from socket import *
from Project import VideoDataBase

ipaddr = '127.0.0.1'
port = 8887
back_log = 5

def serverStart():
    tcp_server = socket(AF_INET, SOCK_STREAM)
    tcp_server.bind((ipaddr, port))
    tcp_server.listen(back_log)

    while True:
        conn,addr = tcp_server.accept()
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # print("data is %s" %data.decode('utf-8'))
            conn.send(data.upper())
            list = str(data.decode('utf-8')).split('*')
            dxx = VideoDataBase.Chatlist(msg=list[1],name=list[0],time =list[2])
            VideoDataBase.session.add_all([dxx])
            VideoDataBase.session.commit()

        conn.close()
    tcp_server.close()

if __name__ == '__main__':
    serverStart()
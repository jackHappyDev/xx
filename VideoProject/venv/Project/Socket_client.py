from socket import *
import  random
import time
ipaddr = '127.0.0.1'
port = 8887

name = ""

def client_start():
    name = radomName()
    tcp_client = socket(AF_INET, SOCK_STREAM)

    tcp_client.connect((ipaddr, port))

    while True:
        msg = input(">>>: ")
        if len(msg)==0 or msg.isspace()==True:
            msg = input(">>>: ")
        localtime = time.asctime(time.localtime(time.time()))
        msg = name + '*' + msg + "*" + str(localtime)
        tcp_client.send(msg.encode("utf-8"))
        data = tcp_client.recv(1024)
        print("data is %s" % data.decode("utf-8"))

    tcp_client.close()

def radomName():
    r = ["张三","李四","王五","赵麻子"]
    x = random.randint(0, 3)
    if len(name)<=0:
        return r[x]
    else:
        pass

if __name__ == '__main__':
    client_start()
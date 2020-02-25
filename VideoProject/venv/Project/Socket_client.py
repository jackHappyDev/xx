from socket import *

ipaddr = '127.0.0.1'
port = 8000

tcp_client = socket(AF_INET, SOCK_STREAM)

tcp_client.connect((ipaddr, port))

while True:
    msg = input(">>>: ")
    tcp_client.send(msg.encode("utf-8"))
    data = tcp_client.recv(1024)
    print("data is %s" % data.decode("utf-8"))

tcp_client.close()
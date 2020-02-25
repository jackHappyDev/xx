from socket import *

ipaddr = '127.0.0.1'
port = 8000
back_log = 5

tcp_server = socket(AF_INET, SOCK_STREAM)
tcp_server.bind((ipaddr, port))
tcp_server.listen(back_log)

while True:
    conn,addr = tcp_server.accept()

    while True:
        try:
            data = conn.recv(1024)
            print("data is %s" %data.decode('utf-8'))
            conn.send(data.upper())
        except Exception:
            break

    conn.close()
tcp_server.close()

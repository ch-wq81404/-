import socket

host = '10.95.222.187'    
#两个段口必须一致
port = 25535
addr = (host, port)
byte = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    data = input('Please input the message: ')
    text = data.encode('utf-8')
    sock.sendto(text, addr)

    #输入'exit'退出
    if data == 'exit':
        break
    else:    
        #getsockname返回当前套接字的信息(IP,端口号)
        print("The OS assigned me the address {}".format(sock.getsockname()))
        data, addr = sock.recvfrom(byte)
        text = data.decode("utf-8")
        print('The server {} replied{!r}'.format(addr, text))

sock.close()

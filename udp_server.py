import socket
from tkinter import *
import time
byte = 1024
#两个端口要保持一致
port = 25535  
host = "10.95.222.187"
addr = (host, port)

#创建套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#绑定
sock.bind(addr)
print("waiting to receive messages...")

def sendmsg():
    '''msg = '客户端'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n'
    print (msg)
    txt_msglist.insert(END,msg,'green') #添加时间
    txt_msglist.insert(END,text) #获取发送消息，添加文本到消息列表'''
    while True:
        (data, addr) = sock.recvfrom(byte)
        text = data.decode('utf-8')
        if text == 'exit':
            break 
        else :
            msg = '客户端'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n'
            print (msg+':'+text)
            text = 'Your data was {}bytes long'.format(len(data))
            data = text.encode('utf-8')
            sock.sendto(data, addr)

sendmsg()
#关闭套接字
sock.close()

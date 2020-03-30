#!/usr/bin/env python
#-*- utf8 -*-  
import socket           
import os

HOST = "10.95.222.187"
PORT = 5555 
addr = (HOST,PORT)  
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(addr)                                              
s.listen(1)
conn,addr = s.accept()

def get_file():
    data = conn.recv(1024)
    with open("D:\\recv.txt","a+") as f:
        sdata=str(data,encoding='gbk')
        f.write(sdata)
        print("写入成功")

def send_file():
    filepath = conn.recv(1024)
    with open(filepath,'rb') as f:
        data = f.read()
        conn.sendall(data)
        print("传输成功")

def main():
    while True:
        cmd = conn.recv(1024)
        sdata = str(cmd,encoding='gbk')
        if sdata == "bye":  
            break
        if sdata == "upload":
            print("等待上传")
            get_file()
            break
        if sdata == "down": 
            print("等待下载")
            send_file()
            break
        if sdata:
            conn.sendall(cmd)
        else:
            conn.send("finish") 
    #conn.close()
    s.close()

if __name__ == "__main__":
    main()

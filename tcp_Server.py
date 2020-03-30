#服务端
# -*-coding: utf-8 -*-
import socket
import threading
import wx
users = [('1234','1234'),('2222','2345')]


#接受客户端发来的信息
def clientThreadIn(conn,nick):
    global  data
    while True:
        try:
            tmp = conn.recv(1024).decode()
            if not tmp:
                conn.close()
                return
            if tmp == ':exit':
                #conn.close()
                NotifyAll(nick + ' leaves the room')  # 正常退出
                conn.close()
                return
            NotifyAll(tmp)
            print(data)

        except :
            NotifyAll(nick+' leaves the room') #出现异常退出
            print(data)
            return
def clientThreadOut(conn,nick):
    global data
    while True:
        if con.acquire():
            con.wait()  #放弃对资源占用，等待通知 ，然后运行后面代码
            if data:
                try:
                    conn.send(data.encode())
                    con.release()
                except:
                    con.release()
                    return
def NotifyAll(ss):
    global  data
    if con.acquire(): #获取锁定线程所有权
        data = ss
        print (data)
        con.notifyAll() #放弃当前线程对资源的占用，通知所有等待线程从wait方法执行
        con.release()

'''class LoginFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'socket编程 登陆',size=(350, 350))
        panel = wx.Panel(self, -1)

        self.port = wx.StaticText(parent=panel,label="端口:",pos=(40, 20))
        self.portText = wx.TextCtrl(panel, -1, pos=(120,20),
                               size=(120, -1))
app = wx.App()
LoginFrame().Show()
app.MainLoop()'''

#HOST = raw_input("input the server ip address:")
con = threading.Condition()
HOST = '10.95.222.187'
port = 8887
data = ''

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('socket created')
s.bind((HOST,port))
s.listen(5)
print('Socket now listening')

while True:
    conn,addr = s.accept() #接受连接
    print('Connected with'+addr[0]+':'+str(addr[1]))
    while 1:
        infor = conn.recv(1024).decode() #获取用户名
        infor = infor.split(',')
        nick,pword = infor[0],infor[1]

        if (nick,pword) not in users:
            conn.send("0".encode())
        else:
            conn.send("1".encode())
            break
    NotifyAll('Welcome '+str(nick)+' to the room!')
    #print(data)
    print( str((threading.activeCount()+1)/2) + 'person(s)' ) #当前房间人数 两个线程/2
    conn.send(data.encode())
    threading.Thread(target=clientThreadIn, args=(conn, nick)).start()
    threading.Thread(target=clientThreadOut, args=(conn, nick)).start()

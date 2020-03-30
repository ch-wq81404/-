#客户端
# -*-coding: utf-8 -*-
import socket
import threading
import wx

outString = ''
inString = ''
nick = ''


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class LoginFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'socket编程 登陆',size=(350, 350))
        panel = wx.Panel(self, -1)

        '''self.port = wx.StaticText(parent=panel,label="端口:",pos=(40, 20))
        self.portText = wx.TextCtrl(panel, -1, pos=(120,20),
                               size=(120, -1))'''
        self.userLabel = wx.StaticText(parent=panel,label="User Name:",pos=(40, 80))
        self.userText = wx.TextCtrl(panel, -1, "Entry your name",pos=(120,80),
                               size=(120, -1))
        self.passwdLabel = wx.StaticText(parent=panel, label="Password:",pos=(40, 140))
        self.passwdText = wx.TextCtrl(panel, -1, '',pos=(120, 140), style=wx.TE_PASSWORD)
        self.logs = wx.StaticText(parent=panel, label='WELCOME', pos=(200, 200), size=(80, 20))
        self.button_confirm = wx.Button(panel, label='登陆', pos=(80, 180), size=(50, 30))
        self.button_confirm.SetBackgroundColour("#87CEFA")

        self.Bind(wx.EVT_BUTTON,self.Onbutton_confirm,self.button_confirm)
        #self.button_out = wx.Button(panel, label='退出', pos=(200, 430), size=(60, 40))
        #self.Bind(wx.EVT_BUTTON,self.logout,self.button_out)
    ''''
    def logout(self,event):
        global log
        log1=0

        self.Close()
    '''''
    def Onbutton_confirm(self,event):
        global nick,pword,log
        nick = self.userText.GetValue()
        pword= self.passwdText.GetValue()
        sock.send((nick + ',' + pword).encode())
        judge = sock.recv(1024).decode()
        print(judge)
        if judge == "1":
            print("成功登录")
            log=1
            self.Close()
        else:
            #print("用户名或密码错啦。再试一次吧")
            self.logs.SetLabel("用户名或密码错啦。再试一次吧")

    def OnEraseBack(self,event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("test.jpg")
        dc.DrawBitmap(bmp, 0, 0)




class ContentFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'socket编程 对话',size=(500, 450))
        panel = wx.Panel(self, -1)
        self.yourcontent = wx.TextCtrl(panel, -1, "Entry your content",pos=(30,300),
                                       size=(400, 50),style=wx.TE_MULTILINE)
        self.allcontent = wx.StaticText(parent=panel,label="",pos=(30,20),size=(400, -1))
        self.button_send = wx.Button(panel, label='发送', pos=(330, 370), size=(50, 30))
        self.Bind(wx.EVT_BUTTON,self.DealOut,self.button_send)
        self.button_send.SetBackgroundColour("#87CEFA")
        self.button_out = wx.Button(panel, label='注销', pos=(100, 370), size=(50, 30))
        self.button_out.SetBackgroundColour("#87CEFA")
        self.Bind(wx.EVT_BUTTON, self.logout, self.button_out)

        global sock
        t = threading.Thread(target=self.DealIn, args=())
        t.setDaemon(True)
        t.start()
    def logout(self,event):
        global log2,sock
        sock.send(':exit'.encode())
        log2=0
        app.SetExitOnFrameDelete(0)


    def DealIn(self):
        global inString,sock
        while True:
            try:
                inString = sock.recv(1024).decode()
                if not inString:
                    break
                #if outString != inString:  # 自己发的
                print(inString)
                self.allcontent.SetLabel(self.allcontent.GetLabel()+'\n'+ inString)
            except:
                break
    # 发送信息
    def DealOut(self,event):
        global nick, outString ,sock
        outString = self.yourcontent.GetValue()
        outString = nick + ':' + outString
        #print(outString)
        #self.allcontent.SetLabel(outString)
        sock.send(outString.encode())
        self.yourcontent.SetValue('')


log = 0

if __name__ == '__main__':
    app = wx.App()
    ip = '10.95.222.187'
    port =8887
    sock.connect((ip, port))
    LoginFrame().Show()
    app.MainLoop()
    if log==True :
        ContentFrame().Show()
        app.MainLoop()

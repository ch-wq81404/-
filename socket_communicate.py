from tkinter import *
import socket
import time
host='10.95.222.187'
class user():
        username=''
        password=''
        def __init__(self,n,a):
                self.username=n
                self.password=a
                
class LoginPage(object):
    def __init__(self, master=None): 
        self.root = master #定义内部变量root 
        self.root.geometry('%dx%d' % (400, 240)) #设置窗口大小
        self.username = StringVar() 
        self.password = StringVar()
        global port
        port=StringVar()
        self.createPage() 

    def createPage(self): 
        self.page = Frame(self.root) #创建Frame 
        self.page.pack() 
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text = '端口: ').grid(row=1, stick=W, pady=10) 
        Entry(self.page, textvariable=port).grid(row=1, column=1, stick=E) 
        Label(self.page, text = '账户: ').grid(row=2, stick=W, pady=10) 
        Entry(self.page, textvariable=self.username).grid(row=2, column=1, stick=E) 
        Label(self.page, text = '密码: ').grid(row=3, stick=W, pady=10) 
        Entry(self.page, textvariable=self.password, show='*').grid(row=3, column=1, stick=E) 
        Button(self.page, text='登陆', command=self.loginCheck).grid(row=5, stick=W, pady=10) 
        Button(self.page, text='退出', command=self.page.quit).grid(row=5, column=1, stick=E)
    
        
    def loginCheck(self):
        _port=port.get()
        __port=int(_port)
        addr = (host,__port)               
        global c
        c= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        c.connect(addr)
        name = self.username.get() 
        secret = self.password.get()
        u=user(name,secret)
        c.send(bytes(u))
        s=str(c.recv(1),encoding='gbk')
        if(s=='1'):
            self.page.destroy() 
            MainPage(self.root)
        else:
            self.showinfo("错误","账号或密码错误!")
class MainPage(object):
    def msgsend():
        msg = '我'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n'
        txt_msglist.insert(END,msg,'green') #添加时间
        txt_msglist.insert(END,txt_msgsend.get('0.0',END)) #获取发送消息，添加文本到消息列表
        txt_msgsend.delete('0.0',END) #清空发送消息
        '''定义取消发送 消息 函数'''
    def cancel():
        txt_msgsend.delete('0.0',END) #取消发送消息，即清空发送消息
        '''绑定up键'''
    def msgsendEvent(event):
        if event.keysym == 'Up':
            msgsend()
    def __init__(event, master=None):
        event.root = master #定义内部变量root 
        event.root.geometry('%dx%d' % (700, 700)) #设置窗口大小
        f_msglist = Frame(height = 300,width = 300) #创建<消息列表分区 >
        f_msgsend = Frame(height = 300,width = 300) #创建<发送消息分区 >
        f_floor = Frame(height = 100,width = 300)   #创建<按钮分区>
        global txt_msglist
        txt_msglist= Text(f_msglist) #消息列表分区中创建文本控件
        txt_msglist.tag_config('green',foreground = 'blue') #消息列表分区中创建标签
        global txt_msgsend
        txt_msgsend= Text(f_msgsend) #发送消息分区中创建文本控件
        txt_msgsend.bind('<KeyPress-Up>',MainPage.msgsendEvent) #发送消息分区中，绑定‘UP’键与消息发送。'''
        button_send = Button(f_floor,text = 'Send',command = MainPage.msgsend) #按钮分区中创建按钮并绑定发送消息函数
        button_cancel = Button(f_floor,text = 'Cancel',command = MainPage.cancel) #分区中创建取消按钮并绑定取消函数
        f_msglist.grid(row = 0,column = 0 ) #消息列表分区
        f_msgsend.grid(row = 1,column = 0)  #发送消息分区
        f_floor.grid(row = 2,column = 0)    #按钮分区
        txt_msglist.grid()  #消息列表文本控件加载
        txt_msgsend.grid()  #消息发送文本控件加载
        button_send.grid(row = 0,column = 0,sticky = W)   #发送按钮控件加载
        button_cancel.grid(row = 0,column = 1,sticky = W) #取消按钮控件加载
        
root = Tk()
root.title('连接服务器10.95.222.187') 
LoginPage(root) 
root.mainloop()

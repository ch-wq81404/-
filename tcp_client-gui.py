from tkinter import *
import socket                   
import tkinter.messagebox
import tkinter.filedialog

HOST = "10.95.222.187"     
PORT = 5555                      
addr = (HOST,PORT)               
c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c.connect(addr)
print(c)

class Application(Frame):

    def __init__(self, master=None):        #创建一个窗口 
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
        
    def createWidgets(self):
        self.alertButton = Button(self, text='上传', bg='#ffffff',fg='black',font=('微软幼圆',20),width='12',command=self.send_file)
        self.alertButton.pack(padx=5, pady=20, side=LEFT)
        self.alertButton = Button(self, text='下载',bg='#ffffff',fg='black',font=('微软幼圆',20),width='12', command=self.get_file)
        self.alertButton.pack(padx=5, pady=20, side=LEFT)
        self.alertButton = Button(self, text='退出',bg='#ffffff',fg='black',font=('微软幼圆',20),width='12', command=self.bye)
        self.alertButton.pack(padx=5, pady=20, side=LEFT)

    def bye(self):
        cmd="bye"
        c.send(bytes(cmd,encoding='gbk'))
        c.close()
        
    def send_file(self):
        cmd="upload"
        c.send(bytes(cmd,encoding='gbk')) 
        filepath=tkinter.filedialog.askopenfilename()
        if filepath==(""):
            tkinter.messagebox.showinfo('消息提醒','无效文件')
            c.close()
            app.destroy()
        with open(filepath,"rb") as f:
            file = f.read()
            c.sendall(file)
        c.close()
        tkinter.messagebox.showinfo('消息提醒','上传成功')
        app.destroy()
        
    def get_file(self):
        cmd="down"
        c.send(bytes(cmd,encoding='gbk')) 
        filepath=tkinter.filedialog.askopenfilename()
        if filepath==(""):
            tkinter.messagebox.showinfo('消息提醒','无效文件')
            c.close()
            app.destroy()
        c.send(bytes(filepath,encoding='gbk')) 
        data = c.recv(20480)                     
        with open("D:\\recv.txt","a+") as f:
            sdata=str(data,encoding='gbk')
            f.write(sdata)
        c.close()
        tkinter.messagebox.showinfo('消息提醒','下载成功')
        app.destroy()
        
app = Application()
app.master.title('上传下载文件')
app.mainloop()

#coding=utf-8
import psutil
from tkinter import *
from tkinter import ttk
from scapy.all import *
import dpkt
import datetime
import socket

NIC=[("WLAN","Intel(R) Dual Band Wireless-AC 3165"),("以太网","Realtek PCIe GBE Family Controller")
     ,("VMware Network Adapter VMnet1","VMware Network Adapter VMnet1")]
class code(object):
    def __init__(self, master=None): 
        self.root = master #定义内部变量root 
        self.root.geometry('%dx%d' % (1100, 800)) #设置窗口大小
        self.page = Frame(self.root) #创建Frame 
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Input = Frame(self.page,height = 200,width = 800)
        Input.grid(row=1)
        Label(Input).grid(row=0, stick=W)
        Label(Input,font='Consolas', foreground='#000080',text = '* 网卡: ').grid(row=1,stick=W, pady=10)
        global ncChosen
        ncChosen=ttk.Combobox(Input)
        ncChosen['values']=netcard_info
        ncChosen.grid(row=1,column=1,stick=E)
        Label(Input,font='Consolas', foreground='#000080',text = '* 源地址: ').grid(row=1,column=2,stick=W, pady=10,padx=20) 
        Entry(Input, font='Consolas',textvariable=source
              ).grid(row=1,column=3, stick=E)
        Label(Input,font='Consolas', foreground='#000080',text = '* 目标地址: ').grid(row=1,column=4,stick=W, pady=10,padx=20) 
        Entry(Input, font='Consolas',textvariable=desti
              ).grid(row=1,column=5, stick=E)
        Button(Input, font='Consolas',text='抓包', command=self.catch,
               foreground='#000080').grid(row=2, column=5, pady=10)
        
        Output = Frame(self.page,width = 800)  #输出区间
        Output.grid(row=2)
        Label(Output,font='Consolas',text='* 包列表:',foreground='#000080').grid(row=0,column=0,stick=W)
        global txt
        txt=Listbox(Output,width=73,height=10,font='Consolas')
        txt.grid(row=1,column=1,stick=W)
        txt.bind('<Double-Button-1>',self.click)
        txt.curIndex = None

        
        Details=Frame(self.page,width=800)   #详情区间
        Details.grid(row=3)
        global detail
        Label(Details,font='Consolas',text='* 详 情:',foreground='#000080').grid(row=0,column=0,stick=W)
        detail=Text(Details,font="Consolas",width=73,height=10)
        detail.grid(row=1,column=1,stick=W)
        
    def get_netcard():
        info = psutil.net_if_addrs()
        for k,v in info.items():
            for item in v:
                if item[0] == 2 and not item[1]=='127.0.0.1':
                    netcard_info.append((k))
                    
    def catch(self):
        global ncChosen
        global dpk
        card=ncChosen.get()
        src=source.get()
        dst=desti.get()
        _filter="ip"
        if(src!=""):
            _filter+=" and src "+src
            if(dst!=""):
                _filter+=" and dst "+dst
        for i in NIC: 
            if i[0]==card:
                print("过滤器内容为："+_filter)
                if(_filter!=""):
                    dpk = sniff(filter=_filter,iface=i[1],count = 10)
                else:
                    dpk = sniff(iface=i[1],count = 10)
                wrpcap("I:\demo.pcap", dpk)
        print ("抓包成功，开始分析")
        print(dpk)
        
        global txt
        txt.delete(0,END)
        for i in range(0,10):
            print(dpk[i][Ether].type)
            if(dpk[i][Ether].type==2048):
                msg="  "+str(i+1)+". src:"+str(dpk[i][IP].src)+"  dst:"+str(dpk[i][IP].dst)+"  proto:"+str(dpk[i][IP].proto)+"  len:"+str(dpk[i][IP].len)+'\n'
            elif(dpk[i][Ether].type==2054):
                msg="  "+str(i+1)+". src:"+str(dpk[i][Ether].src)+"  dst:"+str(dpk[i][Ether].dst)+"  proto:arp  len:56\n"     
            else:
                msg="  "+str(i+1)+".\n"
            txt.insert(END,msg)
            txt.itemconfig(i)
            if not i%2:
                txt.itemconfig(i,bg="#FAF0E6")
           
    def click(self,txt):
        w = txt.widget
        i=str(w.curselection()[0]+1)
        global detail
        global dpk
        _dpk=str(dpk)
        detail.delete('0.0',END)
        detail.insert(END,"第"+i+"个抓到的包:\n")
        i=int(i)-1
        detail.insert(END,"Ether: dst="+str(dpk[i][Ether].dst)+"  src="+str(dpk[i][Ether].src)+'\n')
        if(dpk[i][Ether].type==2048):
            detail.insert(END,"IP: version="+str(dpk[i][IP].version)+"  len="+str(dpk[i][IP].len)+"  id="+str(dpk[i][IP].id)
                     +"  flags="+str(dpk[i][IP].flags)+"  ttl="+str(dpk[i][IP].ttl)+'\n')
            if(dpk[i][IP].proto==6):
                a='TCP'
                detail.insert(END,a+": sport="+str(dpk[i][a].sport)+" dport="+str(dpk[i][a].dport)+" ack="+str(dpk[i][a].ack)+" seq="+str(dpk[i][a].seq)+" chksum="+str(dpk[i][a].chksum)+" win="+str(dpk[i][a].window)+'\n') 
            elif(dpk[i][IP].proto==17):
                a='UDP'
                detail.insert(END,a+": sport="+str(dpk[i][a].sport)+" dport="+str(dpk[i][a].dport)+" chksum="+str(dpk[i][a].chksum)+'\n') 
        elif(dpk[i][Ether].type==2054):
            detail.insert(END,"ARP: op="+str(dpk[i][ARP].op)+"  pdst="+str(dpk[i][ARP].pdst)+'\n'+"Info:Who has "+str(dpk[i][ARP].pdst)+"? Tell "+str(dpk[i][ARP].psrc))
            
        
        
    
root = Tk()
root.title('IPv4抓包实现')
netcard_info = []
global ncChosen
global txt
global dpk
desti=StringVar()
source=StringVar()
code.get_netcard()
code(root)
root.mainloop()

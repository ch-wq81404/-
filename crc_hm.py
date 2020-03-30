import math
from tkinter import *

class code(object):
    def __init__(self, master=None): 
        self.root = master #定义内部变量root 
        self.root.geometry('%dx%d' % (830, 500)) #设置窗口大小
        self.page = Frame(self.root) #创建Frame 
        self.page.pack() 
        Label(self.page).grid(row=0, stick=W)
        Label(self.page,font='黑体', foreground='#000080',text = '* 数 据: ').grid(row=1,stick=W, pady=10) 
        Entry(self.page,font='黑体',textvariable=_cdata,
              ).grid(row=1,column=1, stick=E) 
        Label(self.page,font='黑体', foreground='#000080',text = '* 编 码: ').grid(row=2,stick=W, pady=10) 
        Entry(self.page, font='黑体',textvariable=_cs
              ).grid(row=2,column=1, stick=E)
        Button(self.page, font='黑体',text='crc编码', command=self.main,
               foreground='#000080').grid(row=5, column=1, pady=10)
        
        Label(self.page,font='黑体', foreground='#000080',text = '* 用CRC\n方法检错: ').grid(row=6,stick=W, pady=30)
        Entry(self.page,font='黑体',textvariable=_crctest,
              ).grid(row=6,column=1, stick=E)
        Button(self.page, font='黑体',text='检错', command=self.crctest,
               foreground='#000080').grid(row=6, column=2, pady=10)
        Label(self.page,font='黑体', foreground='#000080',text='检错结果:'
              ).grid(row=7)
        Label(self.page,font='黑体', textvariable= _crcresult
              ).grid(row=7,stick=W, column=1,pady=10)
        
        Label(self.page, font='黑体',foreground='#000080',text = '* 数  据: ').grid(row=1,column=2,stick=W, pady=10,padx=20) 
        Entry(self.page,font='黑体',textvariable=_data
              ).grid(row=1, column=3, stick=E)
        Label(self.page, font='黑体',foreground='#000080',text = '* 编  码: ').grid(row=2,column=2,stick=W, pady=10,padx=20) 
        Entry(self.page,font='黑体', textvariable=_s
              ).grid(row=2, column=3, stick=E)
        Button(self.page, font='黑体',text='海明码', command=self._main,
               foreground='#000080').grid(row=5, column=3, pady=10)
        
        Label(self.page,font='黑体', foreground='#000080',text = '* 用海明\n码纠错: ').grid(row=8,stick=W,pady=20)
        Entry(self.page,font='黑体',textvariable=_hmtest,
              ).grid(row=8,column=1, stick=E,pady=10)
        Button(self.page, font='黑体',text='纠错', command=self.hmtest,
              foreground='#000080').grid(row=8, column=2,pady=10)
        Label(self.page,font='黑体', foreground='#000080',text='纠错结果:'
              ).grid(row=9, pady=10)
        Label(self.page,font='黑体', textvariable = _hmresult
              ).grid(row=9,stick=W,column=1,columnspan=100,pady=10)
        
    def main(self):     #用异或的方式实现模2运算 a:余数 fcs：除数 cdata：被除数
        cdata=_cdata.get()      
        cdata+="000"
        l=len(cdata)
        a=cdata[0:4]
        fcs='1101'
        d=0
        b=[0,0,0,0]
        while True:
            i=0
            if a[0]=='1':
                while i<4:
                    b[i]=int(fcs[i])^int(a[i])
                    i+=1
                d+=1
                if l-d==3:
                    break
                a=''
                for i in range(1,4,1):
                    a+=str(b[i])
                a+=cdata[3+d]
            elif a[0]=='0':
                while i<4:
                    b[i]=0^int(a[i])
                    i+=1
                d+=1
                if l-d==3:
                    break
                a=''
                for i in range(1,4,1):
                    a+=str(b[i])
                a+=cdata[3+d]
        a=''
        for i in range(1,4,1):
            a+=str(b[i])
        s=cdata[0:l-3]+a
        _cs.set(s)
        
    def crctest(self):          #判断余数a是否为0
        crcresult='无差错'
        crctest=_crctest.get()
        l=len(crctest)
        a=crctest[0:4]
        fcs='1101'
        d=0
        b=[0,0,0,0]
        while True:
            i=0
            if a[0]=='1':
                while i<4:
                    b[i]=int(fcs[i])^int(a[i])
                    i+=1
                d+=1
                if l-d==3:
                    break
                a=''
                for i in range(1,4,1):
                    a+=str(b[i])
                a+=crctest[3+d]
            elif a[0]=='0':
                while i<4:
                    b[i]=0^int(a[i])
                    i+=1
                d+=1
                if l-d==3:
                    break
                a=''
                for i in range(1,4,1):
                    a+=str(b[i])
                a+=crctest[3+d]
        for i in range(0,4,1):
            if b[i]==1:
                crcresult='有差错'
                break
        _crcresult.set(crcresult)
        
    def _main(self):
        data=_data.get()
        k=int(len(data))
        r=0
        i=1
        while i!=0:
            temp=pow(2,r)
            temp=temp-1
            if temp>=r+k:
                i=0
            else:
                r=r+1
        i=0
        j=0
        l=1
        s='3'
        while i<k:          #假设冗余码全为1，插入原数据
            if l==pow(2,j):
                s=s+'1'
                j+=1
                l+=1
            else:
                s=s+data[i]
                i=i+1
                l+=1
        sum=0
        i=0
        while i<r:         #计算冗余码实际的值：例如计算R0，从后一位开始判断下标二进制中最低位是否为1，为1则异或
            j=pow(2,i)+1
            while j<r+k+1:
                _b=bin(j)
                b=_b[::-1]
                if b[i]=='1' and j==pow(2,i)+1:
                    sum=int(s[j])
                    j+=1
                elif b[i]=='1':
                    sum=sum^int(s[j])
                    j+=1
                else:
                    j+=1
            s=s[:pow(2,i)]+str(sum)+s[(pow(2,i)+1):]
            i+=1
        s=s[1:r+k+1]
        _s.set(s)

    def hmtest(self):         #与生成的算法相似，不同点在于异或时加上冗余码
        r=i=0
        hmtest=_hmtest.get()
        l=len(hmtest)
        while i!=1:
            temp=pow(2,r)
            temp=temp-1
            if temp>=l:
                i=1
            else:
                r=r+1        
        hmtest='3'+hmtest[0:len(hmtest)]
        a=''
        m=i=sum=0
        while i<r:
            j=pow(2,i)
            while j<l+1:
                _b=bin(j)
                b=_b[::-1]
                if b[i]=='1' and j==pow(2,i):
                    sum=int(hmtest[j])
                    j+=1
                elif b[i]=='1':
                    sum=sum^int(hmtest[j])
                    j+=1
                else:
                    j+=1
            a+=str(sum)
            i+=1
        a=eval('0b'+a[::-1])
        if(a==0):
            hmresult='无差错'
        else:
            if hmtest[a]=='1':
                hmtest=hmtest[:a]+'0'+hmtest[a+1:]
            else:
                hmtest=hmtest[:a]+'1'+hmtest[a+1:]
            hmresult="第"+str(a)+"位出现差错,纠正后的数据为:"+hmtest[1:]
        _hmresult.set(hmresult)

root = Tk()
root.title('crc以及海明码实现')
r=0
_data=StringVar()
_s=StringVar()
_cs=StringVar()
_cdata=StringVar()
_hmtest=StringVar()
_crctest=StringVar()
_hmresult=StringVar()
_crcresult=StringVar()
code(root)
root.mainloop()

        
            
        

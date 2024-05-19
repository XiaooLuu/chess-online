import sys
from socket import *
from tkinter import *
import json
import threading as td
import time
from tkinter import messagebox
import random
#const
clientDict={1:'ChessListWhite',2:'ChessListBlack'}
MessageNumber=int(0)



#构建GUI画面
ServerWindows=Tk()
ServerWindows.geometry('400x250')
ServerWindows.title('Server')
EchoLabel=Label(ServerWindows)
EchoLabel.place(x=0,y=0,width=300,height=250)
EchoLabel.config(relief='groove')

SideLabel=Label(ServerWindows,text='已连接客户端\n------------------')
SideLabel.place(x=300,y=0,width=100,height=200)
SideLabel.config(relief='groove')
SideLabel.config(anchor='n')
OnlineLabel=Label(ServerWindows,text='✉',font=('',40,''))
OnlineLabel.place(x=10,y=10,width=50,height=50)
OnlineLabel.config(fg='red')


#Socket对象

ListenSocket=socket(AF_INET,SOCK_STREAM)



def Recv(selfsocket:socket,targetsocket:socket):
    global MessageNumber
    while True:
        ClientMessage = selfsocket.recv(1024).decode()
        if ClientMessage:
            print(ClientMessage)

            targetsocket.send(ClientMessage.encode())
            MessageNumber+=1
            EchoLabel.config(text=f'通讯中,已转接{MessageNumber}条信息',font=('楷体',15,''))



def Talk(selfsocket:socket,message:str)->None:
    selfsocket.send(message.encode())










def IsOnline(x):
    while True:
        OnlineLabel.config(fg='green')
        time.sleep(0.5)
        OnlineLabel.config(fg='yellow')
        time.sleep(0.5)




def Main(x):
    try:
        PORT = json.load(open('./server.json', 'r'))["PORT"]
    except:
        messagebox.showinfo('错误','找不到\'server.json\'!')
        ServerWindows.withdraw()
        ServerWindows.update()
    try:
        ListenSocket.bind(('', int(PORT)))
        EchoLabel['text'] = '服务器成功创建\n等待第一个客户端连接...'
        c1=random.randint(1,2)
        c2=3-c1
        ListenSocket.listen(2)
        client1,addr=ListenSocket.accept()
        EchoLabel['text']=f'一个客户端连接\n{addr}\n已连接客户端数量:1'
        client1.send('ChessListWhite'.encode())
        SideLabel['text']='已连接客户端\n------------------\n客户端1'
        ListenSocket.listen(2)
        client2, addr = ListenSocket.accept()
        EchoLabel['text'] = f'一个客户端连接\n{addr}\n已连接客户端数量:2\n'
        client2.send('ChessListBlack'.encode())
        SideLabel['text'] = '已连接客户端\n------------------\n客户端1\n------------------\n客户端2'
        Trecv1=td.Thread(target=Recv,args=(client1,client2))
        Trecv2 = td.Thread(target=Recv, args=(client2, client1))
        TIsOnline=td.Thread(target=IsOnline,args=(1,))
        Trecv2.start()
        Trecv1.start()
        TIsOnline.start()
        EchoLabel.config(text=f'通讯中,已转接{MessageNumber}条信息',font=('楷体',15,''))



    except BaseException as e:
        EchoLabel['text'] = '错误!'
        print(e)


TMain=td.Thread(target=Main,args=(1,))
TMain.start()


try:
    ServerWindows.mainloop()
except:
    sys.exit()

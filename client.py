
import time
from tkinter import *
from const import *
import json
from socket import *
import threading as td
from tkinter import messagebox

#GUI



window_Client=Tk()
window_Client.geometry('300x200')
window_Client.title('connect to server...')
etr_Client_IP=Entry(window_Client)
etr_Client_PORT=Entry(window_Client)
etr_Client_IP.place(x=40,y=75,width=120,height=30)
etr_Client_PORT.place(x=170,y=75,width=60,height=30)
lab_Client_IP=Label(window_Client,text='HOST',font=('楷体',12,''))
lab_Client_PORT=Label(window_Client,text='PORT',font=('楷体',12,''))
lab_Client_IP.place(x=40,y=45,width=120,height=30)
lab_Client_PORT.place(x=170,y=45,width=60,height=30)
window_Client.update()




data=socket(AF_INET,SOCK_STREAM)

def Connect(x):
    global IsConnectToServer
    try:
        data.connect((etr_Client_IP.get(),int(etr_Client_PORT.get())))
        etr_Client_PORT.place_forget()
        etr_Client_IP.place_forget()
        labshow=Label(window_Client,text='连接中',font=('',30,''))
        labshow.place(x=0,y=0,width=300,height=200)
        IsConnectToServer=True


    except BaseException as e:
        labshow = Label(window_Client, text='连接失败', font=('', 30, ''))
        labshow.place(x=0, y=0, width=300, height=200)
        print(e)

window_Client.bind('<Return>',Connect)





while IsConnectToServer==False:
    window_Client.update()

which=data.recv(1024).decode()
if which=="ChessListWhite":
    ChessList=ChessListWhite
    TURN=False
elif which=="ChessListBlack":
    ChessList=ChessListBlack
    TURN=True

window_Client.withdraw()


Windows=Tk()
Windows.geometry('550x400')
Windows.title('Chess')
Windows.withdraw()
PawnGodLabel=Label(Windows)
PawnGodLabel.place(x=400,y=300,width=150,height=100)
WinDebug=Tk()
WinDebug.geometry('400x300+800+300')
WinDebug.title('Debug')
LabelDebug=Label(WinDebug)
LabelDebug.place(x=0,y=0,width=300,height=300)
LabelDebug.config(anchor='nw',relief='sunken')
LabelDebugNum=Label(WinDebug)
LabelDebugNum.place(x=300,y=0,width=100,height=300)
LabelSide=Label(Windows)
LabelSide.place(x=400,y=0,width=150,height=200)





LabelName='EchoLabel'
for i in range(8):
    for j in range(8):
        Name=LabelName+f'{i}{j}'
        Name=Label(Windows)
        Name.config(relief='groove')
        Name.place(x=j*50,y=i*50,width=50,height=50)
        EchoLabelList[i][j]=Name











def moveChess(chesslist:list,targetChess:tuple,MoveToLocation:tuple):
    global PawnRoad
    x,y=targetChess[0],targetChess[1]
    targetChessStr=chesslist[x][y]
    chesslist[x][y]='empty'
    if chesslist[MoveToLocation[0]][MoveToLocation[1]]!='empty':
        if chesslist[MoveToLocation[0]][MoveToLocation[1]][0]=='!':
            DeathListEnemy.append(chesslist[MoveToLocation[0]][MoveToLocation[1]])
        elif chesslist[MoveToLocation[0]][MoveToLocation[1]][0]=='?':
            DeathListLocal.append(chesslist[MoveToLocation[0]][MoveToLocation[1]])
    chesslist[MoveToLocation[0]][MoveToLocation[1]]=targetChessStr
    if targetChessStr=='!Pawn' and MoveToLocation[0]==4:
        PawnRoad[MoveToLocation[1]]=2
        print(PawnRoad)
    else:
        for i in range(8):
            if PawnRoad[i]==2:
                PawnRoad[i]=0
                print(PawnRoad)
    if targetChessStr == '?Pawn' and y==MoveToLocation[1]:
        if MoveToLocation[0]==4:
            PawnRoad[MoveToLocation[1]] = 1
            print(PawnRoad)
        else:
            PawnRoad[MoveToLocation[1]] = 0
            print(PawnRoad)
    elif y!=MoveToLocation[1]:
        PawnRoad[y],PawnRoad[MoveToLocation[1]]=0,0



def Debug(textin):
    global DebugText,DebugTextList,DebugNum
    DebugText=''
    DebugNum+=1
    DebugTextList.append(textin)
    if len(DebugTextList)>16:
        DebugTextList=DebugTextList[1:]
    for i in DebugTextList:
        DebugText+=f'\n{i}'
    LabelDebugNum.config(text=f'{DebugNum}',font=('',30,''))






def printChess():
    for i in range(8):
        for j in range(8):
            print('\t'+ChessList[i][j]+'\t|',end='')
        print('\n'+'-'*97)
    print('DeathLocal:',DeathListLocal)
    print('DeathEnemy:',DeathListEnemy)



def Update(chesslist:list):
    for i in range(8):
        for j in range(8):
            if chesslist[i][j]!='empty':
                if chesslist==ChessListWhite:
                    EchoLabelList[i][j].config(text=str(ChessStrDict[chesslist[i][j][1:]][White[chesslist[i][j][0]]]), font=('', 25, ''))
                else:
                    EchoLabelList[i][j].config(text=str(ChessStrDict[chesslist[i][j][1:]][Black[chesslist[i][j][0]]]), font=('', 25, ''))
            else:
                EchoLabelList[i][j].config(text='')
            if (i+j)%2==0:
                EchoLabelList[i][j].config(bg='gray')
            else:
                EchoLabelList[i][j].config(bg='white')
    Windows.update()






def FlaskMove(key):
    global TargetChess,CanMoveToList,CanMove,ChooseNum,CanBeGod
    if TURN==True:
        CanMoveToList=[]
        CanMove=False
        PawnGodLabel.config(text='')
        CanBeGod = [False, False, False, False, False, False, False, False]
        ChooseNum=0
        keyValue = FlaskMoveDict[key]
        Tx,Ty=TargetChess[0],TargetChess[1]
        Kx,Ky=keyValue[0],keyValue[1]
        MoveToPosition=(Tx+Kx,Ty+Ky)
        if (MoveToPosition[0] in range(8)) and (MoveToPosition[1] in range(8)):
            # 还原棋盘颜色
            for i in range(8):
                for j in range(8):
                    if (i + j) % 2 == 0:
                        EchoLabelList[i][j].config(bg='gray')
                    else:
                        EchoLabelList[i][j].config(bg='white')

            if ChessList[Tx][Ty]=='empty':
                EchoLabelList[Tx][Ty]['text']=''

            TargetChess=MoveToPosition
            Tx, Ty = TargetChess[0], TargetChess[1]
            if ChessList[Tx][Ty]=='empty':
                EchoLabelList[Tx][Ty].config(text='¤',font=('',25,''))
            EchoLabelList[Tx][Ty].config(bg='yellow')
            print(f'TargetChess:{TargetChess}')

            #智能走位提示
            if ChessList[Tx][Ty][0]=='?':
                #小兵
                if ChessList[Tx][Ty]=='?Pawn':
                    Debug(f'操作{Tx},{Ty}的小兵')
                    if Tx >0:
                        if ChessList[Tx-1][Ty]!='empty' and ChessList[Tx-1][Ty][0]=='!':
                            Debug(f'小兵前方棋子为对方棋子 {ChessList[Tx-1][Ty][1:]}')
                        elif ChessList[Tx-1][Ty]=='empty':
                            EchoLabelList[Tx-1][Ty].config(bg='green')
                            CanMoveToList.append((Tx-1,Ty))
                            if Tx == 6:
                                Debug('小兵可以移动两格')
                                if ChessList[Tx-2][Ty]!='empty' and ChessList[Tx-2][Ty][0]=='!':
                                    Debug(f'小兵前方棋子为对方棋子 {ChessList[Tx-2][Ty][1:]}')
                                elif ChessList[Tx-2][Ty]=='empty':
                                    Debug('小兵前方无棋子')
                                    EchoLabelList[Tx-2][Ty].config(bg='green')
                                    CanMoveToList.append((Tx-2,Ty))
                        if PawnRoad[Ty]==1:
                            for i in [1,-1]:
                                if Ty+i in range(8) and PawnRoad[Ty+i]==2:
                                    EchoLabelList[Tx][Ty+i].config(bg='purple')
                                    CanMoveToList.append((Tx,Ty+i))
                        for i in [1,-1]:
                            if (Ty+i in range(8)) and (ChessList[Tx-1][Ty+i]!='empty' and ChessList[Tx-1][Ty+i][0]=='!'):
                                EchoLabelList[Tx-1][Ty + i].config(bg='yellow')
                                CanMoveToList.append((Tx-1, Ty+i))
                                Debug(f'{Tx-1},{Ty+i}有敌方棋子')
                    elif Tx==0:
                        CanBeGod[Ty]=True
                        PawnGodLabel.config(text='♛♜♞♝\nQ W E R', font=('', 20, ''))
                        print(CanBeGod)

                if ChessList[Tx][Ty] == '?Knight':
                    Debug(f'操作{Tx},{Ty} 马')
                    for i in [(Tx-1,Ty+2),(Tx+1,Ty+2),(Tx-1,Ty-2),(Tx+1,Ty-2),(Tx+2,Ty-1),(Tx+2,Ty+1),(Tx-2,Ty-1),(Tx-2,Ty+1)]:
                        if  i[0] in range(8) and i[1] in range(8):
                            if ChessList[i[0]][i[1]]!='empty' and ChessList[i[0]][i[1]][0]=='!':
                                Debug('')
                                EchoLabelList[i[0]][i[1]].config(bg='red')
                                CanMoveToList.append((i[0],i[1]))
                            elif ChessList[i[0]][i[1]]=='empty':
                                EchoLabelList[i[0]][i[1]].config(bg='green')
                                CanMoveToList.append((i[0], i[1]))

                if ChessList[Tx][Ty] == '?Rook':
                    Debug(f'操作{Tx},{Ty} 车')
                    for i in [(1,0),(-1,0),(0,1),(0,-1)]:
                        Vx, Vy = Tx, Ty
                        while True:
                            Vx+=i[0]
                            Vy+=i[1]
                            if not (Vx in range(8)) or not (Vy in range(8)):
                                break
                            if ChessList[Vx][Vy]!='empty' and ChessList[Vx][Vy][0]=='!':
                                EchoLabelList[Vx][Vy].config(bg='yellow')
                                CanMoveToList.append((Vx,Vy))
                                break
                            elif ChessList[Vx][Vy]=='empty':
                                EchoLabelList[Vx][Vy].config(bg='green')
                                CanMoveToList.append((Vx, Vy))
                            if ChessList[Vx][Vy][0]=='?':
                                break

                if ChessList[Tx][Ty]== '?Bishop':
                    Debug(f'操作{Tx},{Ty} 象')
                    for i in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                        Vx, Vy = Tx, Ty
                        while True:
                            Vx += i[0]
                            Vy += i[1]
                            if not (Vx in range(8)) or not (Vy in range(8)):
                                break
                            if ChessList[Vx][Vy] != 'empty' and ChessList[Vx][Vy][0] == '!':
                                EchoLabelList[Vx][Vy].config(bg='yellow')
                                CanMoveToList.append((Vx, Vy))
                                break

                            elif ChessList[Vx][Vy] == 'empty':
                                EchoLabelList[Vx][Vy].config(bg='green')
                                CanMoveToList.append((Vx, Vy))
                            if ChessList[Vx][Vy][0]=='?':
                                break

                if ChessList[Tx][Ty]== '?Queen':
                    Debug(f'操作{Tx},{Ty} 后')
                    for i in [(1, 1), (-1, 1), (1, -1), (-1, -1),(1,0),(-1,0),(0,1),(0,-1)]:
                        Vx, Vy = Tx, Ty
                        while True:
                            Vx += i[0]
                            Vy += i[1]
                            if not (Vx in range(8)) or not (Vy in range(8)):
                                break
                            if ChessList[Vx][Vy] != 'empty' and ChessList[Vx][Vy][0] == '!':
                                EchoLabelList[Vx][Vy].config(bg='yellow')
                                CanMoveToList.append((Vx, Vy))
                                break
                            elif ChessList[Vx][Vy] == 'empty':
                                EchoLabelList[Vx][Vy].config(bg='green')
                                CanMoveToList.append((Vx, Vy))
                            if ChessList[Vx][Vy][0]=='?':
                                break
                if ChessList[Tx][Ty]== '?King':
                    Debug(f'操作{Tx},{Ty} 王')
                    for i in[(1, 1), (-1, 1), (1, -1), (-1, -1),(1,0),(-1,0),(0,1),(0,-1)]:
                        Vx,Vy=Tx+i[0],Ty+i[1]
                        if not (Vx in range(8)) or not (Vy in range(8)):
                            continue
                        if ChessList[Vx][Vy]!='empty' and ChessList[Vx][Vy][0]=='!':
                            EchoLabelList[Vx][Vy].config(bg='yellow')
                            CanMoveToList.append((Vx,Vy))
                        elif ChessList[Vx][Vy]=='empty':
                            EchoLabelList[Vx][Vy].config(bg='green')
                            CanMoveToList.append((Vx,Vy))

                    if IsKingMove==False:
                        if IsRook1Move==False:
                            for i in range(1,4):
                                if ChessList[7][i]=='empty' or ChessList[7][i]=='?King':
                                    if not ((7,1) in CanMoveToList):
                                        CanMoveToList.append((7,1))
                                else:
                                    if ((7, 1) in CanMoveToList):
                                        CanMoveToList.remove((7,1))
                                    break
                            if ((7, 1) in CanMoveToList):
                                EchoLabelList[7][1].config(bg='purple')
                        if IsRook2Move == False:
                            for i in range(4,7):
                                if ChessList[7][i]=='empty' or ChessList[7][i]=='?King':

                                    print(1)
                                    if not ((7, 6) in CanMoveToList):
                                        CanMoveToList.append((7, 6))
                                else:
                                    if ((7, 6) in CanMoveToList):
                                        CanMoveToList.remove((7,6))
                                    break
                        if ((7, 6) in CanMoveToList):
                            EchoLabelList[7][6].config(bg='purple')



            CanMoveNum=len(CanMoveToList)//4
            Debug('可以移动:')
            for i in range(CanMoveNum):
                Debug(CanMoveToList[i*4:(i+1)*4])
            Debug(CanMoveToList[CanMoveNum*4:])



class PlayerView:
    @staticmethod
    def Up(x):
        FlaskMove('up')
    @staticmethod
    def Down(x):
        FlaskMove('down')
    @staticmethod
    def Left(x):
        FlaskMove('left')
    @staticmethod
    def Right(x):
        FlaskMove('right')
    @staticmethod
    def Choose(x):
        global ChooseNum,CanMoveToPosition,CanMove
        if TURN==True:
            if len(CanMoveToList) != 0:
                CanMove=True
                CanMoveToPosition=tuple(())
                for i in range(8):
                    for j in range(8):
                        if (i + j) % 2 == 0:
                            EchoLabelList[i][j].config(bg='gray')
                        else:
                            EchoLabelList[i][j].config(bg='white')

                if ChooseNum > len(CanMoveToList)-1:
                    ChooseNum = 0
                CanMoveToPosition = CanMoveToList[ChooseNum]
                EchoLabelList[CanMoveToPosition[0]][CanMoveToPosition[1]].config(bg='orange')
                ChooseNum += 1
                print(f'CanMoveToPosition:{CanMoveToPosition}')


    @staticmethod
    def Move(x):
        global CanMove,CanMoveToPosition,CanMoveToList,ChooseNum,SocketMessage,IsRook1Move,IsKingMove,IsRook2Move,TURN
        if TURN==True:
            if CanMove==True:
                for i in range(8):
                    for j in range(8):
                        if (i + j) % 2 == 0:
                            EchoLabelList[i][j].config(bg='gray')
                        else:
                            EchoLabelList[i][j].config(bg='white')



                if IsKingMove==False and ChessList[TargetChess[0]][TargetChess[1]]=='?King':
                    if CanMoveToPosition==(7,6) and IsRook2Move==False:
                        moveChess(ChessList,(7,7),(7,5))
                        SocketMessage.append(f'm7775')
                        data.send('k7775'.encode())
                    if CanMoveToPosition==(7,1) and IsRook1Move==False:
                        moveChess(ChessList,(7,0),(7,2))
                        SocketMessage.append(f'm7072')
                        data.send('k7072'.encode())


                if ChessList[TargetChess[0]][TargetChess[1]]=='?King':
                    IsKingMove=True
                    Debug('King->moved')
                if ChessList[TargetChess[0]][TargetChess[1]] == '?Rook':
                    if TargetChess[1]==0:
                        IsRook1Move=True
                        Debug('Rook1->moved')
                    elif TargetChess[1]==7:
                        IsRook2Move=True
                        Debug('Rook2->moved')

                moveChess(ChessList, TargetChess, CanMoveToPosition)
                data.send(f'm{TargetChess[0]}{TargetChess[1]}{CanMoveToPosition[0]}{CanMoveToPosition[1]}'.encode())
                TURN=False
                CanMoveToPosition == tuple(())
                CanMoveToList=[]
                ChooseNum=0
                CanMove=False
                Update(ChessList)
                SocketMessage.append(f'm{TargetChess[0]}{TargetChess[1]}{CanMoveToPosition[0]}{CanMoveToPosition[1]}')
                Debug('Socket:')
                for i in range(len(SocketMessage)//4):
                    Debug(SocketMessage[i * 4:(i + 1) * 4])
                Debug(SocketMessage[(len(SocketMessage)//4) * 4:])
                Debug(PawnRoad)
    @staticmethod
    def BeGod(key):
        global CanBeGod
        if (True in CanBeGod) and TURN==True:
            y=CanBeGod.index(True)
            ChessList[TargetChess[0]][y]=BeGodDict[key]
            Update(ChessList)
            EchoLabelList[TargetChess[0]][y].config(bg='blue')
            data.send(f'g{TargetChess[0]}{y}{BeGodDict[key]}'.encode())
            CanBeGod=[False,False,False,False,False,False,False,False]

    @staticmethod
    def Queen(x):
        PlayerView.BeGod('q')

    @staticmethod
    def Rook(x):
        PlayerView.BeGod('w')

    @staticmethod
    def Knight(x):
        PlayerView.BeGod('e')

    @staticmethod
    def Bishop(x):
        PlayerView.BeGod('r')



Windows.bind('<Return>',PlayerView.Move)
Windows.bind('<Tab>',PlayerView.Choose)
Windows.bind('<Up>', PlayerView.Up)
Windows.bind('<Down>', PlayerView.Down)
Windows.bind('<Left>', PlayerView.Left)
Windows.bind('<Right>', PlayerView.Right)
Windows.bind('q',PlayerView.Queen)
Windows.bind('w',PlayerView.Rook)
Windows.bind('e',PlayerView.Knight)
Windows.bind('r',PlayerView.Bishop)



def RECV(x):
    print('trcv')
    global TURN,ChessList
    while True:
        recvmsg=data.recv(1024).decode()
        if recvmsg:
            a,b,c,d=recvmsg[1],recvmsg[2],recvmsg[3],recvmsg[4]
            if recvmsg[0]=='m':
                moveChess(ChessList,(7-int(a),7-int(b)),(7-int(c),7-int(d)))
                TURN=True
            if recvmsg[0]=='k':
                moveChess(ChessList, (7-int(a), 7-int(b)), (7-int(c), 7-int(d)))
            if recvmsg[0]=='g':
                ChessList[7-int(a)][7-int(b)]=recvmsg[3:]



TRECV=td.Thread(target=RECV,args=(1,))

def Isloop(x):
    while True:
        if TURN==False:
            TRECV.start()


TIsloop=td.Thread(target=RECV,args=(1,))
TIsloop.start()

#############################################



Update(ChessList)
Windows.deiconify()


WinDebug.withdraw()
while True:
    if TURN==False:
        LabelSide.config(text='等待对方落子...',font=('楷体',15,''),fg='red')
        ud=0
    if TURN==True and ud==0:
        LabelSide.config(text='该你落子...', font=('楷体', 15, ''),fg='green')
        ud=1
    if ud==1:
        Update(ChessList)
        ud=2
    Windows.update()
    CLIST=[]
    for i in ChessList:
        CLIST=CLIST+i
    if not ('!King' in CLIST):
        Windows.withdraw()
        messagebox.showinfo('chess','你赢了')
        break
    if not ('?King' in CLIST):
        Windows.withdraw()
        messagebox.showinfo('chess','菜就多练')
        break




#############################################



#棋子列表 const
IsConnectToServer=False
ud=0
EchoLabelList=[['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','','']]
IsKingMove,IsRook1Move,IsRook2Move=False,False,False
CanMove=False
ChooseNum=int(0)
DebugText=str('')
DebugNum=int(0)
DebugTextList=[]
CanMoveToList=[]
SocketMessage=[]
PawnRoad=[0,0,0,0,0,0,0,0]
BeGodDict={'q':'?Queen','w':'?Rook','e':'?Knight','r':'?Bishop'}
CanBeGod=[False,False,False,False,False,False,False,False]
CanMoveToPosition=tuple(())
FlaskMoveDict={'up':(-1,0),'down':(1,0),'left':(0,-1),'right':(0,1)}
ChessStrDict = {'Rook':['♜','♖'],
              'Bishop':['♝','♗'],
              'Knight':['♞','♘'],
              'Pawn':['♟','♙'],
              'King':['♚','♔'],
              'Queen':['♛','♕']
              }
White = {'!':0,'?':1}
Black = {'!':1,'?':0}
TargetChess=tuple((7,4))


TURN=True

ChessListBlack=[['!Rook','!Knight','!Bishop','!Queen','!King','!Bishop','!Knight','!Rook'],
           ['!Pawn','!Pawn','!Pawn','!Pawn','!Pawn','!Pawn','!Pawn','!Pawn'],
           ['empty','empty','empty','empty','empty','empty','empty','empty'],
           ['empty','empty','empty','empty','empty','empty','empty','empty'],
           ['empty','empty','empty','empty','empty','empty','empty','empty'],
           ['empty','empty','empty','empty','empty','empty','empty','empty'],
           ['?Pawn','?Pawn','?Pawn','?Pawn','?Pawn','?Pawn','?Pawn','?Pawn'],
           ['?Rook','?Knight','?Bishop','?Queen','?King','?Bishop','?Knight','?Rook']]
ChessListWhite=[['!Rook','!Knight','!Bishop','!King','!Queen','!Bishop','!Knight','!Rook'],
           ['!Pawn','!Pawn','!Pawn','!Pawn','!Pawn','!Pawn','!Pawn','!Pawn'],
           ['empty','empty','empty','empty','empty','empty','empty','empty'],
           ['empty','empty','empty','empty','empty','empty','empty','empty'],
           ['empty','empty','empty','empty','empty','empty','empty','empty'],
           ['empty','empty','empty','empty','empty','empty','empty','empty'],
           ['?Pawn','?Pawn','?Pawn','?Pawn','?Pawn','?Pawn','?Pawn','?Pawn'],
           ['?Rook','?Knight','?Bishop','?King','?Queen','?Bishop','?Knight','?Rook']]
skDict={"ChessListWhite":ChessListWhite,"ChessListBLack":ChessListBlack}

DeathListLocal=[]
DeathListEnemy=[]

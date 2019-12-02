from chessboard import ChessBoard
from Player import ChoiceOfPlayer,HumanPlayer,AIPlayer_1,AIPlayer_2,AIPlayer_3
#from ai import searcher
import time
from const_set import *


import sys
import PyQt5.sip
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox,QInputDialog
from PyQt5.QtCore import Qt,QCoreApplication
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter,QFont
from PyQt5.QtMultimedia import QSound


# ----------------------------------------------------------------------
# 定义线程类执行AI的算法
# ----------------------------------------------------------------------



		
# ----------------------------------------------------------------------
# 重新定义Label类
# ----------------------------------------------------------------------
class LaBel(QLabel):
	def __init__(self, parent):
		super().__init__(parent)
		self.setMouseTracking(True)

	def enterEvent(self, e):
		e.ignore()






class GoBang(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):

		self.chessboard = ChessBoard()# 棋盘类
		self.chess_manual = ""

		palette1 = QPalette()# 设置棋盘背景
		pix  =QtGui.QPixmap('board_' + str(N_LINE) + '.jpg')
		pix = pix.scaled(WIDTH,HEIGHT)
		palette1.setBrush(self.backgroundRole(), QtGui.QBrush(pix))
		self.setPalette(palette1)

		self.setCursor(Qt.PointingHandCursor)# 鼠标变成手指形状
		#self.sound_piece = QSound("sound/luozi.wav")# 加载落子音效
		# self.sound_win = QSound("sound/win.wav")# 加载胜利音效
		# self.sound_defeated = QSound("sound/defeated.wav")# 加载失败音效

		self.resize(WIDTH, HEIGHT)# 固定大小 540*540
		self.setMinimumSize(QtCore.QSize(WIDTH, HEIGHT))
		self.setMaximumSize(QtCore.QSize(WIDTH, HEIGHT))

		self.setWindowTitle("GoBang")# 窗口名称
		self.setWindowIcon(QIcon('black.png'))# 窗口图标

		# self.lb1 = QLabel('			', self)
		# self.lb1.move(20, 10)

		self.black = QPixmap('black.png')
		self.white = QPixmap('white.png')

		self.is_black_do = True# 黑棋回合先行
		self.Going_over = True
		self.step = 0# 步数
		self.x, self.y = 1000, 1000

		self.who = QLabel('Black Player is Going...',self)
		self.who.resize(WIDTH,MARGIN)
		self.who.move(0,0)
		self.who.setAlignment(Qt.AlignHCenter)
		self.who.setFont(QFont("Roman times",MARGIN/3,QFont.Bold))


		# choose the Mode pvp,pve,eve
		text, ok = QInputDialog.getText(self, 'The Black Player', 'Choose the Black Player\n0 for Human\n1 for AI_1\n2 for AI_2\n3 for AI_3\n4 for AI_MCTS')
		black_text = 0
		white_text = 0
		if not ok:
			sys.exit()
		while(1):
			if ok:
				if text == "0":
					black_text = 0
					break
				elif text == "1":
					black_text = 1
					break
				elif text == "2":
					black_text = 2
					break
				elif text == "3":
					black_text = 3
					break
				elif text == "4":
					black_text = 4
					break
				else:
					text, ok = QInputDialog.getText(self, 'The Black Player', 'Illegal Input!\n0 for Human\n1 for AI_1\n2 for AI_2\n3 for AI_3\n4 for AI_MCTS')


		self.setWindowIcon(QIcon('white.png'))
		text, ok = QInputDialog.getText(self, 'The White Player', 'Choose the White Player\n0 for Human\n1 for AI_1\n2 for AI_2\n3 for AI_3\n4 for AI_MCTS')

		if not ok:
			sys.exit()
		while(1):
			if ok:
				if text == "0":
					white_text = 0
					break
				elif text == "1":
					white_text = 1
					break
				elif text == "2":
					white_text = 2
					break
				elif text == "3":
					white_text = 3
					break
				elif text == "4":
					white_text = 4
					break
				else:
					text, ok = QInputDialog.getText(self, 'The White Player', 'Illegal Input!\n0 for Human\n1 for AI_1\n2 for AI_2\n3 for AI_3\n4 for AI_MCTS')

		self.player_black = ChoiceOfPlayer(self.chessboard,black_text,True,self)
		self.player_white = ChoiceOfPlayer(self.chessboard,white_text,False,self)
		self.black_text = black_text
		self.white_text = white_text
		# text, ok = QInputDialog.getText(self, 'Mode Select', '1 for PvsP\n2 for PvsAI\n3 for AIvAI\n4 for Random vs AI\n5 for Random vs Random')
		# Mode = 0
		# while(1):
		# 	if ok:
		# 		if text == "1":
		# 			Mode = 1
		# 			break
		# 		elif text == "2":
		# 			Mode = 2
		# 			break
		# 		elif text == "3":
		# 			Mode = 3
		# 			break
		# 		elif text == "4":
		# 			Mode = 4
		# 			break
		# 		elif text == "5":
		# 			Mode = 5
		# 			break
		# 		else:
		# 			text, ok = QInputDialog.getText(self, 'Mode Select', 'Illegal input\n1 for pvp\n2 for pve\n3 for eve')

		# if Mode == 1:
		# 	self.player_black = ChoiceOfPlayer(self.chessboard,0,True,self)
			
		# 	self.player_white = ChoiceOfPlayer(self.chessboard,0,False,self)

		# elif Mode == 3:
		# 	self.player_black = ChoiceOfPlayer(self.chessboard,1,True,self)
		# 	self.player_white = ChoiceOfPlayer(self.chessboard,1,False,self)
		# elif Mode == 5:
		# 	self.player_black = ChoiceOfPlayer(self.chessboard,2,True,self)
		# 	self.player_white = ChoiceOfPlayer(self.chessboard,2,False,self)
		# elif Mode == 2:
		# 	human_color, ok = QInputDialog.getText(self, 'Color Select', '1 for black\n2 for white')
		# 	while(1):
		# 		if ok:
		# 			if human_color == "1":
		# 				self.player_black = ChoiceOfPlayer(self.chessboard,0,True,self)
		# 				self.player_white = ChoiceOfPlayer(self.chessboard,1,False,self)
		# 				break;
		# 			elif human_color == "2":
		# 				self.player_white = ChoiceOfPlayer(self.chessboard,0,False,self)
		# 				self.player_black = ChoiceOfPlayer(self.chessboard,1,True,self)
		# 				break;
		# 			else:
		# 				human_color, ok = QInputDialog.getText(self, 'Color Select', 'Illegal input\n1 for black\n2 for white')
		# else Mode == 4:

		self.setWindowIcon(QIcon('black.png'))
		self.mouse_point = LaBel(self)# 将鼠标图片改为棋子
		self.mouse_point.setScaledContents(True)
		self.mouse_point.setPixmap(self.black)#加载黑棋
		self.mouse_point.setGeometry(270, 270, PIECE, PIECE)
		self.pieces = [LaBel(self) for i in range(225)]# 新建棋子标签，准备在棋盘上绘制棋子
		for piece in self.pieces:
			piece.setVisible(True)# 图片可视
			piece.setScaledContents(True)#图片大小根据标签大小可变

		self.mouse_point.raise_()# 鼠标始终在最上层
		#self.ai_down = True# AI已下棋，主要是为了加锁，当值是False的时候说明AI正在思考，这时候玩家鼠标点击失效，要忽略掉 mousePressEvent

		self.setMouseTracking(True)
		print('Choose Over')
		self.show()
		self.game()
				

	def game(self):
		

		if(1):
			self.player_black.is_black = True
			self.player_white.is_black = True
			#if self.is_black_do == True and self.Going_over == True:
			if(1):
				print('black')
				self.Going_over = False
				self.player_black.board = self.chessboard
				#self.player_black.is_black = True
				self.player_black.finishSignal.connect(self.AI_draw)
				if self.step < 2:
					self.player_black.start()
				
			#if self.is_black_do == False and self.Going_over == True:
			if(1):
				print('white')
				self.Going_over = False
				self.player_white.board = self.chessboard
				#self.player_white.is_black = False
				self.player_white.finishSignal.connect(self.AI_draw)
				if self.step<2:
					self.player_white.start()
				


	def AI_draw(self, i, j):
		if self.step != -1:
			self.draw(i, j)# AI
			self.x_t, self.y_t = self.coordinate_transform_map2pixel(i, j)
			

		self.update()
		



	def draw(self, i, j):
		x, y = self.coordinate_transform_map2pixel(i, j)

		if self.is_black_do == True:
			self.pieces[self.step].setPixmap(self.black)# 放置黑色棋子
			self.is_black_do = False
			self.chessboard.draw_xy(i, j, BLACK)
			self.who.setText('WHITE Player is Going...')
		else:
			self.pieces[self.step].setPixmap(self.white)# 放置白色棋子
			self.is_black_do = True
			self.chessboard.draw_xy(i, j, WHITE)
			self.who.setText('BLACK Player is Going...')

		print(self.step)
		#b,w = self.chessboard.value_judge()
		#b,w = self.chessboard.value_judge_2(i,j)
		#print('B_value:' + str(b) + '\n' + 'W_value:' + str(w) + '\n')
		self.pieces[self.step].setGeometry(x, y, PIECE, PIECE)# 画出棋子
		#self.sound_piece.play()# 落子音效
		self.step += 1# 步数+1
		self.chess_manual = self.chess_manual + str(i) +',' + str(j) + '|'

		winner = self.chessboard.anyone_win(i, j)# 判断输赢
		self.Going_over = True
		if winner != EMPTY:
			self.mouse_point.clear()
			tmp,black,white = self.chessboard.get_board_item()
			print("BLACK num: " + str(len(black)))
			print("WHITE num: " + str(len(white)))


			self.player_black.is_black = False
			self.player_white.is_black = True
			self.gameover(winner)


	def coordinate_transform_map2pixel(self, i, j):
		# 从 chessMap 里的逻辑坐标到 UI 上的绘制坐标的转换
		return MARGIN + j * GRID - PIECE / 2, MARGIN + i * GRID - PIECE / 2

	def coordinate_transform_pixel2map(self, x, y):
		# 从 UI 上的绘制坐标到 chessMap 里的逻辑坐标的转换
		i, j = int(round((y - MARGIN) / GRID)), int(round((x - MARGIN) / GRID))
		# 有MAGIN, 排除边缘位置导致 i,j 越界
		if i < 0 or i >= N_LINE or j < 0 or j >= N_LINE:
			return None, None
		else:
			return i, j

	def gameover(self, winner):

		fo = open('Manual/'+str(self.black_text) + 'vs' + str(self.white_text) + '_' + str(time.time()) + '.chess','w')
		fo.write('BOARD_SIZE:' + str(N_LINE))
		fo.write('BLACK Player: ' + str(self.black_text) + '\n')
		fo.write('WHITE Player: ' + str(self.white_text) + '\n')
		fo.write('Winner: ' + str(winner) + '\n')
		fo.write(str(self.chess_manual))
		fo.close()

		if winner == BLACK:
			# self.sound_win.play()
			reply = QMessageBox.question(self, 'BLACK Win!', 'BLACK Win! Continue?',
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		elif winner == WHITE:
			# self.sound_defeated.play()
			reply = QMessageBox.question(self, 'WHITE Win!', 'WHITE Win! Continue?',
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		else:
			reply = QMessageBox.question(self, 'Tie', 'Tie! Continue?',
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)			
		if reply == QMessageBox.Yes:# 复位
			self.is_black_do = True
			self.mouse_point.setPixmap(self.black)
			self.step = 0
			for piece in self.pieces:
				piece.clear()
			self.chessboard.reset()
			self.player_black.is_black = True
			self.player_white.is_black = True
			self.chess_manual = ""
			self.who.setText('BLACK Player is Going...')
			self.update()
		else:
			self.close()



	def paintEvent(self, event): # 画出指示箭头
		qp = QPainter()
		qp.begin(self)
		self.drawLines(qp)
		qp.end()

	def mouseMoveEvent(self, e): # 黑色棋子随鼠标移动
		# self.lb1.setText(str(e.x()) + ' ' + str(e.y()))
		self.mouse_point.move(e.x() - PIECE * 0.5, e.y() - PIECE * 0.5)

	# def mousePressEvent(self, e):# 玩家下棋
	#	 if e.button() == Qt.LeftButton and self.ai_down == True:
	#		 x, y = e.x(), e.y()# 鼠标坐标
	#		 i, j = self.coordinate_transform_pixel2map(x, y)# 对应棋盘坐标
	#		 if not i is None and not j is None:# 棋子落在棋盘上，排除边缘
	#			 if self.chessboard.get_xy_on_logic_state(i, j) == EMPTY:# 棋子落在空白处
	#				 self.draw(i, j)
	#				 #self.ai_down = False
	#				 board = self.chessboard.board()
	#				 # self.AI = AI(board)# 新建线程对象，传入棋盘参数
	#				 # self.AI.finishSignal.connect(self.AI_draw)# 结束线程，传出参数
	#				 # self.AI.start()# run

	def mousePressEvent(self,e):
		self.x = e.x()
		self.y = e.y()
		self.Going = False




	def drawLines(self, qp):# 指示AI当前下的棋子
		if self.step != 0:
			pen = QtGui.QPen(QtCore.Qt.red, 10, QtCore.Qt.SolidLine)
			qp.setPen(pen)


			qp.drawLine(self.x_t - 60, self.y_t - 60, self.x_t + 3, self.y_t + 3)
			qp.drawLine(self.x_t + 13, self.y_t, self.x_t + 13, self.y_t + 13)
			qp.drawLine(self.x_t, self.y_t + 13, self.x_t + 13, self.y_t + 13)




if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = GoBang()
	sys.exit(app.exec_())

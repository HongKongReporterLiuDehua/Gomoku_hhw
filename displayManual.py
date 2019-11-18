from chessboard import ChessBoard
#from ai import searcher
import time
from const_set import *


import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox,QFileDialog
from PyQt5.QtCore import Qt,QCoreApplication
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter
from PyQt5.QtMultimedia import QSound


# ----------------------------------------------------------------------
# 定义线程类执行AI的算法
# ----------------------------------------------------------------------
class DisplayPlayer(QtCore.QThread):
	finishSignal = QtCore.pyqtSignal(int, int)

    # 构造函数里增加形参
	def __init__(self,step_list,parent=None):
		super(DisplayPlayer,self).__init__()
		self.step_list = step_list
		self.idx = 0
		self.parent = parent

	def run(self):
		while(self.idx < len(self.step_list)):
			if self.parent.Going == False:
				time.sleep(0.5)
				continue
			self.finishSignal.emit(self.step_list[self.idx][0], self.step_list[self.idx][1])
			self.idx += 1
			self.parent.Going = False

                



		
# ----------------------------------------------------------------------
# 重新定义Label类
# ----------------------------------------------------------------------
class LaBel(QLabel):
	def __init__(self, parent):
		super().__init__(parent)
		self.setMouseTracking(True)

	def enterEvent(self, e):
		e.ignore()






class display_manual(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):

		self.chessboard = ChessBoard()# 棋盘类
		self.chess_manual = []
		self.Going = False
		palette1 = QPalette()# 设置棋盘背景
		pix = QtGui.QPixmap('board_' + str(N_LINE) + '.jpg')
		pix = pix.scaled(WIDTH,HEIGHT)
		palette1.setBrush(self.backgroundRole(), QtGui.QBrush(pix))
		self.setPalette(palette1)
		# self.setStyleSheet("board-image:url(img/chessboard.jpg)")# 不知道这为什么不行
		self.setCursor(Qt.PointingHandCursor)# 鼠标变成手指形状
		#self.sound_piece = QSound("sound/luozi.wav")# 加载落子音效
		# self.sound_win = QSound("sound/win.wav")# 加载胜利音效
		# self.sound_defeated = QSound("sound/defeated.wav")# 加载失败音效

		self.resize(WIDTH, HEIGHT)# 固定大小 540*540
		self.setMinimumSize(QtCore.QSize(WIDTH, HEIGHT))
		self.setMaximumSize(QtCore.QSize(WIDTH, HEIGHT))

		self.setWindowTitle("GoBang")# 窗口名称
		# self.setWindowIcon(QIcon('img/black.png'))# 窗口图标

		# self.lb1 = QLabel('			', self)
		# self.lb1.move(20, 10)

		self.black = QPixmap('black.png')
		self.white = QPixmap('white.png')

		self.is_black_do = True# 黑棋回合先行

		self.step = 0# 步数
		self.x, self.y = 1000, 1000


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
		self.show()
		self.display_it()
				

	def display_it(self):
		openfile_name,file_type = QFileDialog.getOpenFileName(self,'选择文件','','chess_manual(*.chess)')
		
		print(openfile_name)
		fo = open(openfile_name,'r')
		fo.readline()
		fo.readline()
		fo.readline()
		string = fo.readline()
		step_list = []
		flag_1 = False
		flag_2 = False
		x = 0
		y = 0
		flag_1 = True
		sub_str = string.split("|")
		for sub_sub in sub_str:
			if sub_sub == "":
				break
			num_pair = sub_sub.split(',')
			x = int(num_pair[0])
			y = int(num_pair[1])
			step_list.append([x,y])

		print(step_list)
		fo.close()
		# for l in step_list:
		# 	self.AI_draw(l[0],l[1])
		
		self.display_player = DisplayPlayer(step_list,self)
		self.display_player.finishSignal.connect(self.AI_draw)
		self.display_player.start()









				


	def AI_draw(self, i, j):
		if self.step != -1:
			self.draw(i, j)# AI
			self.x_t, self.y_t = self.coordinate_transform_map2pixel(i, j)
			

		self.update()
		print('update')
		



	def draw(self, i, j):
		x, y = self.coordinate_transform_map2pixel(i, j)

		if self.is_black_do == True:
			self.pieces[self.step].setPixmap(self.black)# 放置黑色棋子
			self.is_black_do = False
			self.chessboard.draw_xy(i, j, BLACK)
		else:
			self.pieces[self.step].setPixmap(self.white)# 放置白色棋子
			self.is_black_do = True
			self.chessboard.draw_xy(i, j, WHITE)

		print(self.step)
		self.pieces[self.step].setGeometry(x, y, PIECE, PIECE)# 画出棋子
		#self.sound_piece.play()# 落子音效
		self.step += 1# 步数+1
		self.chess_manual.append([i,j])

		winner = self.chessboard.anyone_win(i, j)# 判断输赢
		self.Going_over = True
		if winner != EMPTY:
			self.mouse_point.clear()
			tmp,black,white = self.chessboard.get_board_item()
			print("BLACK num: " + str(len(black)))
			print("WHITE num: " + str(len(white)))


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



		if winner == BLACK:
			# self.sound_win.play()
			reply = QMessageBox.question(self, 'BLACK Win!', 'BLACK Win! Continue?',
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		else:
			# self.sound_defeated.play()
			reply = QMessageBox.question(self, 'WHITE Win!', 'WHITE Win! Continue?',
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

		if reply == QMessageBox.Yes:# 复位
			self.is_black_do = True
			self.mouse_point.setPixmap(self.black)
			self.step = 0
			for piece in self.pieces:
				piece.clear()
			self.chessboard.reset()
			self.update()
			self.display_it()
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
		self.Going = True




	def drawLines(self, qp):# 指示AI当前下的棋子
		if self.step != 0:
			pen = QtGui.QPen(QtCore.Qt.green, 10, QtCore.Qt.SolidLine)
			qp.setPen(pen)

			qp.drawLine(self.x_t - 60, self.y_t - 60, self.x_t + 3, self.y_t + 3)
			qp.drawLine(self.x_t + 13, self.y_t, self.x_t + 13, self.y_t + 13)
			qp.drawLine(self.x_t, self.y_t + 13, self.x_t + 13, self.y_t + 13)




if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = display_manual()
	sys.exit(app.exec_())

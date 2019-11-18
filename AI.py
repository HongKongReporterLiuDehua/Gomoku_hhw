# init(is_black)
# out: (i,j) the position of the chessboard
from const_set import *


import copy
import time
import random
from chessboard import ChessBoard




def evaluate(board,color):
	b_value,w_value = board.value_judge(color)
	if color == BLACK:

		return b_value - w_value
	else:
		return w_value - b_value


def evaluate_2(board,color,x,y): # for this step
	b_value,w_value = board.value_judge_2(x,y,color)
	if color == BLACK:

		return b_value - w_value
	else:
		return w_value - b_value


class MinMax():
	def __init__(self,is_black,depth = DEPTH):
		self.depth = depth
		if is_black == True:
			self.color = BLACK
			self.other = WHITE
		else:
			self.color = WHITE
			self.other = BLACK



	def get_move(self,board):
		self.over = False
		depth = self.depth
		self.count = 0
		start = time.time()
		value,idx = self.Max(board,None,depth,999999999)
		print("Time of this step: " + str(time.time() - start))
		print('AI_MINMAX had come a over:' + str(self.over))
		#print("The value is : " + str(value))
		return idx

	def Max(self,board,move,depth,cut_value):
		# self.count += 1
		# if self.count % 100 == 0:
		# 	print(self.count)
		my_board = copy.deepcopy(board)

		if move is not None:
			my_board.draw_xy(move[0],move[1],self.other)
			if my_board.anyone_win(move[0],move[1]) == self.color:
				self.over = True
				return 9999999 * (depth + 1),(move[0],move[1])
			if my_board.anyone_win(move[0],move[1]) == self.other:
				self.over = True
				return -9999999 * (depth + 1),(move[0],move[1])

		max_value = -999999999
		empty_item = my_board.get_k_dist_empty(3)
		if len(empty_item) == 0:
			empty_item.append([MIDDLE,MIDDLE])
		t = random.randint(0,len(empty_item)-1)
		max_idx = empty_item[t]
		depth -= 1
		#print('good location:  \n'+str(empty_item))
		#print('MAX_depth:'+str(depth))
		if depth < 0:
			return evaluate(my_board,self.color),(move[0],move[1])

		
		for mov in empty_item:
			
			value,idx = self.Min(my_board,mov,depth,max_value)
			if value > cut_value:
				return cut_value,(move[0],move[1])
			if max_value < value:
				max_value = value
				max_idx = (mov[0],mov[1])

		return max_value,max_idx





	def Min(self,board,move,depth,cut_value):
		# self.count += 1
		# if self.count % 100 == 0:
		# 	print(self.count)
		my_board = copy.deepcopy(board)
		if move is not None:
			my_board.draw_xy(move[0],move[1],self.color)
			if my_board.anyone_win(move[0],move[1]) == self.color:
				self.over = True
				return 9999999 * (depth + 1),(move[0],move[1])
			if my_board.anyone_win(move[0],move[1]) == self.other:
				self.over = True
				return -9999999 * (depth + 1),(move[0],move[1])

		min_value = 999999999
		empty_item = my_board.get_k_dist_empty(3)
		if len(empty_item) == 0:
			empty_item.append([MIDDLE,MIDDLE])
		t = random.randint(0,len(empty_item)-1)
		min_idx = empty_item[t]
		depth -= 1
		#print('MIN_depth:' + str(depth))
		if depth < 0:
			return evaluate(my_board,self.color),(move[0],move[1])


		for mov in empty_item:
			value,idx = self.Max(my_board,mov,depth,min_value)
			if value < cut_value:
				return cut_value,(move[0],move[1])

			if min_value > value:
				min_value = value
				min_idx = (mov[0],mov[1])

		return min_value,min_idx


# class MinMax_2():
# 	def __init__(self,is_black):
# 		if is_black == True:
# 			self.color = BLACK
# 			self.other = WHITE
# 		else:
# 			self.color = WHITE
# 			self.other = BLACK



# 	def get_move(self,board):
# 		self.over = False
# 		depth = DEPTH
# 		self.count = 0
# 		start = time.time()
# 		value,idx = self.Max(board,None,depth,9999999)
# 		print("Time of this step: " + str(time.time() - start))
# 		print("The value is : " + str(value))
# 		return idx

# 	def Max(self,board,move,depth,cut_value):
# 		# self.count += 1
# 		# if self.count % 1000 == 0:
# 		# 	print(self.count)
# 		my_board = copy.deepcopy(board)
# 		base_value = 0
# 		if move is not None:
# 			my_board.draw_xy(move[0],move[1],self.other)
# 			base_value = evaluate_2(my_board,self.color,move[0],move[1])
			
# 			if my_board.anyone_win(move[0],move[1]) == self.color:
# 				return 9999999,(move[0],move[1])
# 			if my_board.anyone_win(move[0],move[1]) == self.other:
# 				return -9999999,(move[0],move[1])
# 		empty_item,a,b = my_board.get_board_item()
# 		max_value = -9999999
# 		t = random.randint(0,len(empty_item)-1)
# 		max_idx = empty_item[t]
# 		depth -= 1
# 		#print('MAX_depth:'+str(depth))
# 		if depth < 0:
# 			return evaluate_2(my_board,self.color,move[0],move[1]),(move[0],move[1])

# 		if base_value > cut_value:
# 			return cut_value,(move[0],move[1])
# 		for mov in empty_item:
			
# 			v,idx = self.Min(my_board,mov,depth,max_value)
# 			value = base_value + v
# 			if value > cut_value:
# 				return cut_value,(move[0],move[1])
# 			if max_value < value:
# 				max_value = value
# 				max_idx = (mov[0],mov[1])
# 		return max_value,max_idx





	# def Min(self,board,move,depth,cut_value):
	# 	# self.count += 1
	# 	# if self.count % 100 == 0:
	# 	# 	print(self.count)
	# 	my_board = copy.deepcopy(board)
	# 	base_value = 0
	# 	if move is not None:
	# 		my_board.draw_xy(move[0],move[1],self.color)
	# 		base_value = evaluate_2(my_board,self.color,move[0],move[1])
			
	# 		if my_board.anyone_win(move[0],move[1]) == self.color:
	# 			return 9999999,(move[0],move[1])
	# 		if my_board.anyone_win(move[0],move[1]) == self.other:
	# 			return -9999999,(move[0],move[1])
	# 	empty_item,a,b = my_board.get_board_item()
	# 	min_value = 9999999
	# 	t = random.randint(0,len(empty_item)-1)
	# 	min_idx = empty_item[t]
	# 	depth -= 1
	# 	#print('MIN_depth:' + str(depth))
	# 	if depth < 0:
	# 		return evaluate_2(my_board,self.color,move[0],move[1]),(move[0],move[1])

	# 	if base_value < cut_value:
	# 		return cut_value,(move[0],move[1])
	# 	for mov in empty_item:
	# 		v,idx = self.Max(my_board,mov,depth,min_value)
	# 		value = base_value + v
	# 		if value < cut_value:
	# 			return cut_value,(move[0],move[1])

	# 		if min_value > value:
	# 			min_value = value
	# 			min_idx = (mov[0],mov[1])

	# 	return min_value,min_idx








class MinMax_smallset():
	def __init__(self,is_black,depth = DEPTH):
		self.depth = depth
		if is_black == True:
			self.color = BLACK
			self.other = WHITE
		else:
			self.color = WHITE
			self.other = BLACK



	def get_move(self,board):
		self.over = False
		depth = self.depth
		self.count = 0
		self.win_depth = 0
		start = time.time()
		value,idx = self.Max(board,None,depth,999999999)
		print("AI step: " + str(idx))
		print("Time of this step: " + str(time.time() - start))
		print('AI_MINMAX_SMALL had come a over:' + str(self.over))
		#print("The value is : " + str(value))
		return idx

	def Max(self,board,move,depth,cut_value):
		# self.count += 1
		# if self.count % 100 == 0:
		# 	print(self.count)
		my_board = copy.deepcopy(board)
		base_value = 0
		if move is not None:
			my_board.draw_xy(move[0],move[1],self.other)
			base_value = evaluate_2(my_board,self.color,move[0],move[1])
			
			if my_board.anyone_win(move[0],move[1]) == self.color:
				self.over = True
				return 9999999 * (depth + 1),(move[0],move[1])
			if my_board.anyone_win(move[0],move[1]) == self.other:
				self.over = True
				return -9999999 * (depth + 1),(move[0],move[1])
		empty_item = my_board.get_k_dist_empty(3)
		if len(empty_item) == 0:
			empty_item.append([MIDDLE,MIDDLE])
		max_value = -999999999

		t = random.randint(0,len(empty_item)-1)
		max_idx = empty_item[t]
		depth -= 1
		#print('MAX_depth:'+str(depth))
		if depth < 0:
			return evaluate_2(my_board,self.color,move[0],move[1]),(move[0],move[1])

		# if base_value > cut_value:
		# 	return cut_value,(move[0],move[1])
		for mov in empty_item:
			
			v,idx = self.Min(my_board,mov,depth,max_value)
			value = base_value + v
			if value > cut_value:
				return cut_value,(move[0],move[1])

			# if value > cut_value:
			# 	return cut_value,(move[0],move[1])
			if max_value < value:
				max_value = value
				max_idx = (mov[0],mov[1])

		return max_value,max_idx





	def Min(self,board,move,depth,cut_value):
		# self.count += 1
		# if self.count % 100 == 0:
		# 	print(self.count)
		my_board = copy.deepcopy(board)
		base_value = 0
		if move is not None:
			my_board.draw_xy(move[0],move[1],self.color)
			base_value = evaluate_2(my_board,self.color,move[0],move[1])
			
			if my_board.anyone_win(move[0],move[1]) == self.color:
				self.over = True
				return 9999999 * (depth + 1),(move[0],move[1])
			if my_board.anyone_win(move[0],move[1]) == self.other:
				self.over = True
				return -9999999 * (depth + 1),(move[0],move[1])
		empty_item = my_board.get_k_dist_empty(3)
		min_value = 999999999
		t = random.randint(0,len(empty_item)-1)
		min_idx = empty_item[t]
		depth -= 1
		#print('MIN_depth:' + str(depth))
		if depth < 0:
			return evaluate_2(my_board,self.color,move[0],move[1]),(move[0],move[1])

		# if base_value < cut_value:
		# 	return cut_value,(move[0],move[1])
		for mov in empty_item:
			v,idx = self.Max(my_board,mov,depth,min_value)
			value = base_value + v
			if value < cut_value:
				return cut_value,(move[0],move[1])

			if min_value > value:
				min_value = value
				min_idx = (mov[0],mov[1])

		return min_value,min_idx





class MinMax_best():
	def __init__(self,is_black,depth = 2):
		self.depth = depth
		if is_black == True:
			self.color = BLACK
			self.other = WHITE
		else:
			self.color = WHITE
			self.other = BLACK



	def get_move(self,board):
		self.over = False
		depth = self.depth
		self.count = 0
		start = time.time()
		value,idx = self.Max(board,None,depth,999999999)
		print("Time of this step: " + str(time.time() - start))
		print('AI_MINMAX had come a over:' + str(self.over))
		#print("The value is : " + str(value))
		return idx

	def Max(self,board,move,depth,cut_value):
		# self.count += 1
		# if self.count % 100 == 0:
		# 	print(self.count)
		my_board = copy.deepcopy(board)

		if move is not None:
			my_board.draw_xy(move[0],move[1],self.other)
			if my_board.anyone_win(move[0],move[1]) == self.color:
				self.over = True
				return 9999999 * (depth + 1),(move[0],move[1])
			if my_board.anyone_win(move[0],move[1]) == self.other:
				self.over = True
				return -9999999 * (depth + 1),(move[0],move[1])

		max_value = -999999999
		empty_item = my_board.get_k_dist_empty(3)
		if len(empty_item) == 0:
			empty_item.append([MIDDLE,MIDDLE])
		t = random.randint(0,len(empty_item)-1)
		max_idx = empty_item[t]
		depth -= 1
		#print('good location:  \n'+str(empty_item))
		#print('MAX_depth:'+str(depth))
		if depth < 0:
			return -evaluate(my_board,self.other),(move[0],move[1])

		
		for mov in empty_item:
			
			value,idx = self.Min(my_board,mov,depth,max_value)
			if value > cut_value:
				return cut_value,(move[0],move[1])
			if max_value < value:
				max_value = value
				max_idx = (mov[0],mov[1])

		return max_value,max_idx





	def Min(self,board,move,depth,cut_value):
		# self.count += 1
		# if self.count % 100 == 0:
		# 	print(self.count)
		my_board = copy.deepcopy(board)
		if move is not None:
			my_board.draw_xy(move[0],move[1],self.color)
			if my_board.anyone_win(move[0],move[1]) == self.color:
				self.over = True
				return 9999999 * (depth + 1),(move[0],move[1])
			if my_board.anyone_win(move[0],move[1]) == self.other:
				self.over = True
				return -9999999 * (depth + 1),(move[0],move[1])

		min_value = 999999999
		empty_item = my_board.get_k_dist_empty(3)
		if len(empty_item) == 0:
			empty_item.append([MIDDLE,MIDDLE])
		t = random.randint(0,len(empty_item)-1)
		min_idx = empty_item[t]
		depth -= 1
		#print('MIN_depth:' + str(depth))
		if depth < 0:
			return evaluate(my_board,self.color),(move[0],move[1])


		for mov in empty_item:
			value,idx = self.Max(my_board,mov,depth,min_value)
			if value < cut_value:
				return cut_value,(move[0],move[1])

			if min_value > value:
				min_value = value
				min_idx = (mov[0],mov[1])

		return min_value,min_idx




from const_set import *
import time
import copy
import random
from treelib import Tree,Node
from math import log,sqrt



class MCTS():
	def __init__(self,confidence = CONFIDENCE,time = MAX_CAL_TIME,max_actions = 1000):

		self.max_cal_time = float(time)
		self.max_actions = max_actions

		self.confidence = confidence


		self.max_depth = 0

	def get_move(self,board,player):
		self.board = board

		self.player = player # The chess color [BLACK or WHITE] represent the player
		empty_set,a,b = self.board.get_board_item()
		if len(empty_set) == 1:
			return (empty_set[0][0],empty_set[0][1])
		if len(empty_set) == 0:
			print("No place to play")
			return None

		self.plays = {}
		self.wins = {}
		simulations = 0
		start = time.time()
		while time.time() - start < (self.max_cal_time-0.5):
			board_for_MCTS = copy.deepcopy(self.board)
			player_for_MCTS = self.player
			
			self.run_simulation(board_for_MCTS,player_for_MCTS)
			simulations += 1

		print("total simuations = ",simulations)

		move = self.select_best_move()

		print("MCTS move:",move[0],move[1])

		return move

	def run_simulation(self,board,player):
		
		plays = self.plays
		wins = self.wins
		availables = board.get_k_dist_empty_tuple(2)

		visited_states = set()
		winner = -1
		expand = True

		# Simulation Start
		for t in range(1,self.max_actions + 1):
			availables = board.get_k_dist_empty_tuple(2)

			# Selection

			if all(plays.get((player,move)) for move in availables):

				log_total = log(sum(plays[(player,move)] for move in availables))
				value,move = max(
					((wins[(player,move)] / plays[(player,move)]) + 
					sqrt(self.confidence * log_total / plays[(player,move)]),move)
					for move in availables)

			else:
				move = random.choice(availables)

			board.draw_xy(move[0],move[1],player)

			#Expand
			if expand and (player,move) not in plays:
				expand = False
				plays[(player,move)] = 0
				wins[(player,move)] = 0
				if t > self.max_depth:
					self.max_depth = t

			visited_states.add((player,move))
			availables = board.get_k_dist_empty_tuple(2)
			is_full = not len(availables)
			winner = board.anyone_win(move[0],move[1])
			
			if winner is not EMPTY or is_full:
				#print(str(move) + '----' + str(winner) + '-----' + str(player))
				break

			player = self.player_change(player)

		for player, move in visited_states:
			if (player,move) not in plays:
				continue
			plays[(player,move)] += 1

			if player == winner:
				wins[(player,move)] += 1






	def select_best_move(self):
		empty_set = self.board.get_k_dist_empty_tuple(2)
		# for move in empty_set:
		# 	ratio = (self.wins.get((self.player,move),0)/
		# 		self.plays.get((self.player,move),1))
		# 	print(move)
		# 	print(ratio)

		#print(empty_set)
		raio_to_win,move = max(
			(self.wins.get((self.player,move),0)/
				self.plays.get((self.player,move),1) + self.closest_value(move),
				move)
			for move in empty_set)
		print(raio_to_win)
		return move


	def closest_value(self,move):
		x = move[0]
		y = move[1]
		return (abs((x-N_LINE + 1) * x) + abs((y-N_LINE + 1) * y)) * 0.0001


	def player_change(self,player):
		if player == BLACK:
			player = WHITE
		elif player == WHITE:
			player = BLACK

		return player





class MCTS_better():
	def __init__(self,confidence = CONFIDENCE,time = MAX_CAL_TIME,max_actions = 1000):

		self.max_cal_time = float(time)
		self.max_actions = max_actions

		self.confidence = confidence


		self.max_depth = 0

	def get_move(self,board,player):
		self.board = board

		self.player = player # The chess color [BLACK or WHITE] represent the player
		empty_set,a,b = self.board.get_board_item()
		if len(a) == 0 and len(b) == 0:
			return (MIDDLE,MIDDLE)
		if len(empty_set) == 1:
			return (empty_set[0][0],empty_set[0][1])
		if len(empty_set) == 0:
			print("No place to play")
			return None
		self.MCTS_tree = Tree()
		self.HeadNode = Node('HeadNode',0)
		self.MCTS_tree.add_node(self.HeadNode)


		self.plays = {}
		self.wins = {}
		simulations = 0
		start = time.time()
		while time.time() - start < (self.max_cal_time-0.5):
			board_for_MCTS = copy.deepcopy(self.board)
			player_for_MCTS = self.player
			
			self.run_simulation(board_for_MCTS,player_for_MCTS)
			simulations += 1

		print("total simuations = ",simulations)
		move = self.select_best_move()

		print("MCTS move:",move[0],move[1])

		return move

	def run_simulation(self,board,player):
		

		tree = self.MCTS_tree
		node = self.HeadNode
		availables = board.get_k_dist_empty_tuple(2)

		visited_states = set()
		winner = -1
		expand = True

		# Simulation Start
		for t in range(1,self.max_actions + 1):
			availables = board.get_k_dist_empty_tuple(2)
			children = tree.children(node.identifier)
			self.plays = {}
			self.wins = {}
			plays = self.plays
			wins = self.wins
			for n in children:
				plays[n.tag] = n.data[0]
				wins[n.tag] = n.data[1]
			# Selection
			

			noused_set = self.select_noused_node(availables,player)
			


			if len(noused_set) == 0:
				#print("ok")
				
				#print(sum(plays[(player,move)] for move in availables))
				log_total = log(sum(plays[(player,move)] for move in availables))
				value,move = max(
					((wins[(player,move)] / plays[(player,move)]) + 
					sqrt(self.confidence * log_total / plays[(player,move)]),move)
					for move in availables)
				#print(move)

				for n in children:
					if n.tag == (player,move):
						node = n

			else:
				#print('good')
				random.shuffle(noused_set)
				move = noused_set.pop()
				new_node = Node(tag = (player,move),data = [0,0])
				tree.add_node(new_node,parent = node)
				node = new_node

			
			board.draw_xy(move[0],move[1],player)

			#Expand
			# if expand and (player,move,t) not in plays:
			# 	expand = False
			# 	plays[(player,move,t)] = 0
			# 	wins[(player,move,t)] = 0
			# 	if t > self.max_depth:
			# 		self.max_depth = t



			#visited_states.add((player,move))
			availables = board.get_k_dist_empty_tuple(2)
			is_full = not len(availables)
			winner = board.anyone_win(move[0],move[1])
			
			if winner is not EMPTY or is_full:
				#print(str(move) + '----' + str(winner) + '-----' + str(player))
				break

			player = self.player_change(player)

		while(node.is_root() == False):
			if winner == self.player:
				node.data[1] += 1
			node.data[0] += 1
			node = tree.parent(node.identifier)







	def select_best_move(self):
		empty_set = self.board.get_k_dist_empty_tuple(2)
		# for move in empty_set:
		# 	ratio = (self.wins.get((self.player,move),0)/
		# 		self.plays.get((self.player,move),1))
		# 	print(move)
		# 	print(ratio)

		#print(empty_set)
		self.plays = {}
		self.wins = {}
		plays = self.plays
		wins = self.wins
		children = self.MCTS_tree.children(0)

		for n in children:
			plays[n.tag] = n.data[0]
			wins[n.tag] = n.data[1]
		# print(plays)
		# print(wins)
		raio_to_win,move = max(
			(self.wins.get((self.player,move),0)/
				self.plays.get((self.player,move),1) + self.closest_value(move),
				move)
			for move in empty_set)
		print(raio_to_win)
		return move


	def closest_value(self,move):
		x = move[0]
		y = move[1]
		return (abs((x-N_LINE + 1) * x) + abs((y-N_LINE + 1) * y)) * 0.0001


	def player_change(self,player):
		if player == BLACK:
			player = WHITE
		elif player == WHITE:
			player = BLACK

		return player

	def select_noused_node(self,availables,player):
		noused_set = []

		for move in availables:
			if not self.plays.get((player,move)):
				noused_set.append(move)

		return noused_set






##MCTS_MC_RAVE


# class MCTS_MC_RAVE():
# 	def __init__(self,confidence = CONFIDENCE,time = MAX_CAL_TIME,max_actions = 1000):

# 		self.max_cal_time = float(time)
# 		self.max_actions = max_actions

# 		self.confidence = confidence


# 		self.max_depth = 0

# 	def get_move(self,board,player):
# 		self.board = board

# 		self.player = player # The chess color [BLACK or WHITE] represent the player
# 		empty_set,a,b = self.board.get_board_item()
# 		if len(a) == 0 and len(b) == 0:
# 			return (MIDDLE,MIDDLE)
# 		if len(empty_set) == 1:
# 			return (empty_set[0][0],empty_set[0][1])
# 		if len(empty_set) == 0:
# 			print("No place to play")
# 			return None

# 		self.plays = {}
# 		self.moves = {}
# 		self.moves_wins = {}
# 		self.wins = {}
# 		simulations = 0
# 		start = time.time()
# 		while time.time() - start < (self.max_cal_time-0.5):
# 			board_for_MCTS = copy.deepcopy(self.board)
# 			player_for_MCTS = self.player
			
# 			self.run_simulation(board_for_MCTS,player_for_MCTS)
# 			simulations += 1

# 		print("total simuations = ",simulations)

# 		move = self.select_best_move()

# 		print("MCTS move:",move[0],move[1])

# 		return move

# 	def run_simulation(self,board,player):
		
# 		plays = self.plays
# 		wins = self.wins
# 		moves = self.moves
# 		moves = self.moves_wins
# 		availables = board.get_k_dist_empty_tuple(2)

# 		visited_states = set()
# 		winner = -1
# 		expand = True

# 		# Simulation Start
# 		for t in range(1,self.max_actions + 1):
# 			availables = board.get_k_dist_empty_tuple(2)

# 			# Selection

# 			if all(plays.get((player,move,t)) for move in availables):

# 				total = sum(plays[(player,move,t)] for move in availables)
# 				log_total = log(total)
# 				beta = sqrt(K / (3 * total + K))
# 				value,move = max(
# 					(((1 - beta) * wins[(player,move,t)] / plays[(player,move,t)] + beta * (moves_wins[(move)] / moves[(moves)])) + 
# 					sqrt(self.confidence * log_total / plays[(player,move,t)]),move)
# 					for move in availables)

# 			else:
# 				move = random.choice(availables)

# 			board.draw_xy(move[0],move[1],player)

# 			#Expand
# 			if expand and (player,move,t) not in plays:
# 				expand = False
# 				plays[(player,move,t)] = 0
# 				wins[(player,move,t)] = 0
# 				if t > self.max_depth:
# 					self.max_depth = t

# 			visited_states.add((player,move,t))
# 			availables = board.get_k_dist_empty_tuple(2)
# 			is_full = not len(availables)
# 			winner = board.anyone_win(move[0],move[1])
			
# 			if winner is not EMPTY or is_full:
# 				#print(str(move) + '----' + str(winner) + '-----' + str(player))
# 				break

# 			player = self.player_change(player)

# 		for player, move, t in visited_states:
# 			if (player,move,t) not in plays:
# 				continue
# 			plays[(player,move,t)] += 1

# 			if player == winner:
# 				wins[(player,move,t)] += 1






# 	def select_best_move(self):
# 		empty_set = self.board.get_k_dist_empty_tuple(2)
# 		# for move in empty_set:
# 		# 	ratio = (self.wins.get((self.player,move),0)/
# 		# 		self.plays.get((self.player,move),1))
# 		# 	print(move)
# 		# 	print(ratio)

# 		#print(empty_set)
# 		raio_to_win,move = max(
# 			(self.wins.get((self.player,move,1),0)/
# 				self.plays.get((self.player,move,1),1) + self.closest_value(move),
# 				move)
# 			for move in empty_set)
# 		print(raio_to_win)
# 		return move


# 	def closest_value(self,move):
# 		x = move[0]
# 		y = move[1]
# 		return (abs((x-N_LINE + 1) * x) + abs((y-N_LINE + 1) * y)) * 0.0001


# 	def player_change(self,player):
# 		if player == BLACK:
# 			player = WHITE
# 		elif player == WHITE:
# 			player = BLACK

# 		return player



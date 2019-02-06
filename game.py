import os
from player import *

class Board:
	
	def __init__ (self, h, w):
		self.h = h
		self.w = w
		
	def init_board (self):
		self.board = [-1 for i in range (self.w * self.h)]
		self.last_put = -1
		self.availables = list (range (self.w * self.h))
		
	def idx2loc (self, idx):
		return idx // self.w, idx % self.h
		
	def loc2idx (self, *loc):
		return loc[0] * self.w + loc[1]
		
	def put (self, player_id, idx):
		self.board[idx] = player_id
		self.availables.remove (idx)
		self.last_put = idx
	
	'''
	计算与idx同色的连续长度
	direction: 0表示按行，1表示按列，2表示左上到右下斜着，3表示左下到右上斜着
	side: -1表示计算idx的左边（上面），1表示计算idx的右边（下面）
	'''
	def max_continue (self, direction, side, idx):
		x, y = self.idx2loc (idx)
		player_id = self.board[idx]
		
		x_delta = {0:0, 1:side, 2:side, 3:-side}
		y_delta = {0:side, 1:0, 2:side, 3:side}
		
		s = 0
		i = x + x_delta[direction]
		j = y + y_delta[direction]
		while (i >= 0 and i < self.h and i > x - 5 and i < x + 5
				and j >= 0 and j < self.w and j > y - 5 and j < y + 5
				and self.board[self.loc2idx(i, j)] == player_id):
			s += 1
			i += x_delta[direction]
			j += y_delta[direction]
		
		return s
	
	def is_game_over (self):
		if -1 == self.last_put:
			return False, -1
		else:
			if self.max_continue (0, -1, self.last_put) + \
				self.max_continue (0, 1, self.last_put) + 1 >= 5: # 按行检查
				return True, self.board[self.last_put]
			elif self.max_continue (1, -1, self.last_put) + \
				self.max_continue (1, 1, self.last_put) + 1 >= 5: # 按列检查
				return True, self.board[self.last_put]
			elif self.max_continue (2, -1, self.last_put) + \
				self.max_continue (2, 1, self.last_put) + 1 >= 5: # 左上右下
				return True, self.board[self.last_put]
			elif self.max_continue (3, -1, self.last_put) + \
				self.max_continue (3, 1, self.last_put) + 1 >= 5: # 左下右上
				return True, self.board[self.last_put]
			elif len (self.availables) == 0: # 棋盘摆满，不分胜负
				return True, -1
			else:
				return False, -1
				
	def game_end (self):
		return self.is_game_over ()

	def print_board (self):
		print ('Player 0 with x\nPlayer 1 with o\n')
		chess = {-1:'-', 0:'x', 1:'o'}
		
		print (end='  ')
		for i in range (self.w):
			print (i, end=' ')
		print ()
		
		for x in range (self.h):
			print (x, end=' ')
			for y in range (self.w):
				player_id = self.board[self.loc2idx(x, y)]
				print (chess[player_id], end=' ')
			print ()
		print ()

class Game:
	
	def __init__(self, board):
		self.board = board
	
	def init_game (self, start_palyer_id = 0):
		self.current_player_id = start_palyer_id
	
	def put (self, idx):
		self.board.put (self.current_player_id, idx)
		self.current_player_id ^= 1 # 切换 Player

	def start (self, players, is_show = 1):
		if is_show:
			self.board.print_board ()
		
		while True:
			idx = players[self.current_player_id].gen_action (self.board)
			self.put (idx)
			if is_show:
				loc = self.board.idx2loc (idx)
				self.board.print_board ()
			
			is_over, winner = self.board.is_game_over ()
			if is_over:
				outcome = f'Winner is Player {winner}' if \
							winner != -1 else 'Tie'
				print ('Game over. ', outcome)
				
				return winner

if __name__ == '__main__':
	board = Board (7, 7)
	board.init_board ()

	game = Game (board)
	game.init_game ()

	players = [HumanPlayer(0), AiPlayer(1)]
	game.start (players)
class Board:
	
	def __init__ (self, size):
		self.size = size
		
	def init_board (self):
		self.board = [-1 for i in range (self.size * self.size)]
		self.last_put = -1
		self.availables = list (range (self.size * self.size))
		
	def idx2loc (self, idx):
		return int (idx // self.size), int (idx % self.size)
		
	def loc2idx (self, *loc):
		return int (loc[0] * self.size + loc[1])
		
	def put (self, player_id, idx):
		self.board[idx] = player_id
		self.availables.remove (idx)
		self.last_put = idx
	
	'''
	计算与 last_put 同色的连续长度
	direction: 0表示按行，1表示按列，2表示左上到右下斜着，3表示左下到右上斜着
	side: -1表示计算idx的左边（上面），1表示计算idx的右边（下面）
	'''
	def max_continue (self, direction, side):
		idx = self.last_put
		x, y = self.idx2loc (idx)
		player_id = self.board[idx]
		
		x_delta = {0:0, 1:side, 2:side, 3:-side}
		y_delta = {0:side, 1:0, 2:side, 3:side}
		
		s = 0
		i = x + x_delta[direction]
		j = y + y_delta[direction]
		while (i >= 0 and i < self.size and i > x - 5 and i < x + 5
				and j >= 0 and j < self.size and j > y - 5 and j < y + 5
				and self.board[self.loc2idx(i, j)] == player_id):
			s += 1
			i += x_delta[direction]
			j += y_delta[direction]
		
		return s

	def print_board (self):
		print ('Player 0 with x\nPlayer 1 with o\n')
		chess = {-1:'-', 0:'x', 1:'o'}
		
		print (end='  ')
		for i in range (self.size):
			print (i, end=' ')
		print ()
		
		for x in range (self.size):
			print (x, end=' ')
			for y in range (self.size):
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

	def is_game_over (self):
		if -1 == self.board.last_put:
			return False, -1
		else:
			winner = self.board.board[self.board.last_put]
			if self.board.max_continue (0, -1) + \
				self.board.max_continue (0, 1) + 1 >= 5: # 按行检查
				return True, winner
			elif self.board.max_continue (1, -1) + \
				self.board.max_continue (1, 1) + 1 >= 5: # 按列检查
				return True, winner
			elif self.board.max_continue (2, -1) + \
				self.board.max_continue (2, 1) + 1 >= 5: # 左上右下
				return True, winner
			elif self.board.max_continue (3, -1) + \
				self.board.max_continue (3, 1) + 1 >= 5: # 左下右上
				return True, winner
			elif len (self.board.availables) == 0: # 棋盘摆满，不分胜负
				return True, -1
			else:
				return False, -1
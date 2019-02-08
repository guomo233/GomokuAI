import tkinter as tk
from tkinter import ttk
import numpy as np
from game import *
from player import *
import time

class GUI:
	
	is_over = False
	ai_player = AiPlayer (1)
	
	def __init__(self, game):
		self.game = game
		self.root = tk.Tk ()
		
	def show (self, title = 'Gomoku', board_size = 540, board_blank = 75):
		self.root.title (title)
		self.board_canvas = GUI.Board (self, board_size, board_blank, 0, 0, 5)
		self.player_hint = GUI.PlayerHint (self, 100, 0, 1)
		self.result_hint = GUI.ResultHint (self, 2, 1)
		self.ai_level_choice = GUI.AiLevelChoice (self, 3, 1)
		
		reset_button = tk.Button (self.root, text = 'Restart', font = 20, command = self.reset)
		reset_button.grid (row = 4, column = 1)
		
		self.root.mainloop ()
		
	def reset (self):
		self.board_canvas.is_over = False

		self.game.board.init_board ()
		self.game.init_game ()

		self.board_canvas.clear ()
		
		self.result_hint.update ()
		
		self.player_hint.update (0)

	class PlayerHint:
		
		color_str = ['black', 'white']
		players_str = ['Human', 'AI']
		
		def __init__ (self, parent, size, row, column, hint_size = 15):
			self.root = parent.root
			self.size = size
			self.hint_size = hint_size
			
			# 棋子
			self.canvas = tk.Canvas (self.root, width = size)
			self.canvas.grid (row = row, column = column)
			
			# 选手
			self.player_var = tk.StringVar ()
			player_hint = tk.Label (self.root, textvariable = self.player_var, font = ("Arial", 20))
			player_hint.grid (row = row + 1, column = column)

			self.update (0)
			
		def update (self, player_id):
			# 更新棋子
			self.canvas.delete ('color_hint')
			
			oval_x = self.size // 2
			oval_y = self.hint_size + 10
			self.canvas.create_oval (oval_x - self.hint_size, oval_y - self.hint_size,
						oval_x + self.hint_size, oval_y + self.hint_size,
						fill = self.color_str[player_id], tags = ('color_hint'))
			
			# 更新选手			
			self.player_var.set (self.players_str[player_id])
			
			self.root.update ()
	
	class Board:
		
		color_str = ['black', 'white']
		is_over = False
		
		def __init__(self, parent, size, blank_size, row, column, rowspan):
			self.parent = parent
			self.root = parent.root
			self.game = parent.game
			
			# 绘制棋盘背景
			self.canvas = tk.Canvas (self.root, bg = "saddlebrown", 
								width = size, 
								height = size)
			self.canvas.grid (row = row, column = column, rowspan = rowspan)
			
			# 绘制网格
			grid_size  = size - blank_size
			self.interval = grid_size / (game.board.size - 1)
			self.canvas_loc = blank_size // 2, blank_size // 2
			for i in range (game.board.size):
				self.canvas.create_line (self.canvas_loc[0], 
										(self.interval * i + self.canvas_loc[1]), 
										self.canvas_loc[0] + grid_size, 
										(self.interval * i + self.canvas_loc[1]))
				self.canvas.create_line ((self.interval * i + self.canvas_loc[0]), 
										self.canvas_loc[1], 
										(self.interval * i + self.canvas_loc[0]), 
										self.canvas_loc[1] + grid_size)

			# 绘制坐标
			for i in range (game.board.size):
				label_x = tk.Label (self.canvas, text = str(i), 
									fg = "black", bg = "saddlebrown", 
									width = 2)
				label_y = tk.Label (self.canvas, text = str(i), 
									fg = "black", bg = "saddlebrown", 
									width = 2)
				label_x.place (x = self.canvas_loc[0] - 30, 
								y = self.interval * i + self.canvas_loc[1] - 10)
				label_y.place (x = self.interval * i + self.canvas_loc[0] - 15, 
								y = self.canvas_loc[0] - 27)
			
			# 绑定鼠标点击事件
			self.canvas.bind ('<Button-1>', self.click)
			
		def click (self, event):
			if not self.is_over and game.current_player_id == 0:
				# 获取当前点击的棋盘位置
				x = int (np.round ((event.y - self.canvas_loc[1]) / self.interval))
				y = int (np.round ((event.x - self.canvas_loc[0]) / self.interval))
				
				# 如果可以落子则落子
				idx = self.game.board.loc2idx (x, y)
				if self.game.board.board[idx] == -1:
					self.put ((x, y), self.game.current_player_id)
					self.game.put (idx)
					self.parent.player_hint.update (self.game.current_player_id)
					
					# 判断游戏结束
					self.is_over, winner = self.game.is_game_over ()
					if self.is_over:
						self.parent.result_hint.update (winner)
						return
					
					# AI落子
					action = self.parent.ai_player.gen_action (game.board, is_show = 0)
					x, y = game.board.idx2loc (action)
					self.put ((x, y), self.game.current_player_id)
					self.game.put (action)
					self.parent.player_hint.update (self.game.current_player_id)
					
					self.is_over, winner = self.game.is_game_over ()
					if self.is_over:
						self.parent.result_hint.update (winner)
						return
			
		def point2loc (self, point):
			x = self.interval * point[0] + self.canvas_loc[0]
			y = self.interval * point[1] + self.canvas_loc[1]
			return x, y
			
		def put (self, point, color):
			point_size = self.interval / 4
			x, y = self.point2loc (point)
			self.canvas.create_oval (y - point_size, x - point_size, 
								y + point_size, x + point_size, 
								fill = self.color_str[color],
								tags = ('put'))
			
			self.root.update ()
			
		def clear (self):
			self.canvas.delete ('put')
			self.root.update ()
			
	class ResultHint:
		
		players_str = ['Human', 'AI']
		
		def __init__(self, parent, row, column):
			self.root = parent.root
			
			self.var = tk.StringVar ()
			label = tk.Label (self.root, textvariable = self.var, font = ("Arial", 20), fg = 'red')
			label.grid (row = row, column = column)
			
			self.update ()
			
		def update (self, winner = None):
			if winner is None:
				result = ''
			elif winner == -1:
				result = 'Tie'
			else:
				result = f'{self.players_str[winner]} Win'
			
			self.var.set (result)

	class AiLevelChoice:
		
		def __init__(self, parent, row, column, default = 3):
			self.root = parent.root
			self.parent = parent
			
			# 提示文本
			label = tk.Label (self.root, text = 'AI Level\n\n\n')
			label.grid (row = row, column = column)
			
			# 设置下拉框
			self.comboxlist = ttk.Combobox (self.root, width = 6, state = 'readonly')
			self.comboxlist['values'] = ('1', '2', '3', '4', '5')
			self.comboxlist.grid (row = row, column = column)

			self.comboxlist.current (default - 1)

			self.comboxlist.bind ('<<ComboboxSelected>>', self.choice)
			
		def choice (self, event):
			level = int (self.comboxlist.get ())
			self.parent.ai_player.set_level (level)
			
if __name__ == '__main__':
	board = Board (7)
	board.init_board ()

	game = Game (board)
	game.init_game ()

	gui = GUI (game)
	gui.show ()
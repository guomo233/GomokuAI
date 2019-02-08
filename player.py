import copy
import abc
from mcts import *
from game import *

class Player (metaclass = abc.ABCMeta):
	
		def __init__ (self, player_id):
			self.player_id = player_id
		
		@abc.abstractmethod
		def __str__ (self):
			pass
		
		@abc.abstractmethod
		def gen_action (self, board):
			pass
			
class HumanPlayer (Player):
	
	def __str__ (self):
		return f'HumanPlayer{self.player_id}'
		
	def gen_action (self, board):
		action = input (f'Player {self.player_id} put: ')
		
		try:
			loc = [int(i.strip()) for i in action.split(',')]
			idx = board.loc2idx (*loc)
			if -1 != board.board[idx]:
				raise RuntimeError ()
		except:
			print ('invalid put')
			idx = self.gen_action (board)
			
		return idx

class AiPlayer (Player):
	
	def __str__ (self):
		return f'AiPlayer{self.player_id}'
	
	def __init__(self, player_id, c_puct = 5, level = 3):
		self.mcts = MCTS (c_puct)
		self.set_level (level)
		super (AiPlayer, self).__init__ (player_id)
	
	def init_ai (self):
		self.mcts.rebuild ()
	
	def set_level (self, level):
		self.n_search = 400 * level
	
	def gen_action (self, board, is_show = 1):
		self.mcts.rebuild (board.last_put)
		
		if len (board.availables) == 1:
			return board.availables[0]
		
		for i in range (self.n_search):
			game = Game (copy.deepcopy (board))
			game.init_game (self.player_id)
			
			self.mcts.search (game)
		
		action = self.mcts.best_action ()
		self.mcts.rebuild (action)
		
		if is_show:
			loc = board.idx2loc (action)
			print (f'Player {self.player_id} put: {loc[0]},{loc[1]}')

		return action
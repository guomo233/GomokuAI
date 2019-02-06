from mcts import *
from game import *
import copy

class Player:
	
		def __init__(self, player_id):
			self.player_id = player_id
		
		def gen_action (self, board):
			pass
			
class HumanPlayer (Player):

	def gen_action (self, board):
		action = input ("put: ")
		
		loc = [int(i.strip()) for i in action.split(',')]
		idx = board.loc2idx (*loc)
		
		if -1 != board.board[idx]:
			print ('invalid put')
			idx = self.gen_action (board)
			
		return idx

class AiPlayer (Player):
	
	def __init__(self, player_id, c_puct = 1, n_search = 2000):
		self.mcts = MCTS (c_puct)
		self.n_search = n_search
		super (AiPlayer, self).__init__ (player_id)
	
	def gen_action (self, board):
		
		if board.last_put != -1:
			self.mcts.rebuild (board.last_put)
		
		if len (board.availables) == 1:
			return board.availables[0]
		
		for i in range (self.n_search):
			game = Game (copy.deepcopy (board))
			game.init_game (self.player_id)
			
			self.mcts.search (game)
		
		action = self.mcts.best_action ()
		self.mcts.rebuild (action)

		return action
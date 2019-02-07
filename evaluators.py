import copy
import numpy as np
import abc

class Evaluator (metaclass = abc.ABCMeta):
			
		def reward (self, winner, current_player):
			if winner == -1:
				return 0
			else:
				# 当前节点的 Q 是为父节点选择用，所以应该在父节点的视角来看
				return -1 if winner == current_player else 1

		'''
		返回当前状态能执行的行为和概率的元组 (action, P) 的列表，
		表示使用这样的策略来模拟评估，为 expand 所用
		'''
		@abc.abstractmethod
		def policy (self, game):
			pass
		
		@abc.abstractmethod
		def evaluate (self, game):
			pass

class MCEvaluator (Evaluator):
	
	def policy (self, game):
		actions = copy.deepcopy (game.board.availables)
		n_actions = len (actions)
		
		# 在此每个 action 的 P = (1 / 空位数)
		return zip (actions, np.ones (n_actions) / n_actions)
	
	def evaluate (self, game):
		current_player_id = game.current_player_id
		
		while True:
			is_over, winner = game.is_game_over ()
			if is_over:
				break
			
			action = np.random.choice (game.board.availables)
			game.put (action)

		return self.reward (winner, current_player_id)

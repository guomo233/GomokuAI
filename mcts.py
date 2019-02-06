import numpy as np
from policy import *

class MCTNode:
	
	def __init__(self, P = 1, parent = None):
		self.parent = parent
		self.childs = {} # action -> node
		self.Q = 0
		self.n = 0
		self.P = P
		
	def select (self, c_puct):
		return max (self.childs.items(), 
					key = lambda child: child[1].PUCT (c_puct))
	
	'''
	要在 select 时计算，而不能 update 的时候算，
	因为节点没经过 update 其 PUCT 值也可能变化
	'''
	def PUCT (self, c_puct):
		U = self.P * c_puct * np.sqrt (self.parent.n) / (1 + self.n)
		return self.Q + U
	
	def expand (self, actions):
		for action, P in actions:
			if action not in self.childs:
				self.childs[action] = MCTNode (P, self)
	
	def update (self, R):
		self.n += 1
		self.Q += 1.0 * (R - self.Q) / self.n

	def is_leaf (self):
		return self.childs == {}
		
	def is_root (self):
		return self.parent is None

class MCTS:
	
	def __init__ (self, c_puct):
		self.c_puct = c_puct
		self.root = MCTNode ()
	
	def select (self):
		node = self.root
		actions = []
		while not node.is_leaf():
			action, node = node.select (self.c_puct)
			actions.append (action)
		
		return actions, node
	
	def update (self, node, R):
		node.update (R)
		if node.parent is not None:
			self.update (node.parent, -R)
	
	def rebuild (self, last_put):
		if last_put in self.root.childs:
			self.root = self.root.childs[last_put]
			self.root.parent = None
		else:
			self.root = MCTNode ()

	def best_action (self):
		return max (self.root.childs.items(), 
					key = lambda item: item[1].Q)[0]
	
	def search (self, game, evaluator = MCEvaluator ()):
		actions, node = self.select ()
		for action in actions:
			game.put (action)
		
		is_over, winner = game.board.is_game_over ()
		if not is_over:
			actions = evaluator.policy (game)
			node.expand (actions)
			R = evaluator.evaluate (game)
		else:
			R = evaluator.reward (winner, game.current_player_id)
		
		self.update (node, R)
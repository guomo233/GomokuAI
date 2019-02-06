import numpy as np
import copy

'''
返回当前状态能执行的行为和概率的元组 (action, P) 的列表，以及状态估值
其中 action 和 P 为 expand 所用，状态估值为 update 所用
之所以将 expand 和 update 所需的都一起返回，是为了和 net_evaluate 统一，
在此每个 action 的 P = 1 / 空位
'''
def MC_evaluate (game):
	current_player_id = game.current_player_id

	n_availables = len (game.board.availables)
	actions = zip (copy.deepcopy (game.board.availables), 
					np.ones (n_availables) / n_availables)
	
	while True:
		is_over, winner = game.board.is_game_over ()
		if is_over:
			break
		
		action = np.random.choice (game.board.availables)
		game.put (action)

	if winner == -1:
		return actions, 0
	else:
		return actions, (1 if winner == current_player_id else -1)

class MCTNode:
	
	def __init__(self, P = 1, parent = None):
		self.parent = parent
		self.childs = {} # action -> node
		self.Q = 0
		self.n = 0
		self.PUCT = 0
		self.P = P
		
	def select (self):
		return max (self.childs.items(), 
					key = lambda child: child[1].PUCT)
	
	def expand (self, actions):
		for action, P in actions:
			if action not in self.childs:
				self.childs[action] = MCTNode (P, self)
	
	def update (self, R, c_puct):
		self.n += 1
		self.Q += 1.0 * (R - self.Q) / self.n
		if not self.is_root ():
			U = self.P * c_puct * np.sqrt (self.parent.n) / (1 + self.n)
			self.PUCT = self.Q + U

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
			action, node = node.select ()
			actions.append (action)
		
		return actions, node
	
	def update (self, node, R):
		node.update (R, self.c_puct)
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
					key = lambda item: item[1].n)[0]
	
	def search (self, game, evaluator = MC_evaluate):
		actions, node = self.select ()
		for action in actions:
			game.put (action)
		
		actions, R = evaluator (game)
		node.expand (actions)
		self.update (node, R)
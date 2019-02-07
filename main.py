from game import *
from player import *

def start (game, players, is_show = 1):
	if is_show:
		game.board.print_board ()
	
	while True:
		idx = players[game.current_player_id].gen_action (game.board)
		game.put (idx)
		if is_show:
			loc = game.board.idx2loc (idx)
			game.board.print_board ()
		
		is_over, winner = game.is_game_over ()
		if is_over:
			outcome = f'Winner is Player {winner}' if \
						winner != -1 else 'Tie'
			print ('Game over. ', outcome)
			
			return winner

board = Board (7)
board.init_board ()

game = Game (board)
game.init_game ()

players = [HumanPlayer(0), AiPlayer(1)]
start (game, players)
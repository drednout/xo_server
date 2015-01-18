import uuid
import random

import xo_engine.game as xo_engine
import xo_server.common.error as error




class SimpleGame(object):
    def __init__(self, player):
        self.player = player
        self.game_id = str(uuid.uuid4())
        game_field = xo_engine.GameField()
        possible_cell_types = [xo_engine.CELL_STATE_O, xo_engine.CELL_STATE_X]
        live_player_cell = random.choice(possible_cell_types)
        possible_cell_types.remove(live_player_cell)
        computer_player_cell = possible_cell_types.pop()
        player1 = xo_engine.Player(player.id, player.nickname, live_player_cell)
        player2 = xo_engine.Player(-1, "Computer", computer_player_cell)
        self.game = xo_engine.Game(game_field, [player1, player2])
        self.live_player = player1
        self.computer_player = player2

        self.possible_moves = {}
        for i in xrange(xo_engine.DEFAULT_FIELD_WIDTH):
            for j in xrange(xo_engine.DEFAULT_FIELD_HEIGHT):
                move = (i, j)
                self.possible_moves.setdefault(move, None)

        if computer_player_cell == xo_engine.CELL_STATE_X:
            self.make_computer_move()


    def make_computer_move(self):
        random_move = random.choice(self.possible_moves.keys())
        if random_move not in self.possible_moves:
            raise error.EInternalError(error.ERROR_INVALID_MOVE)
        self.game.make_move(self.computer_player, random_move[0], random_move[1])
        del self.possible_moves[random_move]

    def make_player_move(self, move_x, move_y):
        player_move = (move_x, move_y)
        if player_move not in self.possible_moves:
            raise error.EInternalError(error.ERROR_INVALID_MOVE)

        self.game.make_move(self.live_player, move_x, move_y)
        del self.possible_moves[player_move]

    def check_game_over(self):
        return self.game.check_game_over()

    def get_winner(self):
        return self.game.get_winner()

    def as_dict(self):
        game_as_dict = {
            "id": self.game_id,
            "player_id": self.player.id,
            "game": self.game.as_dict(),
        }
        return game_as_dict
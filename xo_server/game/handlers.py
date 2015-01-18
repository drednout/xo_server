import cyclone.web
from twisted.internet import defer
from twisted.python import log

from xo_server.common.singletone import service
import xo_server.model.player as player_model
import xo_server.model.session as session_model
import xo_server.model.game as game_model
import xo_server.common.error as error


class HelloHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write("Hello from {} service.".format(service.name))

class LoginHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write(self.__class__.__name__)


    @defer.inlineCallbacks
    def post(self):
        sid = self.get_argument("sid")

        session = session_model.Session(sid=sid)
        yield session.load_by_sid()
        service.sessions[sid] = session

        player = player_model.Player(id=session.player_id)
        yield player.load_by_id()

        service.players[session.player_id] = player
        resp = {
            "player_id": player.id,
        }
        self.write(service.pack(resp))


def validate_sid(sid):
    if sid not in service.sessions:
        raise error.EInternalError(error.ERROR_INVALID_SID)


def get_player(sid):
    session = service.sessions[sid]
    player = service.players[session.player_id]
    return player

class GetProfileHandler(cyclone.web.RequestHandler):
    def get(self):
        sid = self.get_argument("sid")
        validate_sid(sid)
        player = get_player(sid)
        resp = {
            "player": player.as_dict(),
        }
        self.write(service.pack(resp))


class StartSimpleGame(cyclone.web.RequestHandler):
    def post(self):
        sid = self.get_argument("sid")
        validate_sid(sid)
        player = get_player(sid)
        simple_game = game_model.SimpleGame(player)
        service.games[player.id] = simple_game
        resp = {
            "game": simple_game.as_dict(),
        }
        self.write(service.pack(resp))


class GetCurrentGame(cyclone.web.RequestHandler):
    def get(self):
        sid = self.get_argument("sid")
        validate_sid(sid)
        player = get_player(sid)
        simple_game = None
        if player.id in service.games:
            simple_game = service.games[player.id]

        resp = {
            "game": simple_game.as_dict(),
        }
        self.write(service.pack(resp))


class MakeMove(cyclone.web.RequestHandler):
    @defer.inlineCallbacks
    def post(self):
        sid = self.get_argument("sid")
        validate_sid(sid)
        x = int(self.get_argument("x"))
        y = int(self.get_argument("y"))
        player = get_player(sid)

        if player.id not in service.games:
            raise error.EInternalError(error.ERROR_NO_ACTIVE_GAMES)

        simple_game = service.games[player.id]
        simple_game.make_player_move(x, y)
        is_game_over = simple_game.check_game_over()
        if not is_game_over:
            simple_game.make_computer_move()
        is_game_over = simple_game.check_game_over()
        if is_game_over:
            winner = simple_game.get_winner()
            if winner is None:
                #draw, do nothing
                pass
            elif winner == simple_game.computer_player:
                yield player.take_exp(player_model.SIMPLE_GAME_LOOSE_EXP_DELTA)
            elif winner == simple_game.live_player:
                yield player.give_exp(player_model.SIMPLE_GAME_WIN_EXP_DELTA)

        resp = {
            "game": simple_game.as_dict(),
        }
        self.write(service.pack(resp))


HANDLERS_LIST = [
    (r"/", HelloHandler),
    (r"/login", LoginHandler),
    (r"/get_profile", GetProfileHandler),
    (r"/start_simple_game", StartSimpleGame),
    (r"/get_current_game", GetCurrentGame),
    (r"/make_move", MakeMove),
    (r"/get_rating", HelloHandler),
]

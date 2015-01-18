import cyclone.web
from twisted.internet import defer
from twisted.python import log

from xo_server.common.singletone import service
import xo_server.model.player as player_model
import xo_server.model.session as session_model
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


HANDLERS_LIST = [
    (r"/", HelloHandler),
    (r"/login", LoginHandler),
    (r"/get_profile", HelloHandler),
    (r"/start_simple_game", HelloHandler),
    (r"/make_move", HelloHandler),
    (r"/get_rating", HelloHandler),
]

import cyclone.web
from twisted.python import log
from twisted.internet import defer

from xo_server.common.singletone import service
import xo_server.model.player as player_model
import xo_server.model.session as session_model
import xo_server.common.error as error


class HelloHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write("Hello from {} service.".format(service.name))


class RegisterEmailHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write(self.__class__.__name__)

    @defer.inlineCallbacks
    def post(self):
        email = self.get_argument("email")
        nickname = self.get_argument("nickname")
        password = self.get_argument("password")
        password_repeat = self.get_argument("password_repeat")

        log.msg("email is {}".format(email))
        log.msg("password is {}".format(password))

        if password != password_repeat:
            raise error.EInternalError(error.ERROR_PASSWORD_NOT_MATCH)

        new_player = player_model.Player(
                        nickname=nickname,
                        email=email,
                        password=password,
                     )
        is_exists = yield new_player.is_exists()
        if is_exists:
            raise error.EInternalError(error.ERROR_PLAYER_IS_EXISTS)

        yield new_player.insert()
        new_session = session_model.Session(player_id=new_player.id)
        yield new_session.insert()

        msg = {
            "player_id": new_player.id
        }
        res = yield service.broker.send_broker_msg(exchange="bind_fanout",
                                                   f_name="bind", msg=msg)
        game_service_id = res["game_service_id"]
        game_service_info = yield service.redis_db.get_service_info("game", game_service_id)

        resp = {
            "sid": new_session.sid,
            "game_service_info": game_service_info,

        }
        self.write(service.pack(resp))



class LoginEmailHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write(self.__class__.__name__)


    @defer.inlineCallbacks
    def post(self):
        email = self.get_argument("email")
        password = self.get_argument("password")

        log.msg("email is {}".format(email))
        log.msg("password is {}".format(password))


        player = player_model.Player(
                     email=email,
                     password=password,
                 )
        can_login = yield player.can_login()
        if not can_login:
            raise error.EInternalError(error.ERROR_BAD_LOGIN_OR_PASSWORD)

        yield player.load_by_email()

        new_session = session_model.Session(player_id=player.id)
        yield new_session.insert()

        msg = {
            "player_id": player.id
        }
        game_service_id = yield service.redis_db.get_player_server(player.id)
        if game_service_id is None:
            res = yield service.broker.send_broker_msg(exchange="bind_fanout",
                                                       f_name="bind", msg=msg)
            game_service_id = res["game_service_id"]

        game_service_info = yield service.redis_db.get_service_info("game", game_service_id)

        resp = {
            "sid": new_session.sid,
            "game_service_info": game_service_info,
        }
        self.write(service.pack(resp))



HANDLERS_LIST = [
    (r"/", HelloHandler),
    (r"/register/email", RegisterEmailHandler),
    (r"/login/email", LoginEmailHandler)
]

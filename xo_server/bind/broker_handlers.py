from twisted.internet import defer

from xo_server.common.singletone import service

@defer.inlineCallbacks
def handle_ping(_):
    yield 1
    resp = {
        "res": "PONG"
    }
    defer.returnValue(resp)


@defer.inlineCallbacks
def handle_bind(msg):
    player_id = msg["player_id"]
    game_service_id = yield service.redis_db.get_the_laziest_service("game")
    yield service.redis_db.bind_player(player_id, game_service_id)
    resp = {
        "game_service_id": game_service_id,
    }
    defer.returnValue(resp)


HANDLERS_MAP = {
    "ping": handle_ping,
    "bind": handle_bind,
}

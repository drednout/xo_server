from twisted.internet import defer

from xo_server.common.singletone import service

@defer.inlineCallbacks
def handle_ping(_):
    yield 1
    resp = {
        "res": "PONG"
    }
    defer.returnValue(service.pack(resp))


HANDLERS_MAP = {
    "ping": handle_ping,
}

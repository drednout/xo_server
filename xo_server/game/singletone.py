from twisted.internet import defer

import xo_server.common.singletone as common_singletone


class GameServiceSingletone(common_singletone.ServiceSingletone):
    def __init__(self):
        super(common_singletone.ServiceSingletone, self).__init__()
        self.players = {}
        self.sessions = {}


    @defer.inlineCallbacks
    def initialize(self):
        yield common_singletone.ServiceSingletone.initialize(self)


    @defer.inlineCallbacks
    def finalize(self):
        yield 1




service = GameServiceSingletone()

from twisted.internet import defer

import xo_server.common.sql_db as sql_db


class ServiceSingletone(object):
    def __init__(self):
        self.name = None
        self.config = None

    @defer.inlineCallbacks
    def initialize(self):
        yield 1
        self.sql_db = sql_db.ConnectionPool(**self.config["mysql"])
        #db ping
        yield service.sql_db.runQuery("SELECT 1")


    @defer.inlineCallbacks
    def finalize(self):
        yield 1



service = ServiceSingletone()

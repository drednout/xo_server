from twisted.internet import defer

import xo_server.common.sql_db as sql_db
import xo_server.common.serialization_adapter as serialization_adapter


class ServiceSingletone(object):
    def __init__(self):
        self.name = None
        self.config = None
        self.serialization_adapter = None

    @defer.inlineCallbacks
    def initialize(self):
        yield 1
        self.sql_db = sql_db.ConnectionPool(**self.config["mysql"])
        #db ping
        yield self.sql_db.runQuery("SELECT 1")

        serialization_format = self.config["serialization_format"]
        self.serialization_adapter = serialization_adapter.getSerialiazationAdapter(serialization_format)


    @defer.inlineCallbacks
    def finalize(self):
        yield 1


    def pack(self, msg):
        return self.serialization_adapter.pack(msg)


    def unpack(self, msg):
        return self.serialization_adapter.unpack(msg)



service = ServiceSingletone()

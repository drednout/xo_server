from twisted.internet import defer
from twisted.python import log

import xo_server.common.sql_db as sql_db
import xo_server.common.serialization_adapter as serialization_adapter
import xo_server.common.rabbitmq as rabbitmq

class ServiceSingletone(object):
    def __init__(self):
        self.name = None
        self.config = None
        self.serialization_adapter = None
        self.players = {}
        self.sessions = {}
        self.games = {}
        self.sql_db = None
        self.broker = None
        self.broker_handler_map = None

    @defer.inlineCallbacks
    def initialize(self):
        yield 1
        self.sql_db = sql_db.ConnectionPool(**self.config["mysql"])
        #db ping
        yield self.sql_db.runQuery("SELECT 1")

        serialization_format = self.config["serialization_format"]
        self.serialization_adapter = serialization_adapter.getSerialiazationAdapter(serialization_format)

        self.broker = rabbitmq.RabbitmqBroker(self, self.config, self.name, self.name,
                                              handlers_map=self.broker_handler_map)
        yield self.broker.connect_broker()
        res = yield self.broker.send_broker_msg(exchange=self.name, f_name="ping", msg={})
        log.msg("Broker msg PING res: {}".format(res))

    @defer.inlineCallbacks
    def finalize(self):
        yield 1

    def pack(self, msg):
        return self.serialization_adapter.pack(msg)

    def unpack(self, msg):
        return self.serialization_adapter.unpack(msg)

service = ServiceSingletone()

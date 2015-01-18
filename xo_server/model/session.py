import hashlib
import datetime

from twisted.internet import defer
from twisted.python import log

from xo_server.common.singletone import service
import xo_server.common.error as error


class Session(object):
    table_name = "sessions"

    def __init__(self, player_id=None, ip_addr=None,
                 sid=None):
        self.player_id = player_id
        self.ip_addr = ip_addr
        self.sid = sid
        self.id = None

    def generate_sid(self):
        sha1_object = hashlib.sha1("{}{}{}".format(
                            self.player_id, 
                            datetime.datetime.now(),
                            service.config["server_salt"])
                      )
        return sha1_object.hexdigest()


    @defer.inlineCallbacks
    def insert(self):
        if self.sid is None:
            self.sid = self.generate_sid()

        sql_cmd = """INSERT INTO sessions (player_id, sid, ip_addr,
                     created, updated) VALUES
                     (%(player_id)s, %(sid)s, %(ip_addr)s, utc_timestamp(),
                     utc_timestamp())"""
        sql_data = {
            "player_id": self.player_id,
            "sid": self.sid,
            "ip_addr": self.ip_addr,
        }
        player_id = yield service.sql_db.runInteraction(sql_cmd, sql_data)
        self.id = player_id


    @defer.inlineCallbacks
    def load_by_sid(self):
        sql_cmd = """SELECT id, player_id, ip_addr, created, updated FROM
                     sessions WHERE sid=%(sid)s"""
        sql_data = {
            "sid": self.sid,
        }
        session_info = yield service.sql_db.runQuery(sql_cmd, sql_data)
        if not session_info:
            raise error.EInternalError(error.ERROR_INVALID_SID)

        session_info = session_info[0]
        for attr_name, value in session_info.iteritems():
            setattr(self, attr_name, value)



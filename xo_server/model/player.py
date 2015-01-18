import hashlib

from twisted.internet import defer

from xo_server.common.singletone import service
import xo_server.common.error as error


def calc_password_hash(password):
    #TODO: use more robust security schema using
    #separate salt for each user
    data = "{}{}".format(password, service.config["server_salt"])
    return hashlib.sha1(data).hexdigest()



class Player(object):
    table_name = "players"

    def __init__(self, nickname=None, xp=0, email=None,
                 password=None, id=None):
        self.nickname = nickname
        self.xp = xp
        self.email = email
        self.password = password
        self.password_hash = None
        if password is not None:
            self.password_hash = calc_password_hash(self.password)
        self.id = id
        self.created = None
        self.updated = None


    @defer.inlineCallbacks
    def is_exists(self):
        sql_cmd = """SELECT COUNT(*) as player_count FROM players WHERE
                     nickname=%(nickname)s OR email=%(email)s"""
        sql_args = {
            "nickname": self.nickname,
            "email": self.email,
        }
        res = yield service.sql_db.runQuery(sql_cmd, sql_args)
        is_exists = False
        if res[0]["player_count"] > 0:
            is_exists = True

        defer.returnValue(is_exists)


    @defer.inlineCallbacks
    def can_login(self):
        if self.password_hash is None:
            raise error.EInternalError(error.ERROR_NO_PASSWORD_HASH)

        sql_cmd = """SELECT COUNT(*) as player_count FROM players WHERE
                     email=%(email)s AND password_hash=%(password_hash)s"""
        sql_args = {
            "email": self.email,
            "password_hash": self.password_hash,
            }
        res = yield service.sql_db.runQuery(sql_cmd, sql_args)
        can_login = False
        if res[0]["player_count"] > 0:
            can_login = True

        defer.returnValue(can_login)


    @defer.inlineCallbacks
    def insert(self):
        if self.password_hash is None:
            self.password_hash = calc_password_hash(self.password)

        sql_cmd = """INSERT INTO players (nickname, xp, email, 
                     password_hash, created, updated) VALUES
                     (%(nickname)s, %(xp)s, %(email)s, %(password_hash)s,
                     utc_timestamp(), utc_timestamp())"""
        sql_data = {
            "nickname": self.nickname,
            "email": self.email,
            "xp": self.xp,
            "password_hash": self.password_hash,
        }
        player_id = yield service.sql_db.runInteraction(sql_cmd, sql_data)
        self.id = player_id



    @defer.inlineCallbacks
    def update(self):
        yield 1


    @defer.inlineCallbacks
    def load_by_email(self):
        sql_cmd = """SELECT id, nickname, xp, email, created, updated FROM
                     players WHERE email=%(email)s"""
        sql_data = {
            "email": self.email,
        }
        player_info = yield service.sql_db.runQuery(sql_cmd, sql_data)
        if not player_info:
            raise error.EInternalError(error.ERROR_INVALID_PLAYER_EMAIL)

        player_info = player_info[0]
        for attr_name, value in player_info.iteritems():
            setattr(self, attr_name, value)


    @defer.inlineCallbacks
    def load_by_id(self):
        sql_cmd = """SELECT id, nickname, xp, email, created, updated FROM
                     players WHERE id=%(id)s"""
        sql_data = {
            "id": self.id,
        }
        player_info = yield service.sql_db.runQuery(sql_cmd, sql_data)
        if not player_info:
            raise error.EInternalError(error.ERROR_INVALID_PLAYER_ID)

        player_info = player_info[0]
        for attr_name, value in player_info.iteritems():
            setattr(self, attr_name, value)

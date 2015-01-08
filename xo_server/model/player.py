import hashlib

from twisted.internet import defer

from xo_server.common.singletone import service


def calc_password_hash(password):
    #TODO: use more robust security schema using
    #separate salt for each user
    data = "{}{}".format(password, service.config["server_salt"])
    return hashlib.sha1(data).hexdigest()



class Player(object):
    table_name = "players"

    def __init__(self, nickname=None, xp=0, email=None,
                password=None):
        self.nickname = nickname
        self.xp = xp
        self.email = email
        self.password = password
        self.password_hash = None
        self.id = None


    @defer.inlineCallbacks
    def is_exists(self):
        sql_cmd = """SELECT COUNT(*) as player_count FROM players WHERE
                     nickname=%(nickname)s OR email=%(email)s"""
        sql_args = {
            "nickname": self.nickname,
            "email": self.email,
        }
        res = yield service.sql_cmd.runQuery(sql_cmd, sql_args)
        is_exists = False
        if res[0]["player_count"] > 0:
            is_exists = True

        defer.returnValue(is_exists)

    

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
    def load_by_email(self, email):
        yield 1

import time
from datetime import datetime

from twisted.internet import defer, reactor, protocol
from txredis.client import RedisClient
from twisted.python import log


class RedisDb(object):
    def __init__(self, config, current_service, service_id):
        self.current_service = current_service
        self.service_id = service_id
        self.config = config
        self.host = None
        self.port = None
        if ("service" in self.config and
                "host" in self.config["service"]):
            self.host = self.config["service"]["host"]
        if ("service" in self.config and
                "port" in self.config["service"]):
            self.port = self.config["service"]["port"]
        self.service_key = "%s:%d" % (self.current_service, self.service_id)
        self.ttl = 3600
        self.redis_db = None



    @defer.inlineCallbacks
    def connect(self):
        clientCreator = protocol.ClientCreator(reactor, RedisClient)
        self.redis_db = yield clientCreator.connectTCP(self.config["redis"]["host"],
                                                       self.config["redis"]["port"])
        if "password" in self.config["redis"]:
            yield self.redis_db.auth(self.config["redis"]["password"])
        yield self.redis_db.select(self.config["redis"]["db"])
        res = yield self.redis_db.ping()
        log.msg("RedisDB ping answer is {}".format(res))


    @defer.inlineCallbacks
    def service_heart_beat(self):
        yield self.redis_db.expire(self.service_key, self.ttl)
        reactor.callLater(30, self.service_heart_beat)


    def _unix_timestamp(self):
        return time.mktime(datetime.now().timetuple())


    @defer.inlineCallbacks
    def bind_person(self, person_id, game_service_id):
        service_key = "game_service:%d" % game_service_id
        yield self.redis_db.hset("person:%d" % person_id, "gs_id", game_service_id)
        yield self.redis_db.sadd(service_key + "_persons", person_id)

        service_list = "game_services"
        yield self.redis_db.zincrby(service_list, 1, game_service_id)


    @defer.inlineCallbacks
    def get_person_server(self, person_id):
        server_info = yield self.redis_db.hget("person:%d" % person_id, "gs_id")
        
        server_id = None
        if server_info:
            server_id = int(server_info["gs_id"])
        defer.returnValue(server_id)

    @defer.inlineCallbacks
    def is_my_person(self, person_id):
        res = yield self.redis_db.sismember("game_service:%d_persons" % self.service_id, person_id)
        defer.returnValue(bool(int(res)))

    @staticmethod
    def _get_service_list(service_name):
        return service_name + "s"

    @defer.inlineCallbacks
    def get_the_laziest_service(self, service_name):
        service_list = self._get_service_list(service_name)
        raw_server_id = yield self.redis_db.zrange(service_list, 0, 0)
        server_id = None
        if raw_server_id:
            server_id = int(raw_server_id[0])
        defer.returnValue(server_id)


    @defer.inlineCallbacks
    def get_service_info(self, service_name, service_id):
        service_info = yield self.redis_db.hgetall("%s:%d" % (service_name, service_id))
        if service_info:
            service_info["id"] = service_id 
        defer.returnValue(service_info)


    @defer.inlineCallbacks
    def is_new_person(self, person_id):
        is_exists = yield self.redis_db.exists("person:%d" % person_id)
        is_new = not bool(int(is_exists))
        defer.returnValue(is_new)


    @defer.inlineCallbacks
    def service_started(self):
        service_list = self._get_service_list(self.current_service)
        yield self.redis_db.zadd(service_list, 0, self.service_id)
        yield self.redis_db.hset(self.service_key, "started", self._unix_timestamp())
        yield self.redis_db.hset(self.service_key, "id", self.service_id)
        if self.host:
            yield self.redis_db.hset(self.service_key, "host", self.host)
        if self.port:
            yield self.redis_db.hset(self.service_key, "port", self.port)
        yield self.service_heart_beat()


    @defer.inlineCallbacks
    def service_stopped(self):
        service_list = self._get_service_list(self.current_service)
        yield self.redis_db.zrem(service_list, self.service_id)
        yield self.redis_db.zadd(self.service_list, 0, self.service_id)
        yield self.redis_db.delete(self.service_key)



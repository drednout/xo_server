import cyclone.web

from xo_server.common.singletone import service

class HelloHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write("Hello from {} service.".format(service.name))


HANDLERS_LIST = [
    (r"/", HelloHandler),
    (r"/login", HelloHandler),
    (r"/get_profile", HelloHandler),
    (r"/start_simple_game", HelloHandler),
    (r"/make_move", HelloHandler),
    (r"/get_rating", HelloHandler),
]

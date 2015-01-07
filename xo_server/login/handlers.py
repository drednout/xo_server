import cyclone.web

from xo_server.common.singletone import service


class HelloHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write("Hello from {} service.".format(service.name))


class RegisterEmailHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write(self.__class__.__name__)


class LoginEmailHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write(self.__class__.__name__)



HANDLERS_LIST = [
    (r"/", HelloHandler),
    (r"/register/email", RegisterEmailHandler),
    (r"/login/email", LoginEmailHandler)
]

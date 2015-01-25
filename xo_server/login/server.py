import sys
import os
import argparse

from twisted.internet import reactor, defer
from twisted.python import log
import cyclone.web

import xo_server.common.utils as xo_utils
from xo_server.login.handlers import HANDLERS_LIST
from xo_server.common.singletone import service
from xo_server.game.broker_handlers import HANDLERS_MAP



@defer.inlineCallbacks
def main():
    log.startLogging(sys.stdout)
    parser = argparse.ArgumentParser(description='Login service for XO game.')
    parser.add_argument('path_to_config', metavar='FILENAME', 
                        type=str, nargs=1,
                        help='path to the server configuration file')
    args = parser.parse_args()
    log.msg("args are {}".format(args))

    path_to_config = args.path_to_config[0]
    if not os.path.exists(path_to_config):
        log.err("Config file {} does not exists!".format(path_to_config))
        sys.exit(1)

    config = xo_utils.load_config(path_to_config)

    application = cyclone.web.Application(HANDLERS_LIST)

    service.name = "login"
    service.config = config
    service.service_id = 1
    service.broker_handler_map = HANDLERS_MAP
    if "XO_SERVICE_ID" in os.environ:
        service.service_id = int(os.environ["XO_SERVICE_ID"])

    try:
        yield service.initialize()
    except:
        reactor.callLater(0, reactor.stop)
        raise

    reactor.listenTCP(config["service"]["port"], application,
                      interface=config["service"]["host"])



if __name__ == "__main__":
    reactor.callWhenRunning(main)
    reactor.run()

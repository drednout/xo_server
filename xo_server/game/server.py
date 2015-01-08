import sys
import os
import argparse

from twisted.internet import reactor, defer
from twisted.python import log
import cyclone.web

import xo_server.common.utils as xo_utils
from xo_server.game.handlers import HANDLERS_LIST
from xo_server.common.singletone import service



@defer.inlineCallbacks
def main():
    parser = argparse.ArgumentParser(description='Game server for XO game.')
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

    service.name = "game"
    service.config = config
    try:
        yield service.initialize()
    except:
        reactor.callLater(0, reactor.stop)
        raise

    log.startLogging(sys.stdout)
    reactor.listenTCP(config["service"]["port"], application, 
                      interface=config["service"]["host"])



if __name__ == "__main__":
    reactor.callWhenRunning(main)
    reactor.run()

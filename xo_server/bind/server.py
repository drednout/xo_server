import sys
import os
import argparse

from twisted.internet import reactor, defer
from twisted.python import log

import xo_server.common.utils as xo_utils
from xo_server.common.singletone import service
from xo_server.game.broker_handlers import HANDLERS_MAP



@defer.inlineCallbacks
def main():
    parser = argparse.ArgumentParser(description='Bind service for XO game.')
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

    log.startLogging(sys.stdout)

    service.name = "bind"
    service.config = config
    service.broker_handler_map = HANDLERS_MAP
    try:
        yield service.initialize()
    except:
        reactor.callLater(0, reactor.stop)
        raise


if __name__ == "__main__":
    reactor.callWhenRunning(main)
    reactor.run()

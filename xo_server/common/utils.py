import logging
import re

import yaml
from twisted.internet import reactor, defer

def defer_sleep(secs):
    d = defer.Deferred()
    reactor.callLater(secs, d.callback, None)
    return d

def super_include(config_as_str):
    include_list = re.findall('(!include (\S+))', config_as_str)
    logging.debug("include_list is {0}".format(include_list))
    for include_entry in include_list:
        logging.debug("include_entry is {0}".format(include_entry))
        raw_yaml = open(include_entry[1]).read()
        replaced_yaml = super_include(raw_yaml)
        config_as_str = config_as_str.replace(include_entry[0], replaced_yaml)
    return config_as_str


def load_config(config_path):
    config_as_str = super_include(open(config_path).read())
    config = yaml.load(config_as_str)
    return config

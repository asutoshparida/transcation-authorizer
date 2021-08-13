'''
Entry point for the authorizer processor application.
'''
import importlib
import sys
import json
import logging
from logging.config import dictConfig
import yaml
from pkg_resources import resource_stream
from .plugin.component import Component
from .handler.MemoryStorage import MemoryStorage
from .handler.RateLimit import RateLimit
import fileinput

# setup logger
dictConfig(yaml.load(resource_stream(__name__, 'logging.yaml'), Loader=yaml.FullLoader))
log = logging.getLogger('authorize')


def main():
    '''
    Parse the arguments and call the authorizers code.
    '''
    log.debug("inside main :")
    memoryStorage = MemoryStorage()
    rateLimit = RateLimit()
    for line in fileinput.input():
        try:
            line_json = line.rstrip()
            log.info('in transaction:' + str(line_json))

            client_config = json.loads(line_json)
            log.debug('client_config :' + str(client_config))

            res = list(client_config.keys())[0]
            log.debug('res :' + str(res))

            instance = init_component(res.title())
            response_obj = instance.run(line_json, memoryStorage, rateLimit)
            response_json = json.dumps(response_obj, default=lambda obj: obj.__dict__, sort_keys=True)

            log.info('out transaction:' + str(response_json))
        except Exception as e:
            log.error("ERROR !" + e.__class__ + "occurred for:" + line_json)
            log.error("ERROR !" + e)

    log.info('memoryStorage size:' + str(len(memoryStorage.transaction_list)))

def init_component(class_name):
    '''
    Plugin component factory.
    '''
    # This allows a shorter name in the config file.
    component_class = getattr(importlib.import_module("." + class_name, package="authorizer.action"), class_name)

    # Ensure that this is a proper subclass.
    if not issubclass(component_class, Component):
        msg = component_class + ' is NOT a subclass of Component'
        log.error(msg)
        raise ValueError(msg)

    # Create the instance.
    instance = component_class(log)

    # Return the new instance.
    return instance


if __name__ == '__main__':
    sys.exit(main())

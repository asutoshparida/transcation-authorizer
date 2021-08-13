'''
    Base Component Class
'''
import abc
import json
import os
from types import SimpleNamespace

class Component(object, metaclass=abc.ABCMeta):
    '''
    Base class - All component class must implement this
    '''

    @abc.abstractmethod
    def run(self, json_str, memory_storage, rate_limit):
        '''
        Must accept an json_str and memoryStorage and rate_limit
        requried to process the transaction
        '''


    def __init__(self, log):
        log = self.log

    @staticmethod
    def convert_json_to_obj(json_data):
        '''
        Convert json str to SimpleNamespace
        '''
        return json.loads(json_data, object_hook=lambda attribute: SimpleNamespace(**attribute))

    @staticmethod
    def get_response_obj():
        '''
        prepare response object.
        '''
        return {"account": {"active-card": False, "available-limit": 0}, "violations": []}



# Disable warning as this is intended to be abstract class.
class Action(Component, metaclass=abc.ABCMeta):
    '''
    Base class for all transactions.
    '''

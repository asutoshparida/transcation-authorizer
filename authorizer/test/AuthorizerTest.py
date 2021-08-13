"""
AuthorizerTest.py
~~~~~~~~~~~~~~~

This module contains unit tests for the operations of authorizer.
"""
import unittest
from authorizer.handler.MemoryStorage import MemoryStorage
from authorizer.handler.RateLimit import RateLimit
from datetime import datetime
from authorizer.bean.ActionBean import ActionBean
from authorizer.action.Account import Account
from authorizer.action.Transaction import Transaction
from pkg_resources import resource_stream
import logging
from logging.config import dictConfig
import yaml

dictConfig(yaml.load(resource_stream(__name__, 'logging.yaml'), Loader=yaml.FullLoader))
log = logging.getLogger('authorize')

class AuthorizerTest(unittest.TestCase):
    """Test suite for transformation in authorize.py
    """

    def setUp(self):
        """Initialize MemoryStorage & RateLimit
        """
        self.memoryStorage = MemoryStorage()
        self.rateLimit = RateLimit()
        self.log = log

    def tearDown(self):
        """Reset MemoryStorage & RateLimit
        """
        self.memoryStorage = None
        self.rateLimit = None

    def test_do_rate_limit_check(self):
        self.rateLimit.add_transaction_rate(("Habbib's", 10, datetime.strptime('2019-02-14T10:01:59.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")))
        self.rateLimit.add_transaction_rate(("McDonald's", 20, datetime.strptime('2019-02-14T10:02:09.000Z',  "%Y-%m-%dT%H:%M:%S.%fZ")))
        self.rateLimit.add_transaction_rate(("pizza's", 10, datetime.strptime('2019-02-14T10:02:10.000Z',  "%Y-%m-%dT%H:%M:%S.%fZ")))

        actual_value = self.rateLimit.do_rate_limit_check(datetime.strptime('2019-02-14T10:02:11.000Z',"%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(actual_value, False)

    def test_do_similar_transaction_check(self):
        self.rateLimit.add_transaction_rate(("Habbib's", 10, datetime.strptime('2019-02-14T10:01:59.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")))

        actual_value = self.rateLimit.do_similar_transaction_check("Habbib's", 10, datetime.strptime('2019-02-14T10:02:11.000Z', "%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(actual_value, False)

    def test_get_last_transaction(self):
        expected_obj = ActionBean(True, 100)
        self.memoryStorage.add_transaction(expected_obj)
        actual_obj = self.memoryStorage.get_last_transaction()
        self.assertEqual(actual_obj, expected_obj)

    def test_account_run_negative(self):
        expected_value = "{'account': {'active-card': True, 'available-limit': 100}, 'violations': ['account-already-initialized']}"
        actual_obj = ActionBean(True, 100)
        self.memoryStorage.add_transaction(actual_obj)
        actual_value = Account(self.log).run('{"account": {"active-card": true, "available-limit": 100}}', self.memoryStorage, self.rateLimit)
        self.assertEqual(str(actual_value), expected_value)

    def test_account_run_positive(self):
        expected_value = "{'account': {'active-card': True, 'available-limit': 100}, 'violations': []}"
        actual_obj = ActionBean(False, 100)
        self.memoryStorage.add_transaction(actual_obj)
        actual_value = Account(self.log).run('{"account": {"active-card": true, "available-limit": 100}}', self.memoryStorage, self.rateLimit)
        self.assertEqual(str(actual_value), expected_value)

    def test_transaction_run_positive(self):
        expected_value = "{'account': {'active-card': True, 'available-limit': 80}, 'violations': []}"
        actual_obj = ActionBean(True, 100)
        self.memoryStorage.add_transaction(actual_obj)
        actual_value = Transaction(self.log).run('{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}', self.memoryStorage, self.rateLimit)
        self.assertEqual(str(actual_value), expected_value)


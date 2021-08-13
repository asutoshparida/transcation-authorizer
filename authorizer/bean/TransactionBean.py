
class TransactionBean(object):
    '''
    Bean class for all transaction request
    '''

    def __init__(self, merchant, amount, time, balance_amount=0):
        self.merchant = merchant
        self.amount = amount
        self.time = time
        self.balance_amount = balance_amount

    def get_action_type(self):
        return self.action_type

    def get_merchant(self):
        return self.merchant

    def get_amount(self):
        return self.amount

    def get_time(self):
        return self.time

    def get_balance_amount(self):
        return self.balance_amount



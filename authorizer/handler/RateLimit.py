
class RateLimit(object):
    '''
    Base class for all request rate limit check.
    '''

    transaction_date_list = None

    def __init__(self):
        self.transaction_date_list = []

    def set_transaction_date_list(self, transaction_date_list):
        self.transaction_date_list = transaction_date_list

    def get_transaction_date_list(self):
        return self.transaction_date_list

    def add_transaction_rate(self, obj):
        self.transaction_date_list.append(obj)

    def do_rate_limit_check(self, transaction_date_time):
        '''
        There should not be more than 3 transactions on a 2-minute interval: high-frequency-small-interval
        :param transaction_date_time:
        :return: boolean
        '''
        latest_transaction_date_list = []
        for tr_merchant, tr_amount, tr_date in self.transaction_date_list:
            minutes_diff = (transaction_date_time - tr_date).total_seconds() / 60.0
            if minutes_diff <= 2.0:
                latest_transaction_date_list.append(tr_date)

        # print('*****do_rate_limit_check : ' + str(len(latest_transaction_date_list)))
        if len(latest_transaction_date_list) >= 3:
            return False
        else:
            return True

    def do_similar_transaction_check(self, merchant, amount, transaction_date_time):
        '''
        There should not be more than 1 similar transactions (same amount and merchant ) in a 2 minutes interval: doubled-transaction
        :param merchant:
        :param amount:
        :param transaction_date_time:
        :return: boolean
        '''
        latest_transaction_date_list = []
        for tr_merchant, tr_amount, tr_date in self.transaction_date_list:
            minutes_diff = (transaction_date_time - tr_date).total_seconds() / 60.0
            if minutes_diff <= 2.0 and tr_merchant == merchant and tr_amount == amount:
                latest_transaction_date_list.append(tr_date)

        # print('******do_similar_transaction_check : ' + str(len(latest_transaction_date_list)))
        if len(latest_transaction_date_list) >= 1:
            return False
        else:
            return True


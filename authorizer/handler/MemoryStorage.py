
class MemoryStorage(object):
    '''
    Base class for storage of all successful requests
    '''

    transaction_list = None

    def __init__(self):
        self.transaction_list = []

    def set_transaction_list(self, transaction_list):
        self.transaction_list = transaction_list

    def get_transaction_list(self):
        return self.transaction_list

    def get_last_transaction(self):
        '''
        return the last successful transaction
        :return: list
        '''

        list_size = len(self.transaction_list)
        if list_size > 0:
            return self.transaction_list[list_size - 1]
        else:
            return None

    def add_transaction(self, obj):
        '''
        add new successful transaction to transaction_list
        :param obj:
        :return:
        '''
        self.transaction_list.append(obj)





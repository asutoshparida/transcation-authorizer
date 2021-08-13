from authorizer.plugin.component import Action
from authorizer.bean.TransactionBean import TransactionBean
from authorizer.bean.ActionBean import ActionBean
from authorizer.handler.AuthorizeException import AuthorizeException, ErrorCodes
from types import SimpleNamespace
from datetime import datetime


class Transaction(Action):
    '''
    Base class for any transaction request
    '''

    def __init__(self, log):
        self.log = log
        Action.__init__(self, log)

    def run(self, json_str, memory_storage, rate_limit):
        '''
        receives the transaction request,
        persist to memory storage after a successful transaction amount, rate limit, similar transaction limit checker
        and then returns the json response.

        :param json_str:
        :param memory_storage:
        :param rate_limit:
        :return:
        '''
        transaction = self.convert_json_to_obj(json_str)
        trns_date_time = datetime.strptime(getattr(transaction.transaction, 'time'), "%Y-%m-%dT%H:%M:%S.%fZ")

        transactionBean = TransactionBean(getattr(transaction.transaction, 'merchant'),
                                     getattr(transaction.transaction, 'amount'),
                                          trns_date_time)
        return_obj = None
        if transactionBean is not None and memory_storage is not None:
            obj = memory_storage.get_last_transaction()
            return_obj = self.get_response_obj()

            if obj is None:
                '''
                No account created
                '''
                return_obj["account"] = None
                authorize_exception = AuthorizeException(ErrorCodes.ERR_SITUATION_1)
                self.log.debug("Transaction Error :", authorize_exception.message)
                return_obj["violations"] = [authorize_exception.message]

            elif obj is not None and isinstance(obj, ActionBean):
                '''
                 First Transaction with active_card: True/False check
                '''
                if obj.active_card:
                    available_limit = obj.available_limit
                    transaction_amount = transactionBean.amount
                    return_obj = self.run_transaction(available_limit, transaction_amount, transactionBean,
                                                      obj, memory_storage, return_obj)
                    rate_limit.add_transaction_rate((transactionBean.merchant, transactionBean.amount, trns_date_time))
                else:
                    return_obj["account"]["active-card"] = obj.active_card
                    return_obj["account"]["available-limit"] = obj.available_limit
                    authorize_exception = AuthorizeException(ErrorCodes.ERR_SITUATION_3)
                    self.log.debug("Transaction Error :", authorize_exception.message)
                    return_obj["violations"] = [authorize_exception.message]

            elif obj is not None and isinstance(obj, TransactionBean):
                '''
                 Consecutive Transaction with amount, rate limit, similar transaction limit check
                '''
                # call rate limit checker
                is_rate_limit_permitted = rate_limit.do_rate_limit_check(trns_date_time)
                # call similar transaction limit checker
                is_similar_transaction_permitted = rate_limit.do_similar_transaction_check(transactionBean.merchant,
                                                                        transactionBean.amount, trns_date_time)

                if is_rate_limit_permitted and is_similar_transaction_permitted:
                    available_amount = obj.balance_amount
                    transaction_amount = transactionBean.amount
                    return_obj = self.run_transaction(available_amount, transaction_amount, transactionBean,
                                                      obj, memory_storage, return_obj)
                    rate_limit.add_transaction_rate((transactionBean.merchant, transactionBean.amount, trns_date_time))
                elif not is_rate_limit_permitted:
                    return_obj["account"]["active-card"] = True
                    return_obj["account"]["available-limit"] = obj.balance_amount
                    authorize_exception = AuthorizeException(ErrorCodes.ERR_SITUATION_5)
                    self.log.debug("Transaction Error :" + str(authorize_exception.message))
                    return_obj["violations"] = [authorize_exception.message]
                elif not is_similar_transaction_permitted:
                    return_obj["account"]["active-card"] = True
                    return_obj["account"]["available-limit"] = obj.balance_amount
                    authorize_exception = AuthorizeException(ErrorCodes.ERR_SITUATION_6)
                    self.log.debug("Transaction Error :" + str(authorize_exception.message))
                    return_obj["violations"] = [authorize_exception.message]

        return return_obj

    def run_transaction(self, total_amount_available, transaction_amount, current_transaction_obj
                        , last_transaction_obj, memory_storage, return_obj):
        # IF transaction_amount > available_limit
        return_obj["account"]["active-card"] = True
        if transaction_amount > total_amount_available:
            if isinstance(last_transaction_obj, ActionBean):
                return_obj["account"]["available-limit"] = last_transaction_obj.available_limit
            elif isinstance(last_transaction_obj, TransactionBean):
                return_obj["account"]["available-limit"] = last_transaction_obj.balance_amount

            authorize_exception = AuthorizeException(ErrorCodes.ERR_SITUATION_4)
            self.log.debug("Transaction Error :" + str(authorize_exception.message))
            return_obj["violations"] = [authorize_exception.message]
        else:
            available_amount = total_amount_available - transaction_amount
            current_transaction_obj.balance_amount = available_amount
            current_transaction_obj.amount = transaction_amount
            memory_storage.add_transaction(current_transaction_obj)
            return_obj["account"]["available-limit"] = available_amount

        return return_obj

from authorizer.plugin.component import Action
from authorizer.bean.ActionBean import ActionBean
from authorizer.handler.AuthorizeException import AuthorizeException, ErrorCodes


class Account(Action):
    '''
    Base class for any card activation request
    '''

    def __init__(self, log):
        self.log = log
        Action.__init__(self, log)

    def run(self, json_str, memory_storage, rate_limit):
        '''
        receives the card activation request,
        persist to memory storage after a successful last transaction check
        and then returns the json response.

        :param json_str:
        :param memory_storage:
        :param rate_limit:
        :return: json
        '''
        account = self.convert_json_to_obj(json_str)
        action_bean = ActionBean(getattr(account.account, 'active-card'), getattr(account.account, 'available-limit'))
        return_obj = None
        if action_bean is not None and memory_storage is not None:
            obj = memory_storage.get_last_transaction()
            return_obj = self.get_response_obj()

            if obj is None:
                '''
                First card activation request
                '''
                memory_storage.add_transaction(action_bean)
                return_obj["account"]["active-card"] = action_bean.active_card
                return_obj["account"]["available-limit"] = action_bean.available_limit

            elif obj is not None and isinstance(obj, ActionBean):
                '''
                Consecutive card activation request with check for active_card: True/False
                '''
                return_obj["account"]["active-card"] = obj.active_card
                return_obj["account"]["available-limit"] = obj.available_limit
                if obj.active_card:
                    authorize_exception = AuthorizeException(ErrorCodes.ERR_SITUATION_2)
                    self.log.info("Account Error :" + str(authorize_exception.message))
                    return_obj["violations"] = [authorize_exception.message]
                else:
                    obj.active_card = True
                    return_obj["account"]["active-card"] = True

        return return_obj

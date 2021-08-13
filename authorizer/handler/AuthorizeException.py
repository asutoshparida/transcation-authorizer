import sys
from enum import Enum, unique


class AuthorizeException(Exception):
    '''
    base class for all custom Exception on Authorizer processor
    '''

    def __init__(self, error_code, message=''):
          if not isinstance(error_code, ErrorCodes):
              msg = 'Error code passed in the error_code param must be of type ErrorCodes'
              raise AuthorizeException(ErrorCodes.ERR_INCORRECT_ERRCODE, msg)

          # Storing the error code on the exception object
          self.error_code = error_code

          self.traceback = sys.exc_info()

          self.message = error_code.value

          super().__init__(self.message)


@unique
class ErrorCodes(Enum):
    '''
       Enum of Error codes for all module exceptions
       '''
    ERR_INCORRECT_ERRCODE = "Error Code Not Present"
    ERR_SITUATION_1 = "account-not-initialized"
    ERR_SITUATION_2 = "account-already-initialized"
    ERR_SITUATION_3 = "card-not-active"
    ERR_SITUATION_4 = "insufficient-limit"
    ERR_SITUATION_5 = "high-frequency-small-interval"
    ERR_SITUATION_6 = "doubled-transaction"

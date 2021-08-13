

class ActionBean(object):
    '''
    Bean class for all activate card request
    '''

    def __init__(self, active_card, available_limit, violation=[]):
        self.active_card = active_card
        self.available_limit = available_limit
        self.violation = violation

    def get_active_card(self):
        return self.active_card

    def get_available_limit(self):
        return self.available_limit

    def get_violation(self):
        return self.violation




''' Master class for payments '''

class BasePayments(object):
    ''' Base class for payments and interfacing with external subscription systems '''

    def __init__(self, user=None, config=None, rdb=None):
        ''' Initialize the Payments Class '''
        self.user = user
        self.config = config
        self.rdb = rdb

    def exists(self):
        ''' Return user upgrade status '''
        return self.user.upgraded

    def parse_form(self, request):
        ''' Parse the subscription and adjustment forms '''
        return False

    def adjust(self, request=None, quantity=None):
        ''' Base Method for adjusting an existing subscription '''
        return self.modify_subscription

    def create(self, request):
        ''' Base Method for creating a new subscription '''
        return self.create_subscription(form_data=None)

    def create_subscription(self, form_data):
        ''' Base Create Subscription Method '''
        return False

    def modify_subscription(self, form_data):
        ''' Base Subscription Modification Method '''
        return False

    def delete_subscription(self):
        ''' Base Delete Subscription Method '''
        return False

if __name__ == '__main__':  # pragma: no cover
    pass                    # pragma: no cover

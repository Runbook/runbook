''' Module to interface with Self Hosted payments '''
from .. import BasePayments

class Payments(BasePayments):
    ''' Interface with Self Hosted Payments. '''

    def adjust(self, request=None, quantity=None):
        ''' Modify an existing user subscription '''
        if request:
            form_data = self.parse_form(request)
            if form_data['type'] is "adjust":
                if form_data['quantity'] >= self.user.monitorCount:
                    result = self.modify_subscription(form_data)
                    if result:
                        self.user.subplans = form_data['quantity']
                        result = self.user.setSubscription(self.rdb)
                        return result
                    else:
                        return False
                else:
                    return False
            else:
                return False
        elif quantity:
            form_data = {'quantity' : quantity}
            result = self.modify_subscription(form_data)
            if result:
                self.user.subplans = form_data['quantity']
                result = self.user.setSubscription(self.rdb)
                return result
            else:
                return False
        else:
            return False

    def create(self, request):
        ''' Create a new user subscription '''
        form_data = self.parse_form(request)
        if self.user.monitorCount == 0:
        # Require at least one subscription
            self.user.subplans = 1
        else:
            self.user.subplans = self.user.monitorCount
        if form_data['type'] is "subscribe":
            result = self.create_subscription(form_data)
            if result:
                self.user.acttype = form_data['plan']
                set_subscription = self.user.setSubscription(self.rdb)
                if set_subscription:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def parse_form(self, request):
        ''' Parse the form used to subscribe and return a dict of processed data'''
        from generalforms import subscribe
        form = subscribe.AddPackForm(request.form)
        if request.method == "POST" and \
            "stripeToken" in request.form and "plan" in request.form:
            stripe_token = request.form['stripeToken']
            plan = request.form['plan']
            return_data = {'type': 'subscribe',
                           'stripe_token' : stripe_token,
                           'plan' : plan}
        elif request.method == "POST":
            if form.validate():
                return_data = {'type': 'adjust',
                               'quantity': int(form.add_packs.data)}
        else:
            return_data = False
        return return_data

    def create_subscription(self, form_data):
        ''' Create Subscription Method '''
        return True

    def modify_subscription(self, form_data):
        ''' Base Subscription Modification Method '''
        return True

if __name__ == '__main__':  # pragma: no cover
    pass                    # pragma: no cover

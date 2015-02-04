"""Email notification reaction."""

import mandrill
from ..utils import ShouldRun

_MANDRILL_SUCCESS_STATUSES = frozenset(['sent', 'queued', 'scheduled'])


def __action(**kwargs):
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    if ShouldRun(redata, jdata):
        to_address = redata['data']['to_address']
        subject = redata['data']['subject']
        body = redata['data']['body']
        config = kwargs['config']
        client = mandrill.Mandrill(config['mandrill_api_key'])
        message = {
            'from_email': 'noreply@runbook.io',
            'from_name': 'Runbook Notifications',
            'subject': subject,
            'text': body,
            'to': [{ 'email': to_address }],
        }
        results = client.messages.send(message=message, async=True)
        failures = []
        for result in results:
            if result['status'] not in _MANDRILL_SUCCESS_STATUSES:
                failures.append(
                    '%s - %s'
                     % (result['email'], result['reject_reason']))
        if failures:
            raise Exception(
                'Email notifications failed:\n%s' % '\n'.join(failures))
        return True


def action(**kwargs):
    try:
        return __action(**kwargs)
    except Exception, e:  #pylint: disable=broad-except
        redata = kwargs['redata']
        logger = kwargs['logger']
        logger.warning(
            'email-notification: Reaction {id} failed: {message}'.format(
                id=redata['id'], message=e.message))
        return False

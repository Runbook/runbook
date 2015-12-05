######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# API Health Check - Forms Class
######################################################################

from ..base import BaseCheckForm


class CheckForm(BaseCheckForm):

    ''' Class that creates an TCP Check form for the dashboard '''
    title = "Runbook Webhooks"
    description = """
    The Runbook Webhooks monitor allows you to integrate any service or existing health checks that perform HTTP webhook requests.
    Our webhooks work via a simple HTTP GET to a unique URL. Based on the URL called the monitor will either be "True" or "False".
    """
    webhook_include = "monitors/webhooks/general.html"

if __name__ == '__main__':
    pass

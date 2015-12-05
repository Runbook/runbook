######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Datadog Webhook Health Check - Forms Class
######################################################################

from ..base import BaseCheckForm


class CheckForm(BaseCheckForm):

    ''' Class that creates an TCP Check form for the dashboard '''
    title = "Datadog: Webhooks"
    description = """
        This monitor is designed to receive and process Datadog webhook requests. As Datadog provides unique JSON messages with webhooks this monitor will trigger a False value for errors/alerts and a True value for recovered alerts.
    """
    webhook_include = "monitors/webhooks/datadog.html"
    pass

if __name__ == '__main__':
    pass

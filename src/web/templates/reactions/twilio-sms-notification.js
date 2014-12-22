<script type="text/javascript">
  $(document).ready(function() {
    $.each([
        '#twilio-sms-notification-account_sid',
        '#twilio-sms-notification-auth_token',
        '#twilio-sms-notification-from_address',
        '#twilio-sms-notification-to_address',
        '#twilio-sms-notification-text',
      ], function(_, value) {
      $(value).popover({
        placement: 'auto bottom',
        container: 'body',
        trigger: 'click focus'
      });
    });

  });

</script>

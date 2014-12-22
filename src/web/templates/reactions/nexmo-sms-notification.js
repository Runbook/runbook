<script type="text/javascript">
  $(document).ready(function() {
    $.each([
        '#nexmo-sms-notification-api_key',
        '#nexmo-sms-notification-api_secret',
        '#nexmo-sms-notification-from_address',
        '#nexmo-sms-notification-to_address',
        '#nexmo-sms-notification-text',
      ], function(_, value) {
      $(value).popover({
        placement: 'auto bottom',
        container: 'body',
        trigger: 'click focus'
      });
    });

  });

</script>

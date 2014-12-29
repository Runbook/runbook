<script type="text/javascript">
  $(document).ready(function() {
    $.each([
        '#ssl-certificate-expiry-hostname',
        '#ssl-certificate-expiry-port',
        '#ssl-certificat-expiry-num_days'
      ], function(_, value) {
      $(value).popover({
        placement: 'auto bottom',
        container: 'body',
        trigger: 'click focus'
      });
    });

  });

</script>

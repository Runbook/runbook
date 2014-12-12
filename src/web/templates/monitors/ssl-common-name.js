<script type="text/javascript">
  $(document).ready(function() {
    $.each([
        '#ssl-common-name-host',
        '#ssl-common-name-port',
        '#ssl-common-name-expected_hostname'
      ], function(_, value) {
      $(value).popover({
        placement: 'auto bottom',
        container: 'body',
        trigger: 'click focus'
      });
    });

  });

</script>

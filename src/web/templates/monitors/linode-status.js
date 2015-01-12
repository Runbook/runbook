<script type="text/javascript">
  $(document).ready(function() {
    $.each([
        '#linode-status-apikey',
        '#linode-status-linodeid',
        '#linode-status-server-status'
      ], function(_, value) {
      $(value).popover({
        placement: 'auto bottom',
        container: 'body',
        trigger: 'click focus'
      });
    });

  });

</script>
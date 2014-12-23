<script type="text/javascript">
  $(document).ready(function() {
    $.each([
        '#cl-email',
        '#cl-snapshot'
      ], function(_, value) {
      $(value).popover({
        placement: 'auto bottom',
        container: 'body',
        trigger: 'click focus'
      });
    });

  });

</script>
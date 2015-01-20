<script type="text/javascript">
  $(document).ready(function() {
    $.each([
        '#http-http_verb',
        '#http-url',
        '#http-extra_headers',
        '#http-payload',
      ], function(_, value) {
      $(value).popover({
        placement: 'auto bottom',
        container: 'body',
        trigger: 'click focus'
      });
    });

  });

</script>

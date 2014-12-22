<script type="text/javascript">
  $(document).ready(function() {
    $.each([
        '#http-post-url',
        '#http-post-host',
        '#http-post-payload',
        '#http-post-extra_headers',
        '#http-post-response_regex',
        '#http-post-response_headers',
      ], function(_, value) {
      $(value).popover({
        placement: 'auto bottom',
        container: 'body',
        trigger: 'click focus'
      });
    });

  });

</script>

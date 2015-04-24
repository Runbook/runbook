<script type="text/javascript">
  ;(function(p,l,o,w,i){if(!p[i]){p.__asml=p.__asml||[];
  p.__asml.push(i);p[i]=function(){(p[i].q=p[i].q||[]).push(arguments)
  };p[i].q=p[i].q||[];n=l.createElement(o);g=l.getElementsByTagName(o)[0];n.async=1;
  n.src=w;g.parentNode.insertBefore(n,g)}}(window,document,"script","https://d1uxm17u44dmmr.cloudfront.net/1.0.0/asml.js","asml"));

  asml('create', 'fdc1605623bb4606f9f0c6eaa37942cfbd519389');

  {% if data['loggedin'] %}
    asml('track', '{{ data['email_digest'] }}');
  {% else %}
    asml('track');
  {% endif %}
</script>

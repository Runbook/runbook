<script type="text/javascript">
  $(document).ready(function() {
    $.each([
        '#digitalocean-new-droplet-api_key',
        '#digitalocean-new-droplet-name_prefix',
        '#digitalocean-new-droplet-region',
        '#digitalocean-new-droplet-size',
        '#digitalocean-new-droplet-image',
        '#digitalocean-new-droplet-ssh_keys',
        '#digitalocean-new-droplet-backups',
        '#digitalocean-new-droplet-ipv6',
        '#digitalocean-new-droplet-private_networking',
      ], function(_, value) {
      $(value).popover({
        placement: 'auto bottom',
        container: 'body',
        trigger: 'click focus'
      });
    });

  });

</script>

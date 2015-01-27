<script type="text/javascript">
$(document).ready(function() {
    $.each([
        '#email-notification-to_address',
        '#email-notification-subject',
        '#email-notification-body',
        ], function(_, value) {
            $(value).popover({
                placement: 'auto bottom',
                container: 'body',
                trigger: 'click focus'
            });
        });

    });

    </script>

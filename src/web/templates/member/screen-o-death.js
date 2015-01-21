<script type="text/javascript">
  $(document).ready(function() {
   $('a[data-toggle="tab"]:first').trigger("shown.bs.tab");
   $('.btn-delete-monitor').click(function(e){
       e.preventDefault();
       var monitorName = $(e.target).attr('data');
       var url = $(e.target).attr('href');
       bootbox.confirm('Are you sure you want to delete monitor '+ monitorName + '?', function(result) {
           if (result) {
               window.location.href = url;
           }
       });
   });
   $('.btn-delete-reaction').click(function(e){
       e.preventDefault();
       var reactionName = $(e.target).attr('data');
       var url = $(e.target).attr('href');
       bootbox.confirm('Are you sure you want to delete reaction ' + reactionName + '?', function(result){
           if (result) {
               window.location.href = url;
           }
       });
   });
  });
</script>
<script src="//cdnjs.cloudflare.com/ajax/libs/bootbox.js/4.3.0/bootbox.min.js"></script>

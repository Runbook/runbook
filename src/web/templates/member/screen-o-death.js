<script type="text/javascript">
  $(document).ready(function() {
   $('a[data-toggle="tab"]:first').trigger("shown.bs.tab");
   $('.btn-delete-monitor').click(function(e){
       var monitorName = $(e.target).attr('data');
       if (!window.confirm('Are you sure you want to delete monitor '+ monitorName + '?')) {
           e.preventDefault();
       }
   });
   $('.btn-delete-reaction').click(function(e){
       var reactionName = $(e.target).attr('data');
       if (!window.confirm('Are you sure you want to delete reaction ' + reactionName + '?')) {
           e.preventDefault();
       }
   });
  });
</script>

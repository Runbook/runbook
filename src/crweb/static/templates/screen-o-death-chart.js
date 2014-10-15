<script src="/static/js/c3.min.js"></script>
<script src="/static/js/d3.min.js"></script>
<script type="text/javascript">
  c3.generate({
    bindto: '#chart',
    data: {
      columns: [
        ['Healthy', {{ data['monstats']['healthy'] }}],
        ['Failed', {{ data['monstats']['failed'] }}],
        ['Other', {{ data['monstats']['unknown'] }}]
      ],
      colors: {
        'Failed': '#EC1D25',
        'Healthy': '#008cba',
        'Other': '#e99002'
      },
      type: 'donut',
    }
  });

</script>

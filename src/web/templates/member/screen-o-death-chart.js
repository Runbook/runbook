<script src="/static/js/c3.min.js"></script>
<script src="/static/js/d3.min.js"></script>
<script type="text/javascript">
  c3.generate({
    bindto: '#chart',
    data: {
      columns: [
        ['True', {{ data['monstats']['true'] }}],
        ['False', {{ data['monstats']['false'] }}],
        ['Other', {{ data['monstats']['unknown'] }}]
      ],
      colors: {
        'False': '#EC1D25',
        'True': '#008cba',
        'Other': '#e99002'
      },
      type: 'donut',
    }
  });

</script>

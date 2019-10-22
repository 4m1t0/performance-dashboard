<template>
  <DetailDashboard
    url1="shared/num-of-requests.html"
    url2="shared/num-of-errors.html"
    url3="total/distributed-dot-plot.html"
    url4="total/rps-timeline-chart.html"
    url5="total/99percentile-timeline-chart.html"
    url6="total/99percentile-degradation-timeline-chart.html"
    url7="total/98percentile-timeline-chart.html"
    url8="total/98percentile-degradation-timeline-chart.html"
    url9="total/95percentile-timeline-chart.html"
    url10="total/95percentile-degradation-timeline-chart.html"
    url11="total/90percentile-timeline-chart.html"
    url12="total/90percentile-degradation-timeline-chart.html"
    url13="total/80percentile-timeline-chart.html"
    url14="total/80percentile-degradation-timeline-chart.html"
    url15="total/75percentile-timeline-chart.html"
    url16="total/75percentile-degradation-timeline-chart.html"
    url17="total/66percentile-timeline-chart.html"
    url18="total/66percentile-degradation-timeline-chart.html"
    url19="total/50percentile-timeline-chart.html"
    url20="total/50percentile-degradation-timeline-chart.html"
    url21="total/average-timeline-chart.html"
    url22="total/average-degradation-timeline-chart.html"
    url23="total/max-timeline-chart.html"
    url24="total/max-degradation-timeline-chart.html"
    url25="total/min-timeline-chart.html"
    url26="total/min-degradation-timeline-chart.html"
  />
</template>

<script>
import DetailDashboard from '~/components/DetailDashboard'

export default {
  components: {
    DetailDashboard
  }
}
</script>

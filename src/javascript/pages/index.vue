<template>
  <div>
    <v-row>
      <Plot url="shared/num-of-requests.html" />
      <Plot url="shared/num-of-errors.html" />
    </v-row>
    <v-row>
      <Plot url="shared/99percentiles.html" />
      <Plot url="shared/rps-timeline-chart.html" />
    </v-row>
    <v-row>
      <Plot url="shared/activity-chart.html" />
    </v-row>
  </div>
</template>

<script>
import Plot from '~/components/Plot'

export default {
  components: {
    Plot
  }
}
</script>

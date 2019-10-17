<template>
  <v-layout justify-center>
    <v-flex xs12 sm12 md9 lg6 xl6>
      <v-container fluid grid-list-lg>
        <v-row no-gutters>
          <Plot url="/temp-plot.html" />
          <Plot url="/temp-plot.html" />
          <Plot url="/temp-plot.html" />
        </v-row>
        <v-row no-gutters>
          <Plot url="/temp-plot.html" />
          <Plot url="/temp-plot.html" />
        </v-row>
        <v-row no-gutters>
          <Plot url="/temp-plot.html" />
          <Plot url="/temp-plot.html" />
        </v-row>
        <v-row no-gutters>
          <Plot url="/temp-plot.html" />
          <Plot url="/temp-plot.html" />
        </v-row>
        <v-row no-gutters>
          <Plot url="/temp-plot.html" />
          <Plot url="/temp-plot.html" />
        </v-row>
        <v-row no-gutters>
          <Plot url="/temp-plot.html" />
          <Plot url="/temp-plot.html" />
        </v-row>
        <v-row no-gutters>
          <Plot url="/temp-plot.html" />
          <Plot url="/temp-plot.html" />
        </v-row>
      </v-container>
    </v-flex>
  </v-layout>
</template>

<script>
import Plot from '~/components/Plot'

export default {
  components: {
    Plot
  }
}
</script>

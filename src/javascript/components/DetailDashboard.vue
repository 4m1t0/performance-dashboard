<template>
  <div>
    <v-row>
      <Plot :url="this.url1" />
      <Plot :url="this.url2" />
    </v-row>
    <v-row>
      <Plot :url="this.url3" />
      <Plot :url="this.url4" />
    </v-row>
    <v-row>
      <Plot :url="this.url5" />
      <Plot :url="this.url6" />
    </v-row>
    <v-row>
      <Plot :url="this.url7" />
      <Plot :url="this.url8" />
    </v-row>
    <v-row>
      <Plot :url="this.url9" />
      <Plot :url="this.url10" />
    </v-row>
    <v-row>
      <Plot :url="this.url11" />
      <Plot :url="this.url12" />
    </v-row>
    <v-row>
      <Plot :url="this.url13" />
      <Plot :url="this.url14" />
    </v-row>
    <v-row>
      <Plot :url="this.url15" />
      <Plot :url="this.url16" />
    </v-row>
    <v-row>
      <Plot :url="this.url17" />
      <Plot :url="this.url18" />
    </v-row>
    <v-row>
      <Plot :url="this.url19" />
      <Plot :url="this.url20" />
    </v-row>
    <v-row>
      <Plot :url="this.url21" />
      <Plot :url="this.url22" />
    </v-row>
    <v-row>
      <Plot :url="this.url23" />
      <Plot :url="this.url24" />
    </v-row>
    <v-row>
      <Plot :url="this.url25" />
      <Plot :url="this.url26" />
    </v-row>
  </div>
</template>

<script>
import Plot from '~/components/Plot'

export default {
  props: {
    url1: String,
    url2: String,
    url3: String,
    url4: String,
    url5: String,
    url6: String,
    url7: String,
    url8: String,
    url9: String,
    url10: String,
    url11: String,
    url12: String,
    url13: String,
    url14: String,
    url15: String,
    url16: String,
    url17: String,
    url18: String,
    url19: String,
    url20: String,
    url21: String,
    url22: String,
    url23: String,
    url24: String,
    url25: String,
    url26: String
  },
  components: {
    Plot
  }
}
</script>

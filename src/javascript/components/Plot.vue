<template>
  <v-col>
    <v-card color="#1E1E38">
      <iframe
        width="100%"
        height="500"
        frameborder="0"
        seamless="seamless"
        scrolling="no"
        loading="lazy"
        :src="this.url"
      ></iframe>
    </v-card>
  </v-col>
</template>

<script>
export default {
  props: {
    url: String
  }
}
</script>

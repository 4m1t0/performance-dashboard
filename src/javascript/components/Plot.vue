<template>
  <v-col>
    <v-card color="#20203B">
      <iframe
        width="100%"
        height="500"
        frameborder="0"
        seamless="seamless"
        scrolling="no"
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

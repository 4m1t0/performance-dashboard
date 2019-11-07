<template>
  <v-app dark>
    <v-app-bar :clipped-left="clipped" fixed color="#121221" flat app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title v-text="title" />
    </v-app-bar>
    <v-navigation-drawer
      v-model="drawer"
      color="#0091EA"
      :mini-variant="miniVariant"
      :clipped="clipped"
      fixed
      temporary
      app
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          color="#FFFFFF"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-content>
      <v-container fluid>
        <nuxt />
      </v-container>
    </v-content>
    <v-footer absolute color="#121221" flat app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'mdi-apps',
          title: 'Welcome',
          to: '/'
        },
        {
          icon: 'mdi-buffer',
          title: 'Total',
          to: '/total'
        },
        {
          icon: 'mdi-api',
          title: 'GET /',
          to: '/get'
        },
        {
          icon: 'mdi-api',
          title: 'GET /login',
          to: '/get/login'
        },
        {
          icon: 'mdi-api',
          title: 'GET /my/page',
          to: '/get/my/page'
        },
        {
          icon: 'mdi-api',
          title: 'GET /projects',
          to: '/get/projects'
        },
        {
          icon: 'mdi-api',
          title: 'POST /login',
          to: '/post/login'
        },
        {
          icon: 'mdi-api',
          title: 'POST /logout',
          to: '/post/logout'
        }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'Performance Dashboard'
    }
  }
}
</script>

<style>
body {
  background: #121221;
}
.v-application {
  font-family: 'SF Pro Text', 'SF Pro Icons', 'Helvetica Neue', 'Helvetica',
    'Arial', sans-serif;
}
.theme--dark.v-application {
  background: #121221;
}
.container--fluid {
  padding-left: 12rem;
  padding-right: 12rem;
}
</style>

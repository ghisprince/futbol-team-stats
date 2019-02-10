<template>
  <v-app id="inspire" :dark="dark">
    <v-navigation-drawer
      v-show="show_drawer"
      persistent
      :mini-variant="miniVariant"
      v-model="drawer"
      fixed
      app>
      <v-list>
        <v-subheader class="mt-3 grey--text text--darken-1">Statistic by...</v-subheader>

        <v-list-tile
          value="true"
          v-for="(item, i) in items"
          :key="i"
        >
          <v-list-tile-action>
            <v-icon v-html="item.icon"></v-icon>
          </v-list-tile-action>

          <v-list-tile-content>
            <router-link :to="{ name: item.route }">{{item.title}}</router-link>
          </v-list-tile-content>
        </v-list-tile>

        <v-divider></v-divider>

        <v-subheader class="mt-3 grey--text text--darken-1">Other pages</v-subheader>

        <v-list-tile value="true">
          <v-list-tile-action>
            <v-icon>help_outline</v-icon>
          </v-list-tile-action>

          <v-list-tile-content>
            <router-link :to="{ name: 'Home' }">Help</router-link>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile value="true">
          <v-list-tile-action>
            <v-icon>close</v-icon>
          </v-list-tile-action>

          <v-list-tile-content>
              <router-link :to="{ name: 'logout' }">
              <span v-on:click="log_user_out">Logout</span>
              </router-link>
          </v-list-tile-content>
        </v-list-tile>

        <v-divider></v-divider>
        <v-list-tile>
          <v-list-tile-content>
            <v-btn small @click="dark = !dark">Toggle dark mode</v-btn>
          </v-list-tile-content>
        </v-list-tile>

      </v-list>

    </v-navigation-drawer>
    <v-toolbar app>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-toolbar-title v-text="title"></v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-content>
      <router-view/> <!-- this all the content -->
    </v-content>
    <!--
    <v-footer :fixed="fixed" app dark>
      <v-spacer></v-spacer>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
    -->
  </v-app>
</template>

<script>
import API from '@/lib/API'

export default {
  name: 'App',
  data () {
    return {
      drawer: false,
      dark: true,
      fixed: true,
      miniVariant: false,
      right: true,
      title: 'Futbol Stats',
      items: [
        {icon: 'view_list', title: 'Competition', route: 'Competitions'},
        {icon: 'view_list', title: 'Opponent', route: 'Opponents'},
        {icon: 'view_list', title: 'Players', route: 'Players'}
      ],
      items2: [
        {icon: 'help_outline', title: 'Help', route: 'Home'},
        {icon: 'close', title: 'Log out', route: 'logout'}
      ]
    }
  },
  computed: {
    /*
    state () {
      return this.$store.state
    }, */
    show_drawer: function () {
      return this.$route.name !== 'login' && this.$route.name !== 'logout'
    }
  },
  methods: {
    log_user_out () {
      API.logout()
      this.$store.dispatch('clearCurrentUser')
    }
  },
  created () {
    this.$store.dispatch('init')
  }
}
</script>

<template>
  <v-app dark>
    <v-navigation-drawer
      persistent
      :mini-variant="miniVariant"
      v-model="drawer"
      fixed
      app>
      <v-list>
        <v-subheader class="mt-3 grey--text text--darken-1">View stats by...</v-subheader>

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
      </v-list>
    </v-navigation-drawer>
    <v-toolbar app>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-toolbar-title v-text="title"></v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-content>
      <router-view/>
    </v-content>
    <v-footer :fixed="fixed" app>
      <span>&copy; 2018</span>
    </v-footer>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data () {
    return {
      drawer: false,
      fixed: true,
      miniVariant: false,
      right: true,
      title: 'Pats B04 Futbol stats',
      items: [
        { icon: 'view_list', title: 'Competition', route: 'Competitions' },
        { icon: 'view_list', title: 'Opponent', route: 'Opponents' },
        { icon: 'view_list', title: 'Players', route: 'Players' }
      ]
    }
  }
}
</script>

<template id="player-list">
  <v-card>
    <v-container>
      <v-card>
        <v-layout align-start justify-end fill-height>
          <v-btn v-if="is_editor"
                 color="success"
                 :to="{ name: 'PlayerCreate' }">
            New Player
          </v-btn>
        </v-layout>

        <v-card-title>
          <h2>Players</h2>
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="search"
            label="Search"
            single-line
          ></v-text-field>
        </v-card-title>

        <v-data-table
          :headers="headers"
          :items="players"
          :search="search"
          :pagination.sync="pagination"
        >
          <template slot="headerCell" slot-scope="props">
            <v-tooltip bottom>
              <span slot="activator">
                {{ props.header.text }}
              </span>
              <span>
                {{ props.header.tooltip ? props.header.tooltip : props.header.text  }}
              </span>
            </v-tooltip>
          </template>

          <template slot="items" slot-scope="props">
            <td>{{ props.item.label }}</td>
            <td><v-icon v-show="props.item.active">done</v-icon></td>
            <td>{{ props.item.num_apps }}</td>
            <td>
              <router-link :to="{
                  name: 'Player',
                  params: { id: props.item.id }
                }">
                <v-icon>insert_chart</v-icon>
              </router-link>
            </td>
          </template>
          <v-alert slot="no-results" :value="true" color="error" icon="warning">
            Your search for "{{ search }}" found no results.
          </v-alert>
        </v-data-table>
      </v-card>
    </v-container>
  </v-card>
</template>

<script>
export default {
  data () {
    return {
      pagination: {},
      search: '',
      headers: [
        {text: 'Name', value: 'label'},
        {text: 'Active', value: 'active'},
        {text: 'Apps', tooltip: 'Number of Matches participated in', value: 'num_apps'},
        {text: 'Details', value: 'id'}
      ]
    }
  },
  computed: {
    is_editor () {
      return this.$store.state.user.is_editor
    },
    players () {
      return this.$store.state.players
    }
  }
}
</script>

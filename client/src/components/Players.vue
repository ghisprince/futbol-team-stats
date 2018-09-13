<template id="player-list">
  <div>
    <v-card>
      <v-layout align-start justify-end fill-height>
        <v-btn color="success"
              :to="{ name: 'PlayerCreate' }">
          NEW PLAYER
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
        <template slot="items" slot-scope="props">
          <td>{{ props.item.label }}</td>
          <td>{{ props.item.active }}</td>
          <td>{{ props.item.num_apps }}</td>
          <td>
            <router-link :to="{
                name: 'Player',
                params: { id: props.item.id }
              }">
              Stats
            </router-link>
          </td>
        </template>
        <v-alert slot="no-results" :value="true" color="error" icon="warning">
          Your search for "{{ search }}" found no results.
        </v-alert>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import API from '@/lib/API'

export default {
  data () {
    return {
      players: [],
      pagination: {
        
      },
      search: '',
      headers: [
        {text: 'Name', value: 'label'},
        {text: 'Active', value: 'active'},
        {text: 'Apps', value: 'num_apps'},
        {text: 'Stats', value: 'id'}
      ]
    }
  },
  mounted () {
    this.load()
  },
  methods: {
    load () {
      API.getPlayers()
        .then(players => {
          this.players = players
        })
    }
  }
}
</script>

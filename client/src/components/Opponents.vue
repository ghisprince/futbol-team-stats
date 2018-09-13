<template id="opponent-list">
  <div>
    <v-card>
      <v-layout align-start justify-end fill-height>
        <v-btn color="success"
              :to="{name: 'OpponentCreate'}">
          NEW Opponent
        </v-btn>
      </v-layout>

      <v-card-title>
        <h2>Opponentsz</h2>
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
        :items="opponents"
        :search="search"
      >
        <template slot="items" slot-scope="props">
          <td>{{ props.item.name }}</td>
          <td class="text-xs">{{ props.item.match_results }}</td>
          <td class="text-xs">
              <router-link :to="{
                name: 'Opponent',
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
      opponents: [],
      search: '',
      headers: [
        {text: 'Name', value: 'name'},
        {text: 'W-D-L', value: 'match_results'},
        {text: 'Stats', value: 'id'}
      ]
    }
  },
  mounted () {
    this.load()
  },
  methods: {
    load () {
      API.getOpponents()
        .then(opponents => {
          this.opponents = opponents
        })
    }
  }
}
</script>

<template id="opponent-list">
  <v-card>
    <v-container>
      <v-card>
        <v-layout align-start justify-end fill-height>
          <v-btn v-if="canEdit"
                 color="success"
                 :to="{name: 'OpponentCreate'}">
            New Opponent
          </v-btn>
        </v-layout>

        <v-card-title>
          <h2>Opponents</h2>
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
            <td>{{ props.item.match_results }}</td>
            <td><span v-show="props.item.goal_differential > 0">+</span>{{ props.item.goal_differential}}</td>
            <td>
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
    </v-container>
  </v-card>
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
        {text: 'Goal Diff', value: 'goal_differential'},
        {text: 'Stats', value: 'id'}
      ]
    }
  },
  computed: {
    canEdit () {
      return this.$store.state.canEdit
    }
  },
  mounted () {
    this.load()
  },
  methods: {
    load () {
      // TODO: possibly move this to store?
      API.getOpponents()
        .then(opponents => {
          this.opponents = opponents
        })
    }
  }
}
</script>

<template id="competition-list">
  <div>
    <v-card>
      <v-layout align-start justify-end fill-height>
        <v-btn v-if="canEdit"
               color="success"
               :to="{name: 'CompetitionCreate'}">
          NEW COMPETITION
        </v-btn>
      </v-layout>

      <v-card-title>
        <h2>Competitions</h2>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="search"
          label="Search"
          single-line>
        </v-text-field>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="competitions"
        :search="search"
        :pagination.sync="pagination">

        <template slot="items" slot-scope="props">
          <td>{{ props.item.name }}</td>
          <td>{{ props.item.start_date }}</td>
          <td>{{ props.item.num_match }}</td>
          <td>{{ props.item.match_results }}</td>
          <td>{{ props.item.result }}</td>
          <td><span v-show="props.item.goal_differential > 0">+</span>{{ props.item.goal_differential}}</td>
          <td>{{ props.item.clean_sheets }}</td>
          <td>
              <router-link :to="{
                name: 'Competition',
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
  </div>
</template>

<script>
import API from '@/lib/API'

export default {
  data () {
    return {
      competitions: [],
      pagination: {
        sortBy: 'start_date',
        descending: true
      },
      search: '',
      headers: [
        {text: 'Name', value: 'name', sortable: false},
        {text: 'Start', value: 'start_date'},
        {text: '# Match', value: 'num_match'},
        {text: 'W-D-L', value: 'match_results'},
        {text: 'Result', value: 'result'},
        {text: 'Goal Diff', value: 'goal_differential'},
        {text: 'Clean Sheets', value: 'clean_sheets'},
        {text: 'Details', value: 'id'}
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
      API.getCompetitions()
        .then(competitions => {
          this.competitions = competitions
        })
    }
  }
}
</script>

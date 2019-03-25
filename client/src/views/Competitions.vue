<template id="competition-list">
  <v-card>
    <v-container>
      <v-card>
        <v-layout align-start justify-end fill-height>
          <v-btn v-if="is_editor"
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
            <td>{{ props.item.name }}</td>
            <td>{{ props.item.start_date }}</td>
            <td>{{ props.item.level }}</td>
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
    </v-container>
  </v-card>
</template>

<script>
export default {
  data () {
    return {
      pagination: {
        sortBy: 'start_date',
        descending: true
      },
      search: '',
      headers: [
        {text: 'Name', value: 'name', sortable: false},
        {text: 'Start', tooltip: 'Start Date', value: 'start_date'},
        {text: 'Level', tooltip: 'Tournament level', value: 'level'},
        {text: 'Matches', tooltip: 'Number of Matches', value: 'num_match'},
        {text: 'W-D-L', tooltip: 'Number of Win-Draw-Loss', value: 'match_results'},
        {text: 'Result', value: 'result'},
        {text: 'Goal Diff', tooltip: 'Goal Differential (Goals scored-Goals allowed)', value: 'goal_differential'},
        {text: 'Clean Sheets', value: 'clean_sheets'},
        {text: 'Details', value: 'id'}
      ]
    }
  },
  computed: {
    is_editor () {
      return this.$store.state.user.is_editor
    },
    competitions () {
      return this.$store.state.competitions
    }
  }
}
</script>

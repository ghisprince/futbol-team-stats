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
            <td>{{ props.item.num_match }}</td>
            <td>{{ props.item.match_results }}</td>
            <td><span v-show="props.item.goal_differential > 0">+</span>{{ props.item.goal_differential}}</td>
            <td>
                <router-link :to="{
                  name: 'Opponent',
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
      search: '',
      headers: [
        {text: 'Name', value: 'name'},
        {text: 'Matches', tooltip: 'Number of Matches', value: 'num_match'},
        {text: 'W-D-L', tooltip: 'Number of Wins-Draws-Losses', value: 'match_results'},
        {text: 'Goal Diff', tooltip: 'Goal Differential (Goals scored-Goals allowed)', value: 'goal_differential'},
        {text: 'Details', value: 'id'}
      ]
    }
  },
  computed: {
    canEdit () {
      return this.$store.state.authUser.canEdit
    },
    opponents () {
      return this.$store.getters.opponentsSorted
    }
  }
}
</script>

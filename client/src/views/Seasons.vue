<template id="season-list">
  <v-card>
    <v-container>
      <v-card>
        <v-layout align-start justify-end fill-height>
          <v-btn v-if="is_editor"
                color="success"
                :to="{name: 'SeasonCreate'}">
            NEW SEASON
          </v-btn>
        </v-layout>

        <v-card-title>
          <h2>Seasons</h2>
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
          :items="seasons"
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
            <td>{{ props.item.num_matches }}</td>
            <td>{{ props.item.match_results }}</td>
            <td>
                <router-link :to="{
                  name: 'Season',
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
        { text: 'Name', value: 'name', sortable: false },
        { text: 'Start', tooltip: 'Start Date', value: 'start_date' },
        { text: 'Matches', tooltip: 'Number of Matches', value: 'num_matches' },
        { text: 'W-D-L', tooltip: 'Number of Win-Draw-Loss', value: 'match_results' },
        { text: 'Details', value: 'id' }
      ]
    }
  },
  computed: {
    is_editor () {
      return this.$store.state.user.is_editor
    },
    seasons () {
      return this.$store.state.seasons
    }
  }
}
</script>

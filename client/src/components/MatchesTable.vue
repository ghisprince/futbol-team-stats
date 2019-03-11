<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="matches"
      :search="search"
      :pagination.sync="pagination"
      :loading="true"
    >
      <v-progress-linear v-show="showProgress"
                         slot="progress"
                         color="blue"
                         indeterminate>
      </v-progress-linear>

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

        <td>{{ props.item.date_time | formatDate  }}</td>

        <td v-if="showOpponent">
            <router-link :to="{
              name: 'Opponent',
              params: { id: props.item.opponent }
            }">
            {{ props.item.opponent_name }}
          </router-link>
        </td>

        <td v-if="showCompetition">
            <router-link :to="{
              name: 'Competition',
              params: { id: props.item.competition }
            }">
            {{ props.item.competition_name }}
          </router-link>
        </td>

        <td>
          <span v-show="props.item.result === 'win'" style="color:limegreen">{{ props.item.result }}</span>
          <span v-show="props.item.result === 'loss'" style="color:#ff4000">{{ props.item.result }}</span>
          <span v-show="props.item.result === 'tie'" style="color:darkgrey">{{ props.item.result }}</span>
        </td>

        <td>{{ props.item.score }}</td>
        <td>{{ props.item.num_shots }}-{{props.item.num_shots_against}}</td>
        <td>
          <router-link :to="{
              name: 'Match',
              params: { id: props.item.id }
            }">
            <v-icon>insert_chart</v-icon>
          </router-link></td>

      </template>
    </v-data-table>
  </div>
</template>

<script>
export default {
  props: ['matches', 'showOpponent', 'showCompetition', 'showProgress'],
  data () {
    return {
      win_color: 'blue',
      pagination: {
        sortBy: 'date_time',
        descending: true
      },
      search: '',
      headersAll: [
        {text: 'Date', value: 'date_time', tooltip: 'Date & time of match', width: '1%'},
        {text: 'Competition', value: 'competition_name', tooltip: 'Name of competition', width: '1%'},
        {text: 'Opponent', value: 'opponent_name', tooltip: 'Opponent name', width: '1%'},
        {text: 'Result', value: 'result', width: '1%'},
        {text: 'Score', value: 'score', tooltip: 'Goals for-Goals against', width: '1%'},
        {text: 'Shots', value: 'num_shots', tooltip: 'Shots for-Shots against', width: '1%'},
        {text: 'Match Details', value: 'match', tooltip: 'Further Match Details', width: '1%'}
      ]
    }
  },
  methods: {
  },
  computed: {
    headers: function () {
      let h = this.headersAll
      if (!this.showCompetition) {
        h = h.filter(header => header.value !== 'competition_name')
      }
      if (!this.showOpponent) {
        h = h.filter(header => header.value !== 'opponent_name')
      }
      return h
    }
  }
}
</script>

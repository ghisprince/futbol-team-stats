<template>
  <div>
      <v-data-table
        :headers="headers"
        :items="matches"
        :search="search"
        :pagination.sync="pagination"
      >
        <template slot="items" slot-scope="props">

          <td>{{ props.item.date_time }}</td>

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
          <td>{{ props.item.result }}</td>
          <td>{{ props.item.score }}</td>
          <td>
            <router-link :to="{
                name: 'Match',
                params: { id: props.item.id }
              }">
              Details
            </router-link></td>

        </template>
      </v-data-table>

  </div>
</template>

<script>
export default {
  props: ['matches', 'showOpponent', 'showCompetition'],
  data () {
    return {
      pagination: {
        sortBy: 'date_time',
        descending: true
      },
      search: '',
      headersAll: [
        {text: 'Date', value: 'date_time'},
        {text: 'Competition', value: 'competition_name'},
        {text: 'Opponent', value: 'opponent_name'},
        {text: 'Result', value: 'result'},
        {text: 'Score', value: 'score'},
        {text: 'Match Details', value: 'match'}
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

<template>
  <v-container fluid>

    <v-card offset-sm3>
      <v-alert
        v-model="alert"
        dismissible
        color="warning"
        icon="priority_high"
      >
        {{ alertMessage }}
      </v-alert>
      <v-card-title>
        <h2>{{ player.label }}</h2>

        <v-spacer></v-spacer>
        <v-btn
          :to="{
            name: 'PlayerEdit',
            params: {
                id: player.id
            }
          }"
          color="primary">Edit</v-btn>
        <v-btn @click="deletePlayer()" color="error">Delete</v-btn>

      </v-card-title>
      <div>
        <h2>Aggregated by Competition</h2>
        <player-matches-agg-table :player_matches="player_matches" :showPlayer="false" :showCompetition="true"></player-matches-agg-table>

        <h2>Individual Matches</h2>
        <player-matches-table :player_matches="player_matches" :showPlayer="false" :showMatch="true"></player-matches-table>
      </div>
    </v-card>
  </v-container>
</template>

<script>
import API from '@/lib/API'
import PlayerMatchesTable from '@/components/PlayerMatchesTable'
import PlayerMatchesAggTable from '@/components/PlayerMatchesAggTable'

export default {
  components: {
    PlayerMatchesTable, PlayerMatchesAggTable
  },
  data () {
    return {
      alert: false,
      alertMessage: '',
      player: {
        id: -1,
        label: null
      },
      player_matches: []
    }
  },
  mounted () {
    const { id } = this.$route.params
    this.load(id)
  },
  methods: {
    load (id) {
      API.getPlayer(id)
        .then((player) => {
          this.player = player
        })
      API.getPlayerMatchesByPlayerEx(id)
        .then((player_matches) => {
          this.player_matches = player_matches
        })
    },
    deletePlayer () {
      API.deletePlayer(this.player.id)
        .then(() => {
          this.$router.push({
            name: 'Players'
          })
        })
        .catch((err) => {
          this.alert = true
          this.alertMessage = err.response.data.error
        })
    }
  }
}
</script>

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
        <h2>{{ opponent.name }}</h2>

        <v-spacer></v-spacer>
        <v-btn
          :to="{
            name: 'OpponentEdit',
            params: {
                id: opponent.id
            }
          }"
          color="primary">Edit</v-btn>
        <v-btn @click="deleteOpponent()" color="error">Delete</v-btn>

      </v-card-title>
        <div>

        Match Results (W-D-L): {{ opponent.match_results }} <br/>

        <div v-if="opponent.note">
          Note: {{ opponent.note }}
        </div>
        <div v-if="opponent.external_url">
            <a v-bind:href="opponent.external_url">Opponent's web site</a>
        </div>

        <matches-table :matches="matches" :showCompetition="true"></matches-table>

        <h2>Player stats vs this opponent</h2>
        <player-matches-agg-table :player_matches="player_matches" :showPlayer="true"></player-matches-agg-table>

        </div>
    </v-card>
  </v-container>
</template>

<script>
import API from '@/lib/API'
import MatchesTable from '@/components/MatchesTable'
import PlayerMatchesAggTable from '@/components/PlayerMatchesAggTable'

export default {
  components: {
    MatchesTable, PlayerMatchesAggTable
  },
  data () {
    return {
      alert: false,
      alertMessage: '',
      opponent: {
        id: -1,
        name: null
      },
      matches: [],
      player_matches: []
    }
  },
  mounted () {
    const { id } = this.$route.params
    this.load(id)
  },
  methods: {
    load (id) {
      API.getOpponent(id)
        .then((opponent) => {
          this.opponent = opponent
        })
      API.getMatchesByOpponent(id)
        .then((matches) => {
          this.matches = matches
        })
      API.getPlayerMatchesByOpponent(id)
        .then((player_matches) => {
          this.player_matches = player_matches
        })
    },
    deleteOpponent () {
      API.deleteOpponent(this.opponent.id)
        .then(() => {
          this.$router.push({
            name: 'Opponents'
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

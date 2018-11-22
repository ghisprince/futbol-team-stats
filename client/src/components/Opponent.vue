<template>
  <v-card>
    <v-container>
      <v-card offset-sm3>
        <v-alert
          v-model="alert"
          dismissible
          color="warning"
          icon="priority_high">
          {{ alertMessage }}
        </v-alert>
        <v-card-title>
          <h2>{{ opponent.name }}</h2>

          <v-spacer></v-spacer>
          <div v-if="canEdit">
            <v-btn
              :to="{
                name: 'OpponentEdit',
                params: {
                    id: opponent.id
                }
              }"
              color="primary">Edit</v-btn>
            <v-btn @click="deleteOpponent()" color="error">Delete</v-btn>
          </div>
        </v-card-title>

        <v-card-text>

          Match Results (W-D-L): {{ opponent.match_results }} <br/>

          <div v-if="opponent.note">
            Note: {{ opponent.note }}
          </div>
          <div v-if="opponent.external_url">
              <a v-bind:href="opponent.external_url">Web site</a>
          </div>
        <matches-table :matches="matches" :showCompetition="true"></matches-table>
        </v-card-text>

      </v-card>
    </v-container>
    <v-container>
      <v-card>
        <v-card-title>
          <h2>Player stats vs this opponent</h2>
        </v-card-title>

        <v-card-text>
          <player-matches-agg-table :player_matches="player_matches" :showPlayer="true"></player-matches-agg-table>
        </v-card-text>
      </v-card>
    </v-container>
  </v-card>
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
  computed: {
    canEdit () {
      return this.$store.state.authUser.canEdit
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
        .catch((err) => {
          if (err.response.status === 401) {
            this.$router.push({name: 'login'})
          }
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
      this.$store.dispatch('deleteOpponent', this.opponent.id)
      .then(response => {
        console.log('deleteOpponent success')
      }, error => {
        console.log('deleteOpponent error')
        this.alert = true
        this.alertMessage = error.response.data.error
      })
    }
  }
}
</script>

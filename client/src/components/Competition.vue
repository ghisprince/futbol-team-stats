<template>
  <v-card>
    <v-container>
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
          <h2>{{ competition.name }}</h2>

          <v-spacer></v-spacer>
          <div v-if="canEdit">
            <v-btn
              :to="{
                name: 'CompetitionEdit',
                params: {
                    id: competition.id
                }
              }"
              color="primary">Edit</v-btn>
            <v-btn @click="deleteCompetition()" color="error">Delete</v-btn>
          </div>
        </v-card-title>
        <v-card-text>
          Match Results (W-D-L): {{ competition.match_results }} <br/>

          <div v-if="competition.result">
            Results : {{ competition.result }}
          </div>

          <div v-if="competition.note">
            Note: {{ competition.note }}
          </div>

          <div v-if="competition.external_url">
              <a v-bind:href="competition.external_url">Web site</a>
          </div>

        </v-card-text>
      </v-card>
    </v-container>
    <v-container>
        <v-card>
          <v-card-title>
            <h2>Matches</h2>
            <v-spacer></v-spacer>
            <v-btn v-if="canEdit"
                   color="success"
                   :to="{name: 'MatchCreate'}">
              ADD MATCH
            </v-btn>
          </v-card-title>
          <v-card-text>
            <matches-table :matches="matches" :showOpponent="true"></matches-table>
          </v-card-text>
        </v-card>
    </v-container>
    <v-container>
      <v-card>
        <v-card-title>
          <h2>Player stats</h2>
        </v-card-title>

        <v-card-text>
          <player-matches-agg-table :player_matches="player_matches" :showPlayer="true"></player-matches-agg-table>
        </v-card-text>
      </v-card>
    </v-container>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
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
      competition: {
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
  computed: {
    canEdit () {
      return this.$store.state.canEdit
    }
  },
  methods: {
    load (id) {
      API.getCompetition(id)
        .then((competition) => {
          this.competition = competition
        })
      API.getMatchesByCompetition(id)
        .then((matches) => {
          this.matches = matches
        })
      API.getPlayerMatchesByCompetition(id)
        .then((player_matches) => {
          this.player_matches = player_matches
        })
    },
    deleteCompetition () {
      API.deleteCompetition(this.competition.id)
        .then(() => {
          this.$router.push({
            name: 'Competitions'
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

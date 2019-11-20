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
          <h2>{{ competition.name }}</h2>

          <v-spacer></v-spacer>
          <div v-if="is_editor">
            <v-btn
              :to="{
                name: 'CompetitionEdit',
                params: {
                    id: competition.id
                }
              }"
              color="primary">Edit</v-btn>
            <v-btn @click="deleteCompetition()" color="error">
              Delete
            </v-btn>
          </div>
        </v-card-title>
        <v-card-text>
          <strong> Match Results (W-D-L) : </strong>
          {{ competition.match_results }}

          <div v-if="competition.season">
            <strong> Season : </strong> {{ competition.season_name }}
          </div>

          <div v-if="competition.result">
            <strong> Result : </strong> {{ competition.result }}
          </div>

          <div v-if="competition.note">
            <strong> Note : </strong> {{ competition.note }}
          </div>

          <div v-if="competition.external_url">
              <strong>Web site : </strong>
              <a v-bind:href="competition.external_url" target="_blank">
                {{ competition.external_url | getHostName}}
              </a>
          </div>
        </v-card-text>
      </v-card>
    </v-container>
    <v-container>
        <v-card>
          <v-card-title>
            <h2>Matches</h2>
            <v-spacer></v-spacer>
            <v-btn v-if="is_editor"
                   color="success"
                   :to="{name: 'MatchCreate'}">
              ADD MATCH
            </v-btn>
          </v-card-title>
          <v-card-text>
            <matches-table :matches="matches"
                           :showOpponent="true"
                           :showProgress="showProgress">
            </matches-table>
          </v-card-text>
        </v-card>
    </v-container>
    <v-container>
      <v-card>
        <v-card-title>
          <h2>Player stats</h2>
        </v-card-title>

        <v-card-text>
          <player-matches-agg-table :player_matches="player_matches"
                                    :showPlayer="true"
                                    :showProgress="showProgress2">
          </player-matches-agg-table>
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
      competition: {
        id: -1,
        name: null
      },
      matches: [],
      player_matches: [],
      showProgress: true,
      showProgress2: true
    }
  },
  mounted () {
    const { id } = this.$route.params
    this.load(id)
  },
  computed: {
    is_editor () {
      return this.$store.state.user.is_editor
    }
  },
  methods: {
    load (id) {
      API.getCompetition(id)
        .then((competition) => {
          this.competition = competition
        })
        .catch((err) => {
          if (err.response.status === 401) {
            this.$router.push({ name: 'login' })
          }
        })
      API.getMatchesByCompetition(id)
        .then((matches) => {
          this.matches = matches
          this.showProgress = false
        })
      API.getPlayerMatchesByCompetition(id)
        .then((player_matches) => {
          this.player_matches = player_matches
          this.showProgress2 = false
        })
    },
    deleteCompetition () {
      this.$store.dispatch('deleteCompetition', this.competition.id)
        .then(response => {
          console.log('deleteCompetition success')
        }, error => {
          console.log('deleteCompetition error')
          this.alert = true
          this.alertMessage = error.response.data.error
        })
    }
  }
}
</script>

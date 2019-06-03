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
          <div v-if="is_editor">
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

          <strong>Match Results (W-D-L) : </strong> {{ opponent.match_results }} <br/>

          <div v-if="opponent.note">
            <strong>Note : </strong> {{ opponent.note }}
          </div>

          <div v-if="opponent.external_url">
              <strong> Web site : </strong>
              <a v-bind:href="opponent.external_url" target="_blank">
                external link
              </a>
          </div>

          <matches-table :matches="matches"
                         :showCompetition="true"
                         :showProgress="showProgress">
          </matches-table>
        </v-card-text>

      </v-card>
    </v-container>
    <v-container>
      <v-card>
        <v-card-title>
          <h2>Player stats vs this opponent</h2>
        </v-card-title>

        <v-card-text>
          <player-matches-agg-table :player_matches="player_matches"
                                    :showPlayer="true"
                                    :showProgress="showProgress">
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
      opponent: {
        id: -1,
        name: null
      },
      matches: [],
      player_matches: [],
      showProgress: true
    }
  },
  computed: {
    is_editor () {
      return this.$store.state.user.is_editor
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
            this.$router.push({ name: 'login' })
          }
        })
      API.getMatchesByOpponent(id)
        .then((matches) => {
          this.matches = matches
          this.showProgress = false
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
          this.alert = true
          this.alertMessage = error.response.data.error
        })
    }
  }
}
</script>

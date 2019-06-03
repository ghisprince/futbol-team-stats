<template>
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
      <h1>{{ player.label }}</h1>
      <v-spacer></v-spacer>

      <div v-if="is_editor">
        <v-btn
          :to="{
            name: 'PlayerEdit',
            params: {
                id: player.id
            }
          }"
          color="primary">Edit</v-btn>
        <v-btn @click="deletePlayer()" color="error">Delete</v-btn>
      </div>

    </v-card-title>
    <v-container>
      <v-card>
      <v-card-text>
        <h3>Aggregated by Competition</h3>
        <player-matches-agg-table :player_matches="player_matches"
                                  :showPlayer="false"
                                  :showCompetition="true"
                                  :showProgress="showProgress"
                                  >
        </player-matches-agg-table>
      </v-card-text>
      </v-card>
    </v-container>
    <v-container>
      <v-card>
        <v-card-text>
        <h3>Individual Matches</h3>
        <player-matches-table :player_matches="player_matches"
                              :showPlayer="false"
                              :showMatch="true"
                              :showProgress="showProgress">
        </player-matches-table>
      </v-card-text>
      </v-card>
    </v-container>
  </v-card>
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
      API.getPlayer(id)
        .then((player) => {
          this.player = player
        })
        .catch((err) => {
          if (err.response.status === 401) {
            this.$router.push({ name: 'login' })
          }
        })
      API.getPlayerMatchesByPlayerEx(id)
        .then((player_matches) => {
          this.player_matches = player_matches
          this.showProgress = false
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

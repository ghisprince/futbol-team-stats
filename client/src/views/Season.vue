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
          <h2>{{ season.name }} season</h2>

          <v-spacer></v-spacer>
          <div v-if="is_editor">
            <v-btn
              :to="{
                name: 'SeasonEdit',
                params: {
                    id: season.id
                }
              }"
              color="primary">Edit</v-btn>
            <v-btn @click="deleteSeason()" color="error">
              Delete
            </v-btn>
          </div>
        </v-card-title>
        <v-card-text>
          <strong> Number of Matches : </strong>
          {{ season.num_matches }} <br/>

          <strong> Match Results (W-D-L) : </strong>
          {{ season.match_results }} <br/>

          <div v-if="season.note">
            <strong> Note : </strong> {{ season.note }}
          </div>

        </v-card-text>
      </v-card>
    </v-container>
    <v-container>
      <v-card>
        <v-card-title>
          <h2>Competitions</h2>
        </v-card-title>
        <v-card-text>

          <competitions-table :competitions="competitions"
                              :search="null"
                              :showProgress="showProgress"
          ></competitions-table>

        </v-card-text>
      </v-card>
    </v-container>
    <v-container>
      <v-card>
        <v-card-title>
          <h2>Player season stats</h2>
        </v-card-title>

        <v-card-text>
          <h3>Aggregated by Season</h3>
          <player-seasons-agg-table :agg_player_matches="player_season_data"
                                    :showPlayer="true"
                                    :showSeason="false"
                                    :showProgress="showProgress2"
                                    >
          </player-seasons-agg-table>
        </v-card-text>
      </v-card>
    </v-container>
  </v-card>
</template>

<script>
import API from '@/lib/API'
import CompetitionsTable from '@/components/CompetitionsTable'
import PlayerSeasonsAggTable from '@/components/PlayerSeasonsAggTable'

export default {
  components: {
    CompetitionsTable, PlayerSeasonsAggTable
  },
  data () {
    return {
      alert: false,
      alertMessage: '',
      season: {
        id: -1,
        name: '',
        note: ''
      },
      matches: [],
      player_season_data: [],
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
    },
    competitions () {
      return this.$store.state.competitions.filter(
        competition => competition.season === this.season.id)
    }
  },
  methods: {
    load (id) {
      API.getSeason(id)
        .then((season) => {
          this.season = season
        })
        .catch((err) => {
          if (err.response.status === 401) {
            this.$router.push({ name: 'login' })
          }
        })
      API.getTeamSeasonData(id)
        .then((player_season_data) => {
          this.player_season_data = player_season_data
          this.showProgress2 = false
        })
    },
    deleteSeason () {
      this.$store.dispatch('deleteSeason', this.season.id)
        .then(response => {
          console.log('deleteSeason success')
        }, error => {
          console.log('deleteSeason error')
          this.alert = true
          this.alertMessage = error.response.data.error
        })
    }
  }
}
</script>

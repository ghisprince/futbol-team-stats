<template id="competition">
    <div>
        <h2>{{ competition.name }}</h2>

        <div v-if="competition.external_url">
            <a v-bind:href="competition.external_url">Competition's web site</a>
        </div>
        <h3>Team record: {{competition.match_results}}</h3>

        <div v-show="competition.note" align="left">
            Note: {{competition.note}}
        </div>

        <match-table v-bind:matches="competition.matches" v-bind:showCompetition=false> </match-table>

        <agg-player-match-table v-bind:player_matches="player_matches"> </agg-player-match-table>

        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/competition-list'">Back to competition list</router-link>
    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'
import MatchTable from '../MatchTable.vue'
import AggPlayerMatchTable from '../player_match/AggPlayerMatchTable.vue'

export default {
    data () {
        return {competition: {name: ''},
                player_matches: [],
                matches: []}
    },
    components: {
        'match-table': MatchTable,
        'agg-player-match-table': AggPlayerMatchTable
    },
    created() {
        // get competition data
        axios.get(`/api/v1/competitions/` + this.$route.params.competition_id + `?expand=true`)
        .then(response => {
            this.competition = response.data;
        })

        // get all player matches for AggPlayerMatchTable
        axios.get(`/api/v1/playermatches/?competition_id=` + this.$route.params.competition_id + `&expand=true`)
        .then(response => {
            this.player_matches = _.orderBy(response.data, "player.name");
        })
    },
    computed: {
    }
}

</script>

<style>
</style>
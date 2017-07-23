<template id="competition">
    <div>
        <h2>{{ competition.name }}</h2>

        <div v-if="competition.external_url">
            <a v-bind:href="competition.external_url">Competition's web site</a>
        </div>
        <h3>Team's record in this competition: {{competition.match_results}}</h3>

        <match-table v-bind:matches="competition.matches" v-bind:showCompetition=false> </match-table>

        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/competition-list'">Back to competition list</router-link>
    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'
import MatchTable from '../MatchTable.vue'

export default {
    data () {
        return {competition: {name: ''}}
    },
    components: {
        'match-table': MatchTable
    },
    created() {
        // get competition data
        axios.get(`/api/v1/competitions/` + this.$route.params.competition_id + `?expand=true`)
        .then(response => {
            this.competition = response.data
        })
    },
    computed: {
    }
}

</script>

<style>
</style>
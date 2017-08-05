<template id="opponent">
    <div>
        <h2>{{ opponent.name }}</h2>

        <div v-if="opponent.external_url">
            <a v-bind:href="opponent.external_url">Team's gotsoccer web site</a>
        </div>

        <h4>Team's record vs this opponent: {{opponent.match_results}}</h4>

        <match-table v-bind:matches="opponent.matches" v-bind:showOpponent=false> </match-table>

        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/opponent-list'">Back to opponent list</router-link>
    </div>
</template>


<script>

import axios from 'axios'
import _ from 'lodash'
import MatchTable from '../MatchTable.vue'

export default {
    data () {
        return {opponent: {name: ''}}
    },
    components: {
        'match-table': MatchTable
    },
    created() {
        // get opponent data
        axios.get(`/api/v1/opponents/` + this.$route.params.opponent_id + `?expand=true`)
        .then(response => {
            this.opponent = response.data
        })
    },
    computed: {
    }
}

</script>

<style>
</style>
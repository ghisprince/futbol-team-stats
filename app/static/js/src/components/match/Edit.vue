<template id="match-edit">
    <div>
        <h2>Edit match info</h2>
        <form>

            <match :match.sync="match"></match>
            <a class="btn btn-primary" v-on:click="updateMatch">
                Update Match Info
            </a>

            <hr/>

            <h2>Edit match stats</h2>
            <match-stats :match_stats.sync="match_stats"></match-stats>

            <a class="btn btn-primary" v-on:click="updateMatchStats">
                Update Match Stats
            </a>

            <hr/>

            <player-match-table :showActions=true&&user.is_editor></player-match-table>

            <hr/>

            <shot-graph :enableEditing=true></shot-graph>

            <br/>
        </form>
        <br/>
        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/match-list'">Back to match list</router-link>
        <br/>

    </div>
</template>


<script>
import axios from 'axios'
import Match from './Match.vue'
import MatchStats from './MatchStats.vue'
import PlayerMatchTable from '../player_match/PlayerMatchTable.vue'
import ShotGraph from '../player_match/ShotGraph.vue'


export default {
    data () {
        return {match: {},
                match_stats:{},
                user: {is_editor:false}
                }
    },
    components: {
        'match': Match,
        'match-stats': MatchStats,
        'shot-graph': ShotGraph,
        'player-match-table': PlayerMatchTable
    },
    created() {
        axios.get(`/api/v1/matches/` + this.$route.params.match_id + `?expand=true`)
        .then(response => {
            this.match = response.data;
            if ('match_stats' in response.data) {
                this.match_stats = response.data.match_stats;
            } else {
                this.match_stats = {};
            }
        })
        axios.get(`/api/v1/user`)
        .then(response => {
            this.user = response.data;
        })

    },
    methods: {
        updateMatch: function() {
            axios.patch(this.match._links.self,
                        {team: this.match.team,
                         date_time: this.match.date_time,
                         opponent: this.match.opponent,
                         competition: this.match.competition,
                         at_home: this.match.at_home
                         }
            )
        },
        updateMatchStats: function() {
            var ms = this.match_stats;
            delete ms.id;
            delete ms.match;
            axios.patch(this.match_stats._links.self,
                        this.match_stats
            )
        }
    }
}
</script>
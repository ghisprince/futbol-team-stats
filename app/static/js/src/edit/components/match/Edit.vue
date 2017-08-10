<template id="match-edit">
    <div>
        <h2>Edit match</h2>
        <form v-on:submit="updateMatch">

            <match :match.sync="match"></match>

            <player-match-table :showActions=true></player-match-table>

            <button type="submit" class="btn btn-primary">Save</button>
            <router-link class="btn btn-default" v-bind:to="'/match-list'">Cancel</router-link>
        </form>


    </div>
</template>


<script>
import axios from 'axios'
import Match from './Match.vue'
import PlayerMatchTable from './PlayerMatchTable.vue'


export default {
    data () {
        return {match: {}}
    },
    components: {
        'match': Match,
        'player-match-table': PlayerMatchTable
    },
    created() {
        axios.get(`/api/v1/matches/` + this.$route.params.match_id + `?expand=true`)
        .then(response => {
            this.match = response.data
        })
        .catch(e => {
            console.log(e)
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
            .then(response => {
                console.log("UPDATE match successful!")
                this.$router.go(-1)
            })
            .catch(e => {
                alert("UPDATE match failed")
                console.log(e)
            })
        }
    }
}
</script>
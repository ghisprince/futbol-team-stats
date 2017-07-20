<template id="player">
    <div>
        <h2>{{ player.name }} #{{ player.number}}</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>date</th>
                    <th>competition</th>
                    <th>opponent</th>
                    <th>result</th>
                    <th>starter</th>
                    <th>minutes</th>
                    <th>shots</th>
                    <th>goals</th>
                    <th>assists</th>
                    <th>corners</th>
                    <th>yellow_card</th>
                    <th>red_card</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="pm in playermatches">
                    <td align="left">
                        {{ pm.match.date_time | formatDate }}
                    </td>
                    <td align="left">
                        {{ pm.match.competition.name }}
                    </td>
                    <td align="left">
                        {{ pm.match.opponent.name }}
                    </td>
                    <td align="left">
                        {{ pm.match.result }}
                    </td>
                    <td align="left">
                        {{ pm.starter }}
                    </td>
                    <td align="left">
                        {{ pm.minutes }}
                    </td>
                    <td align="left">
                        {{ pm.shots.length }}
                    </td>
                    <td align="left">
                        {{ pm.num_goals }}
                    </td>
                    <td align="left">
                        {{ pm.assists.length }}
                    </td>
                    <td align="left">
                       {{ pm.corners }}
                    </td>
                    <td align="left">
                       {{ pm.yellow_card }}
                    </td>
                    <td align="left">
                       {{ pm.red_card }}
                    </td>
                </tr>
            </tbody>
        </table>
        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/'">Back to player list</router-link>
    </div>
</template>


<script>
import axios from 'axios'

export default {
    data () {
        return {player: {name: ''},
                playermatches: {}
                }
    },
    created() {
        // get player data
        axios.get(`/api/v1/players/` + this.$route.params.player_id)
        .then(response => {
            this.player = response.data
        })

        // get this player's matches data
        console.log(`/api/v1/playermatches/?player_id=` + this.$route.params.player_id + `&expand=true`)
        axios.get(`/api/v1/playermatches/?player_id=` + this.$route.params.player_id + `&expand=true`)
        .then(response => {
            this.playermatches = response.data;
        })
    }
}

</script>
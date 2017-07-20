<template id="player">
    <div>
        <h2>{{ player.name }} #{{ player.number}}</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>opponent</th>
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
                        {{pm.opponent}}
                    </td>
                    <td align="left">
                        {{pm.starter}}
                    </td>
                    <td align="left">
                        {{pm.minutes}}
                    </td>
                    <td align="left">
                        {{pm.shots.length}}
                    </td>
                    <td align="left">
                        {{pm.num_goals}}
                    </td>
                    <td align="left">
                        {{pm.assists.length}}
                    </td>
                    <td align="left">
                       {{pm.corners}}
                    </td>
                    <td align="left">
                       {{pm.yellow_card}}
                    </td>
                    <td align="left">
                       {{pm.red_card}}
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
        axios.get(`/api/v1/playermatches/?player_id=` + this.$route.params.player_id)
        .then(response => {
            var playermatches = response.data;
            for (var i = 0; i < playermatches.length; i++) {
                var match = {date_time: null,
                             opponent: null,
                             result: null
                             };

                axios.get(playermatches[i].match._links.self)
                .then(response => {
                    console.log(response.data.opponent.name)
                    playermatches[i].opponent = response.data.opponent.name;
                })
            }
            this.playermatches =  playermatches
        })
    }
}

</script>
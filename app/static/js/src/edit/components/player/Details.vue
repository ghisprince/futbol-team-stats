<template id="player">
    <div>
        <h2>{{ player.name }}</h2>

        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Competition</th>
                    <th>Opponent</th>
                    <th>Result</th>
                    <th title="Started the match">Starter</th>
                    <th title="Minutes played">Min</th>
                    <th title="Goals">G</th>
                    <th title="Assists">A</th>
                    <th title="Shots">S</th>
                    <th title="Yellow Cards">YC</th>
                    <th title="Red Cards">RC</th>
                    <th title="Subbed out due to injury">injury</th>
                </tr>
            </thead>
            <tfoot>
                <tr>
                    <td v-for="footSum in footSums"> {{ footSum }}</td>
                </tr>
            </tfoot>
            <tbody>
                <tr v-for="pm in orderedPlayerMatches">
                    <td>
                        <router-link v-bind:to="{name: 'match', params: {match_id: pm.match.id}}">
                            {{ pm.match.date_time | formatDate }}
                        </router-link>
                    </td>
                    <td>
                        {{ pm.match.competition.name }}
                    </td>
                    <td>
                        {{ pm.match.opponent.name }}
                    </td>
                    <td>
                        {{ pm.match.result }}
                    </td>
                    <td>
                        {{ pm.starter }}
                    </td>
                    <td>
                        {{ pm.minutes }}
                    </td>
                    <td>
                        {{ pm.num_goals }}
                    </td>
                    <td>
                        {{ pm.assists.length }}
                    </td>
                    <td>
                        {{ pm.shots.length }}
                    </td>
                    <td>
                        {{ pm.yellow_cards }}
                    </td>
                    <td>
                        {{ pm.red_cards }}
                    </td>
                    <td>
                        {{ pm.subbed_due_to_injury }}
                    </td>
                </tr>
            </tbody>
        </table>
        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/player-list'">Back to player list</router-link>
    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'


export default {
    data () {
        return {player: {name: null, number: null, player_matches: []} }
    },
    created() {
        // get player data
        axios.get(`/api/v1/players/` + this.$route.params.player_id + `?expand=true`)
        .then(response => {
            this.player = response.data
        })
    },
    getSum(items, prop){
        return items.reduce( function(a, b){
            return a + b[prop];
        }, 0);
    },
    computed: {
        player_num_matches : function() {
            return this.player.player_matches.length;
        },
        orderedPlayerMatches: function() {
            return _.orderBy(this.player.player_matches, 'match.date_time', 'desc')
        },
        footSums: function () {
            // why not "matches: this.player.player_matches.length? because vue
            //  gives this.player.player_matches is undefined, clearly
            //  lodash does it right though
            return ["Apps: " + _(this.player.player_matches).size(),
                    "-",
                    "-",
                    "-",
                    _.sum(_.map(this.player.player_matches, 'starter')),
                    _.sum(_.map(this.player.player_matches, 'minutes')),
                    _.sum(_.map(this.player.player_matches, 'num_goals')),
                    _.sum(_.map(this.player.player_matches, 'assists.length')),
                    _.sum(_.map(this.player.player_matches, 'shots.length')),
                    _.sum(_.map(this.player.player_matches, 'yellow_cards')),
                    _.sum(_.map(this.player.player_matches, 'red_cards')),
                    _.sum(_.map(this.player.player_matches, 'subbed_due_to_injury')),
                    ]
        }
    }
}

</script>

<style>
</style>
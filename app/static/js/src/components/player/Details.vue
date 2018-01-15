<template id="player">
    <div>
        <h2>{{ player.name }}</h2>

        <div v-show="!showTable">
            <vue-simple-spinner></vue-simple-spinner>
        </div>

        <div v-show="showTable">
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
                        <th title="Subbed out due to injury">Injury</th>
                        <th>Match Report</th>
                    </tr>
                </thead>
                <tfoot>
                    <tr>
                        <td v-for="footSum in footSums" v-bind:key="footSum.id"> 
                            {{ footSum.value }}
                        </td>
                    </tr>
                </tfoot>
                <tbody>
                    <tr v-for="pm in orderedPlayerMatches" v-bind:key="pm.id">
                        <td>
                            {{ pm.match.date_time | formatDate }}
                        </td>
                        <td>
                            {{ pm.match.competition.name }}
                        </td>
                        <td>
                            {{ pm.match.opponent_name }}
                        </td>
                        <td>
                            {{ pm.match.result }}
                        </td>
                        <td>
                            <div v-if="pm.starter">
                                <span class="glyphicon glyphicon-ok"></span>
                            </div>
                            <div v-else></div>
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
                            <div v-if="pm.subbed_due_to_injury">
                                <span class="glyphicon glyphicon-ok"></span>
                            </div>
                            <div v-else></div>
                        </td>
                        <td>
                            <router-link v-bind:to="{name: 'match', params: {match_id: pm.match.id}}">
                                Match Report <span class="glyphicon glyphicon-stats"></span>
                            </router-link>
                        </td>

                    </tr>
                </tbody>
            </table>
        </div>
        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/player-list'">Back to player list</router-link>
    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'
import Spinner from 'vue-simple-spinner'

export default {
    data () {
        return {player: {name: null, 
                         number: null, 
                         player_matches: []
                         },
                showTable: false
                }
    },
    created() {
        // get player data
        axios.get(`/api/v1/players/` + this.$route.params.player_id + `?expand=true`)
        .then(response => {
            this.player = response.data
            this.showTable=true;
        })
    },
    components: {
        'vue-simple-spinner': Spinner
    },
    computed: {
        player_num_matches : function() {
            return this.player.player_matches.length;
        },
        orderedPlayerMatches: function() {
            return _.orderBy(this.player.player_matches, 'match.date_time', 'desc')
        },
        footSums: function () {

            return [{id: 0, value: "Apps: " + _(this.player.player_matches).size()},
                    {id: 1, value: "-"},
                    {id: 2, value: "-"},
                    {id: 3, value: "-"},
                    {id: 4, value: _.sum(_.map(this.player.player_matches, 'starter'))},
                    {id: 5, value: _.sum(_.map(this.player.player_matches, 'minutes'))},
                    {id: 6, value: _.sum(_.map(this.player.player_matches, 'num_goals'))},
                    {id: 7, value: _.sum(_.map(this.player.player_matches, 'assists.length'))},
                    {id: 8, value: _.sum(_.map(this.player.player_matches, 'shots.length'))},
                    {id: 9, value: _.sum(_.map(this.player.player_matches, 'yellow_cards'))},
                    {id: 10, value: _.sum(_.map(this.player.player_matches, 'red_cards'))},
                    {id: 11, value: _.sum(_.map(this.player.player_matches, 'subbed_due_to_injury'))},
                    {id: 12, value: "-"}
                    ]
        }
    }
}

</script>

<style>
</style>
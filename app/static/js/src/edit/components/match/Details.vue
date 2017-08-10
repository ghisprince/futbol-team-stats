<template id="match">
    <div>

        <div id="match-details">
            <h2 id="section">Match info</h2>

            <table class="table table-striped table-bordered">
                <tbody>
                    <tr>
                        <th>Opponent</th>
                        <td>{{ match.opponent.name }}</td>
                    </tr>
                    <tr>
                        <th>Result</th>
                        <td>{{ match.result_long }}</td>
                    </tr>
                    <tr>
                        <th>Date/Time</th>
                        <td>{{ match.date_time | formatDate }}</td>
                    </tr>
                    <tr>
                        <th>Competition</th>
                        <td>{{ match.competition.name }}</td>
                    </tr>
                    <tr>
                        <th>Home game</th>
                        <td>{{ match.at_home }}</td>
                    </tr>
                </tbody>
            </table>

        </div>

        <player-match-table :showActions=false></player-match-table>

        <shot-graph></shot-graph>

        <br/>
        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/match-list'">Back to match list</router-link>

    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'
import PlayerMatchTable from './PlayerMatchTable.vue'
import ShotGraph from './ShotGraph.vue'

//  https://jsfiddle.net/n5osgpkg/
export default {
    props: [],
    data () {
        return {match: {date_time: null,
                        at_home: null,
                        team: null,
                        opponent: {name: ""},
                        competition: {name: ""},
                        player_matches: []
                        }
                }
    },
    components: {
        'shot-graph': ShotGraph,
        'player-match-table': PlayerMatchTable
    },
    created() {
        // get match data
        axios.get(`/api/v1/matches/` + this.$route.params.match_id + `?expand=true`)
        .then(response => {
            this.match = response.data
        })
    },
    computed: {
        match_num_matches : function() {
            return this.match.player_matches.length;
        },
        orderedPlayerMatches: function() {
            return _.orderBy(this.match.player_matches, 'player.name', 'desc')
        },
        footSums: function () {
            // "matches: this.match.player_matches.length? gives
            // this.match.player_matches is undefined, but lodash does it right
            return [_.size(this.match.player_matches),
                    "-",
                    _.sum(_.map(this.match.player_matches, 'minutes')),
                    _.sum(_.map(this.match.player_matches, 'num_goals')),
                    _.sum(_.map(this.match.player_matches, 'num_assists')),
                    _.sum(_.map(this.match.player_matches, 'shots.length')),
                    _.sum(_.map(this.match.player_matches, 'corners')),
                    _.sum(_.map(this.match.player_matches, 'yellow_cards')),
                    _.sum(_.map(this.match.player_matches, 'red_cards')),
                    _.sum(_.map(this.match.player_matches, 'subbed_due_to_injury'))
                    ]
        }
    }
}

</script>

<style>
    canvas{border:1px solid red;
           display: inline;
           width: 500;
           height: 500;
    }

    #canvas-container {
       width: 100%;
       text-align:center;
    }

    #match-details {
        text-align: left;
    }
</style>
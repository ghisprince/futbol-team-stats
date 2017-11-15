<template id="match">
    <div>
        <!-- remove this table in favor of simple str

        <div id="match-details">
            <h2 id="section">Match Details</h2>
            <table class="table">
                <tbody>
                    <tr>
                        <th>Date/Time</th>
                        <td>{{ match.date_time | formatDate }}</td>
                    </tr>
                    <tr>
                        <th>Competition</th>
                        <td>{{ match.competition.name }}</td>
                    </tr>
                    <tr>
                        <th>Duration (min)</th>
                        <td>{{ match.duration }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        -->

        <h5 id="section">{{ match.competition.name }}, {{ match.date_time | formatDate }}</h5>

        <h2 id="section">Team Stats</h2>
        <table class="table table-striped" align="center">
            <thead>
                <tr>
                    <th id="ra-col" class="col-md-5">{{ match.team.name }}</th>
                    <td id="ca-col" class="col-md-2"></td>
                    <th class="col-md-5">{{ match.opponent.name }}</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td id="ra-col">{{ match.num_goals }}</td>
                    <td id="ca-col">Goals</td>
                    <td>{{ match.num_goals_against }}</td>
                </tr>
                <tr>
                    <td id="ra-col">{{ match.num_shots }}</td>
                    <td id="ca-col">Shots</td>
                    <td>{{ match.num_shots_against }}</td>
                </tr>
                <tr>
                    <td id="ra-col">{{ match.shot_on_target_pct }}%</td>
                    <td id="ca-col">Shots On Target</td>
                    <td>{{ match.opponent_shot_on_target_pct }}%</td>
                </tr>
                <tr>
                    <td id="ra-col">{{ match.num_corners  }}</td>
                    <td id="ca-col">Corners</td>
                    <td>{{ match.num_opponent_corners ? match.num_opponent_corners : '?' }}</td>
                </tr>
                <tr>
                    <td id="ra-col">{{ match.num_yellow_cards }}</td>
                    <td id="ca-col">Yellow Cards</td>
                    <td>{{ match.num_opponent_yellow_cards ? match.num_opponent_yellow_cards : '?' }}</td>
                </tr>
                <tr>
                    <td id="ra-col">{{ match.num_red_cards }}</td>
                    <td id="ca-col">Red Cards</td>
                    <td>{{ match.num_opponent_red_cards ? match.num_opponent_red_cards : '?' }}</td>
                </tr>
                <tr v-if="match.num_passes">
                    <td id="ra-col">{{ match.num_passes }}</td>
                    <td id="ca-col">Pass</td>
                    <td>{{ match.num_opponent_passes }}</td>
                </tr>
                <tr v-if="match.pass_pct">
                    <td id="ra-col">{{ match.pass_pct }}%</td>
                    <td id="ca-col">Pass %</td>
                    <td>{{ match.opponent_pass_pct }}%</td>
                </tr>
                <tr v-if="match.num_pass_strings">
                    <td id="ra-col">{{ match.num_pass_strings }}</td>
                    <td id="ca-col" title="Pass Strings = 3+ consecutive passes">Pass Strings</td>
                    <td>{{ match.num_opponent_pass_strings }}</td>
                </tr>
            </tbody>
        </table>


        <player-match-table :showActions=false></player-match-table>

        <shot-graph :enableEditing=false></shot-graph>

        <br/>
        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/match-list'">Back to match list</router-link>

    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'
import moment from 'moment'
import PlayerMatchTable from '../player_match/PlayerMatchTable.vue'
import ShotGraph from '../player_match/ShotGraph.vue'


//  https://jsfiddle.net/n5osgpkg/
export default {
    props: [],
    data () {
        return {match: {date_time: null,
                        at_home: null,
                        team: {name: ""},
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
        date_time_pretty : function(v) {
            return v;
        },
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
    #ra-col {
        text-align: right;
    }
    #ca-col {
        text-align: center;
    }

</style>
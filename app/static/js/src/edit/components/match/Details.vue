<template id="match">
    <div>

        <div id="match-details">
            <h2 id="section">Match info</h2>
            <!--

                <strong>Opponent:</strong> {{ match.opponent.name }} <br/>
                <strong>Result:</strong> {{ match.result_long }} <br/>
                <strong>Date/time:</strong> {{ match.date_time | formatDate }}<br/>
                <strong>Competition:</strong>  {{ match.competition.name }} <br/>
                <strong>Home/Away:</strong> {{ match.at_home }} <br/>
            -->

            <table class="table table-striped">
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

        <h2 id="section">Player data</h2>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th title="Player">Player</th>
                    <th title="Started the match">Starter</th>
                    <th title="Minutes played">Min</th>
                    <th title="Goals">G</th>
                    <th title="Assists">A</th>
                    <th title="Shots">S</th>
                    <th title="Corners taken">C</th>
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
                        <router-link v-bind:to="{name: 'player', params: {player_id: pm.player.id}}">
                            {{ pm.player.name }}
                        </router-link>
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
                        {{ pm.corners }}
                    </td>
                    <td>
                        {{ pm.yellow_card}}
                    </td>
                    <td>
                        {{ pm.red_card}}
                    </td>
                    <td>
                        {{ pm.subbed_due_to_injury}}
                    </td>
                </tr>
            </tbody>
        </table>

        <h2 id="section">Shot/Goal data</h2>
        <shot-graph :player_matches="orderedPlayerMatches"></shot-graph>

        <br/>
        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/match-list'">Back to match list</router-link>

    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'
import ShotGraph from './ShotGraph.vue'
// The raw data to observe

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
        'shot-graph': ShotGraph
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
            return ["-",
                    "-",
                    _.sum(_.map(this.match.player_matches, 'minutes')),
                    _.sum(_.map(this.match.player_matches, 'num_goals')),
                    _.sum(_.map(this.match.player_matches, 'num_assists')),
                    _.sum(_.map(this.match.player_matches, 'shots.length')),
                    _.sum(_.map(this.match.player_matches, 'corners')),
                    _.sum(_.map(this.match.player_matches, 'yellow_card')),
                    _.sum(_.map(this.match.player_matches, 'red_card')),
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
    #section{
        text-align: left;
    }
</style>
<template id="match">
    <div>
        <h2> {{ match.date_time }}</h2>
        <h3> {{ match.at_home }} </h3>
        <h3> {{ match.opponent.name }} </h3>
        <h3> {{ match.competition.name }} </h3>
        <h3> {{ match.result }} </h3>

        <table class="table">
            <thead>
                <tr>
                    <th title="Player">Player</th>
                    <th title="Started the match">Starter</th>
                    <th title="Minutes played">Min</th>
                    <th title="Shots">S</th>
                    <th title="Assists">A</th>
                    <th title="Goals">G</th>
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
                        {{ pm.player.name }}
                    </td>
                    <td>
                        {{ pm.starter }}
                    </td>
                    <td>
                        {{ pm.minutes }}
                    </td>
                    <td>
                        {{ pm.shots.length }}
                    </td>
                    <td>
                        {{ pm.assists.length }}
                    </td>
                    <td>
                        {{ pm.num_goals }}
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
        <div id="canvas-container">
            <canvas id="canvas" width=400 height=400></canvas>
        </div>
        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/match-list'">Back to match list</router-link>
    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'

//  https://jsfiddle.net/n5osgpkg/
export default {
    props: [],
    data () {
        return {match: {date_time: null,
                        at_home: null,
                        team: null,
                        opponent: {name: ""},
                        competition: {name: ""},
                        player_matches: []} }
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
                    _.sum(_.map(this.match.player_matches, 'shots.length')),
                    _.sum(_.map(this.match.player_matches, 'num_goals')),
                    _.sum(_.map(this.match.player_matches, 'num_assists')),
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
           height: 500;}

    #canvas-container {
       width: 100%;
       text-align:center;
}
</style>
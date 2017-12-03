<template id="agg-player-match-table">
    <div>
        <h2 id="section">Aggregated Player data</h2>
        <div v-show="!showTable">
            <vue-simple-spinner></vue-simple-spinner>
        </div>
        <div v-show="showTable">
            <table class="table table-striped table-bordered">
                <thead>
                    <tr>
                        <th title="Player">Player</th>
                        <th title="Appearances by player">Apps</th>
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
                    <tr v-for="pms in aggregatedPlayerMatches">
                        <td>
                            {{ pms.player }}
                        </td>
                        <td>
                            {{ pms.apps }}
                        </td>
                        <td>
                            {{ pms.starter }}
                        </td>
                        <td>
                            {{ pms.minutes }}
                        </td>
                        <td>
                            {{ pms.num_goals ? pms.num_goals : '' }}
                        </td>
                        <td>
                            {{ pms.assists ? pms.assists : '' }}
                        </td>
                        <td>
                            {{ pms.shots ? pms.shots : '' }}
                        </td>
                        <td>
                            {{ pms.yellow_cards ? pms.yellow_cards : '' }}
                        </td>
                        <td>
                            {{ pms.red_cards ? pms.red_cards : '' }}
                        </td>
                        <td>
                            {{ pms.subbed_due_to_injury ? pms.subbed_due_to_injury : '' }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p id="sub-table-note"><i>Bottom most row is summary of each column</i></p>

    </div>
</template>


<script>

import _ from 'lodash'
import Spinner from 'vue-simple-spinner'

function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
}

function countShotsfor(pm) {
    var count = 0;

    for (var i=0; i < pm.shots.length; i++) {
        if (pm.shots[i].by_opponent == false) {
            count ++;
        }
    }
    return count
}

function sum(numbers) {
    return _.reduce(numbers, function(result, current) {
        return result + parseFloat(current);
    }, 0);
}

function countTrue(bools) {
    return bools.reduce(function(a, b){
            return b?a+1:a;
    },0);
}

export default {
    props: {
        player_matches: {}
    },
    data() {
        return {
            showTable: false
        }
    },
    created() {},
    components: {
        'vue-simple-spinner': Spinner
    },
    computed: {
        aggregatedPlayerMatches: function() {
            // https://stackoverflow.com/questions/22954066/group-by-and-aggregation-on-json-array-using-underscore-js
            return _.chain(this.player_matches)
                    .groupBy("player.name")
                    .map(function(value, key) {
                        return {
                            player: key,
                            apps: value.length,
                            starter: countTrue(_.map(value, "starter")),
                            minutes: sum(_.map(value, "minutes")),
                            num_goals: sum(_.map(value, "num_goals")),
                            assists: sum(_.map(value, "assists.length")),
                            //shots: sum(_.map(value, "shots.length")),
                            //shots: _.filter(value, {'shots.by_opponent': true} ).length,
                            shots: sum(_.map(value, countShotsfor)),
                            yellow_cards: sum(_.map(value, "yellow_cards")),
                            red_cards: sum(_.map(value, "red_cards")),
                            subbed_due_to_injury: countTrue(_.map(value, "subbed_due_to_injury"))
                        }
            })
            .value().sort();

        },
        footSums: function () {

            var tds = [
                    "Count: " + _(this.aggregatedPlayerMatches).size(),
                    "-",
                    "-",
                    _.sum(_.map(this.player_matches, 'minutes')),
                    _.sum(_.map(this.player_matches, 'num_goals')),
                    _.sum(_.map(this.player_matches, 'assists.length')),
                    _.sum(_.map(this.player_matches, countShotsfor)),
                    _.sum(_.map(this.player_matches, 'yellow_cards')),
                    _.sum(_.map(this.player_matches, 'red_cards')),
                    _.sum(_.map(this.player_matches, 'subbed_due_to_injury')),
                    ];

            // show the table once all values are computed
            if (_(this.aggregatedPlayerMatches).size() > 0) {
                this.showTable=true;
            }
            return tds;
        }
    }
}

</script>


<style>
</style>

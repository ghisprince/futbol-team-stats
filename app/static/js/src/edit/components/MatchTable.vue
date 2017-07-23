<template id="match-table">
    <div>

        <table class="table">
            <thead>
                <tr>
                    <th>Date</th>
                    <th v-if="showCompetition">Competition</th>
                    <th v-if="showOpponent">Opponent</th>
                    <th>Result</th>
                    <th title="Goals For">GF</th>
                    <th title="Goals Against">GA</th>
                    <th title="Shots For">SF</th>
                    <th title="Shots Against">SA</th>
                    <th>Match details</th>
                </tr>
            </thead>
            <tfoot>
                <tr>
                    <td v-for="footSum in footSums"> {{ footSum }}</td>
                </tr>
            </tfoot>
            <tbody>
                <tr v-for="match in orderedMatches">
                    <td>
                        {{ match.date_time | formatDate }}
                    </td>
                    <td v-if="showCompetition === true">
                        {{ match.competition.name }}
                    </td>
                    <td v-if="showOpponent">
                        {{ match.opponent.name }}
                    </td>
                    <td>
                        {{ match.result }}
                    </td>
                    <td>
                        {{ match.num_goals }}
                    </td>
                    <td>
                        {{ match.num_goals_against }}
                    </td>
                    <td>
                        {{ match.num_shots }}
                    </td>
                    <td>
                        {{ match.num_shots_against }}
                    </td>
                    <td>
                        <router-link v-bind:to="{name: 'match', params: {match_id: match.id, uri: match._links.self}}">
                            Match Details
                        </router-link>
                    </td>
                    <td v-if="showActions">
                        <router-link class="btn btn-warning btn-xs"
                                     v-bind:to="{name: 'match-edit', params: {match_id: match.id, uri: match._links.self}}">
                            <span class="glyphicon glyphicon-pencil"></span> Edit
                        </router-link>
                        <router-link v-if="match.player_matches.length == 0"
                                     class="btn btn-danger btn-xs" v-bind:to="{name: 'match-delete', params: {match_id: match.id, type: 'match', name: match.name, uri: match._links.self}}">
                            <span class="glyphicon glyphicon-remove"></span> Delete
                        </router-link>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>


<script>

import _ from 'lodash'

export default {
    props: {matches: {},
            showCompetition: {default: true},
            showOpponent: {default: true},
            showActions: {default: false}
            },
    data () {
        return {}
    },
    created() {
    },
    computed: {
        orderedMatches: function() {
            return _.orderBy(this.matches, 'date_time', 'desc')
        },
        footSums: function () {
            // why not "match: this.player.player_match.length? because vue
            //  gives this.player.player_match is undefined, clearly
            //  lodash does it right though
            var tds = ["-"];
            if (this.showCompetition){
                var tds = tds.concat(["-"]);
            }
            if (this.showOpponent){
                var tds = tds.concat(["-"]);
            }

             var tds = tds.concat(
                   ["-",
                    _.sum(_.map(this.matches, 'num_goals')),
                    _.sum(_.map(this.matches, 'num_goals_against')),
                    _.sum(_.map(this.matches, 'num_shots')),
                    _.sum(_.map(this.matches, 'num_shots_against')),
                    "-"
                    ]);
             return tds;
        }
    }
}

</script>


<style>
</style>

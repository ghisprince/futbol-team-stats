<template id="match-table">
    <div>
        <div class="filters row" v-show="showCompetition && showOpponent">
            <div class="form-group col-sm-3">
                <label for="search-element">Name filter</label>
                <input v-model="searchKey" class="form-control" id="search-element" required/>
            </div>
        </div>

        <div v-show="!showTable">
            <vue-simple-spinner></vue-simple-spinner>
        </div>
        <div v-show="showTable">

            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Match Date</th>
                        <th v-if="showCompetition">Competition</th>
                        <th v-if="showOpponent">Opponent</th>
                        <th>Result</th>
                        <th title="Goals For">GF</th>
                        <th title="Goals Against">GA</th>
                        <th title="Shots For">SF</th>
                        <th title="Shots Against">SA</th>
                        <th title="Detailed Match Report">Match Report</th>
                        <th v-if="showActions">Actions</th>
                    </tr>
                </thead>
                <tfoot>
                    <tr>
                        <td v-for="footSum in footSums" v-bind:key="footSum.id"> {{ footSum.value }}</td>
                    </tr>
                </tfoot>
                <tbody>
                    <tr v-for="match in orderedMatches" v-bind:key="match.id">
                        <td>
                            {{ match.date_time | formatDate }}
                        </td>
                        <td v-if="showCompetition === true">
                            <router-link v-bind:to="{name: 'competition', params: {competition_id: (Number.isInteger(match.competition) ? match.competition :  match.competition.id ) }}">
                                {{ match.competition_name }}
                            </router-link>
                        </td>
                        <td v-if="showOpponent">
                            <router-link v-bind:to="{name: 'opponent', params: {opponent_id: (Number.isInteger(match.opponent) ? match.opponent :  match.opponent.id ) }}">
                                {{ match.opponent_name }}
                            </router-link>
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
                                Match Report <span class="glyphicon glyphicon-stats"></span>
                            </router-link>
                        </td>
                        <td v-if="showActions">
                            <router-link class="btn btn-warning btn-xs"
                                         v-bind:to="{name: 'match-edit', params: {match_id: match.id, uri: match._links.self}}">
                                <span class="glyphicon glyphicon-pencil"></span> Edit
                            </router-link>
                            <router-link v-if="match.player_matches.length == 0"
                                         class="btn btn-danger btn-xs"
                                         v-bind:to="{name: 'match-delete', params: {match_id: match.id, type: 'match', name: match.name, uri: match._links.self}}">
                                <span class="glyphicon glyphicon-remove"></span> Delete
                            </router-link>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>


<script>

import _ from 'lodash'
import Spinner from 'vue-simple-spinner'


export default {
    props: {matches: {},
            showCompetition: {default: true},
            showOpponent: {default: true},
            showActions: {default: false}
    },
    data() {
        return {
            showTable: false,
            searchKey: ''
        }
    },
    created() {
    },
    components: {
        'vue-simple-spinner': Spinner
    },
    computed: {
        orderedMatches: function() {
            if (!this.matches) {
                return [];
            }
            var matches = this.matches.filter(function (match) {
                return this.searchKey=='' || match.opponent_name.indexOf(this.searchKey) !== -1 || match.competition_name.indexOf(this.searchKey) !== -1;
            }, this);

            return _.orderBy(matches, 'date_time', 'desc')
        },
        footSums: function () {
            // why not "match: this.player.player_match.length? because vue
            //  gives this.player.player_match is undefined, clearly
            //  lodash does it right though
            var tds = [{id: 0, value: "Count: " + _(this.matches).size()}];

            if (_(this.matches).size() > 0) {
                this.showTable=true;
            }

            if (this.showCompetition){
                var tds = tds.concat(["-"]);
            }

            if (this.showOpponent){
                var tds = tds.concat([{id: 1, value: "-"}]);
            }

             var tds = tds.concat(
                   [{id: 2, value: "-"},
                    {id: 3, value: _.sum(_.map(this.matches, 'num_goals'))},
                    {id: 4, value: _.sum(_.map(this.matches, 'num_goals_against'))},
                    {id: 5, value: _.sum(_.map(this.matches, 'num_shots'))},
                    {id: 6, value: _.sum(_.map(this.matches, 'num_shots_against'))},
                    {id: 7, value: "-"}
                    ]);
             return tds;
        }
    }
}

</script>


<style>
</style>

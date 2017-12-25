<template id="player-match-table">
    <div>
        <h2 id="section">Player Stats</h2>
        <div v-show="!showTable">
            <vue-simple-spinner></vue-simple-spinner>
        </div>
        <div v-show="showTable">
            <table class="table table-striped table-bordered">
                <thead>
                    <tr>
                        <th title="Player">Player</th>
                        <th title="Started the match">Starter</th>
                        <th title="Minutes played">Min</th>
                        <th title="Goals">G</th>
                        <th title="Assists">A</th>
                        <th title="Shots">S</th>
                        <th title="Corners">Corners</th>
                        <th title="Yellow Cards">YC</th>
                        <th title="Red Cards">RC</th>
                        <th title="Subbed out due to injury">Injury</th>
                        <th v-if="showActions">Actions</th>
                    </tr>
                </thead>
                <tfoot>
                    <tr>
                        <td v-for="footSum in footSums"> {{ footSum }}</td>
                        <td v-if="showActions">
                            <router-link class="btn btn-success btn-xs"
                                         v-bind:to="{name: 'playermatch-add', params: {match_id: $route.params.match_id }}">
                                <span class="glyphicon glyphicon-plus"></span> Add
                            </router-link>
                        </td>
                    </tr>
                </tfoot>
                <tbody>
                    <tr v-for="pm in player_matches">
                        <td>
                            <router-link v-bind:to="{name: 'player', params: {player_id: pm.player.id}}">
                                {{ pm.player.name }}
                            </router-link>
                        </td>
                        <td>
                            {{ pm.starter ? 'Y' : '' }}
                        </td>
                        <td>
                            {{ pm.minutes }}
                        </td>
                        <td>
                            {{ pm.num_goals ? pm.num_goals : '' }}
                        </td>
                        <td>
                            {{ pm.assists.length ? pm.assists.length : '' }}
                        </td>
                        <td>
                            {{ pm.shots.filter(function(i){return i.by_opponent == false;}).length  ? pm.shots.filter(function(i){return i.by_opponent == false;}).length : '' }}

                        </td>
                        <td>
                            {{ pm.corners ? pm.corners : '' }}
                        </td>
                        <td>
                            {{ pm.yellow_cards ? pm.yellow_cards : '' }}
                        </td>
                        <td>
                            {{ pm.red_cards ? pm.red_cards : '' }}
                        </td>
                        <td>
                            {{ pm.subbed_due_to_injury ? 'Y' : '' }}
                        </td>
                        <td v-if="showActions">
                            <router-link class="btn btn-warning btn-xs"
                                         v-bind:to="{name: 'playermatch-edit', params: {playermatch_id: pm.id, uri: pm._links.self}}">
                                <span class="glyphicon glyphicon-pencil"></span> Edit
                            </router-link>

                            <a class="btn btn-danger btn-xs" v-on:click="deletePlayerMatch( pm )">
                                <span class="glyphicon glyphicon-remove"></span> Delete
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p id="sub-table-note"><i>Bottom most row is summary of each column</i></p>

    </div>
</template>


<script>

import axios from 'axios'
import _ from 'lodash'
import Spinner from 'vue-simple-spinner'

function num_shots_not_by_opponent(pm){
    var iii;
    var count = 0;
    for (iii=0; iii < pm.shots.length; iii++){
        if (pm.shots[iii].by_opponent == false) count ++;
    }
    return count;
}

export default {
    props: {showActions: {default: false}
    },
    data () {
        return {player_matches: [],
                showTable: false
                }
    },
    components: {
        'vue-simple-spinner': Spinner
    },
    created() {
        var parent = this;
        axios.get(`/api/v1/playermatches/?match_id=` + this.$route.params.match_id + `&expand=true`)
        .then(response => {
            this.player_matches = _.orderBy(response.data, "player.name");
            this.showTable=true;
        })
    },
    computed: {
        footSums: function () {
            var tds = [
                    "Players: " + _(this.player_matches).size(),
                    _.sum(_.map(this.player_matches, 'starter')),
                    _.sum(_.map(this.player_matches, 'minutes')),
                    _.sum(_.map(this.player_matches, 'num_goals')),
                    _.sum(_.map(this.player_matches, 'assists.length')),
                    _.sum(_.map(this.player_matches, num_shots_not_by_opponent)),
                    _.sum(_.map(this.player_matches, 'corners')),
                    _.sum(_.map(this.player_matches, 'yellow_cards')),
                    _.sum(_.map(this.player_matches, 'red_cards')),
                    _.sum(_.map(this.player_matches, 'subbed_due_to_injury')),
                    ];

            return tds;
        }
    },
    methods: {
        deletePlayerMatch: function(pm) {
            // remove all assists joined to this playermatch first
            axios.get(`/api/v1/assists/?playermatch_id=` + pm.id)
            .then(response => {
                var assists = response.data;
                for (var i=0; i < assists.length; i++){
                    axios.delete(assists[i]._links.self)
                    .then(response => {console.log("delete assist succeeded")})
                    .catch(response => {console.log("delete assist failed")})

                }
                // then delete the playermatch
                axios.delete(pm._links.self)
                .then(response => {
                    // update this.player_matches to excluded pm just deleted
                    this.player_matches = _.filter(this.player_matches, function(i) {
                            return i.id != pm.id;
                        })
                })
            })
        }
    }
}

</script>


<style>
</style>

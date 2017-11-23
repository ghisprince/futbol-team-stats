<template id="player-list">
    <div>
        <div class="actions">
            <router-link class="btn btn-success" v-bind:to="{path: '/add-player'}">
                <span class="glyphicon glyphicon-plus"></span>
                Add player
            </router-link>
        </div>
        <div class="filters row">
            <div class="form-group col-sm-3">
                <label for="search-element">Name filter</label>
                <input v-model="searchKey" class="form-control" id="search-element" required/>
            </div>
        </div>
        <table class="table">
            <thead>
                <tr>
                <th>Name</th>
                <th>Active</th>
                <th>Matches</th>
                <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="player in filteredPlayers">
                <td>
                    {{ player.name }} #{{player.number}}
                </td>
                <td>
                    {{ player.active }}
                </td>
                <td>
                    <router-link v-bind:to="{name: 'player', params: {player_id: player.id}}">
                        {{ player.player_matches.length }} matches
                    </router-link>
                </td>
                <td>
                    <router-link class="btn btn-warning btn-xs"
                                 v-bind:to="{name: 'player-edit', params: {player_id: player.id}}">
                        <span class="glyphicon glyphicon-pencil"></span> Edit
                    </router-link>
                    <router-link v-if="player.player_matches.length == 0"
                                 class="btn btn-danger btn-xs" v-bind:to="{name: 'player-delete', params: {player_id: player.id, type: 'player', name: player.name, uri: player._links.self}}">
                        <span class="glyphicon glyphicon-remove"></span> Delete
                    </router-link>
                </td>
                </tr>
            </tbody>
        </table>

        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/'">Back to editing options</router-link>

    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'

export default {
    data () {
        return {
            players: [],
            searchKey: ''
        }
    },
    created() {
        axios.get(`/api/v1/players`)
        .then(response => {
            this.players = response.data
        })
    },
    computed: {
        filteredPlayers: function () {
            return this.orderedPlayers.filter(function (player) {
                return this.searchKey=='' || player.name.indexOf(this.searchKey) !== -1;
            },this);
        },
        orderedPlayers: function() {
            return _.orderBy(this.players, 'name')
        }
    }
}
</script>
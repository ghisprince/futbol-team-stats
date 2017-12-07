<template id="player-list">
    <div>
        <div class="actions" v-show="$root.current_user.is_editor">
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

        <div v-show="!showTable">
            <vue-simple-spinner></vue-simple-spinner>
        </div>

        <div v-show="showTable">
            <table class="table">
                <thead>
                    <tr>
                    <th>Name</th>
                    <th>Active</th>
                    <th>Matches</th>
                    <th v-show="$root.current_user.is_editor">Actions</th>
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
                    <td v-show="$root.current_user.is_editor">
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
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'
import Spinner from 'vue-simple-spinner'

export default {
    data () {
        return {
            players: [],
            showTable: false,
            searchKey: ''
        }
    },
    created() {
        axios.get(`/api/v1/players`)
        .then(response => {
            this.players = response.data;
            this.showTable=true;
        })
    },
    components: {
        'vue-simple-spinner': Spinner
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
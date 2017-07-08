<template id="player-list">
    <div>
        <div class="actions">
            <router-link class="btn btn-default" v-bind:to="{path: '/add-player'}">
                <span class="glyphicon glyphicon-plus"></span>
                Add player
            </router-link>
        </div>
        <div class="filters row">
            <div class="form-group col-sm-3">
                <label for="search-element">Player name</label>
                <input v-model="searchKey" class="form-control" id="search-element" requred/>
            </div>
        </div>
        <table class="table">
            <thead>
                <tr>
                <th>Name</th>
                <th>Number</th>
                <th>Statistics</th>
                <th class="col-sm-2">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="player in filteredPlayers">
                <td align="left">
                    <router-link v-bind:to="{name: 'player', params: {player_id: player.id}}">{{ player.name }}</router-link>
                </td>
                <td align="left">{{ player.number}}</td>
                <td align="left"> Stats page </td>
                <td>
                    <router-link class="btn btn-warning btn-xs" v-bind:to="{name: 'player-edit', params: {player_id: player.id}}">Edit</router-link>
                    <router-link class="btn btn-danger btn-xs" v-bind:to="{name: 'player-delete', params: {player_id: player.id}}">Delete</router-link>
                </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>


<script>
import axios from 'axios'

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
        .catch(e => {
            console.log(e)
        })
    },
    computed: {
        filteredPlayers: function () {
            return this.players.filter(function (player) {
                return this.searchKey=='' || player.name.indexOf(this.searchKey) !== -1;
            },this);
        }
    }
}
</script>
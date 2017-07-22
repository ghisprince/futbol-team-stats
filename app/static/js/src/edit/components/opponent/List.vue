<template id="opponent-list">
    <div>
        <div class="actions">
            <router-link class="btn btn-default" v-bind:to="{path: '/add-opponent'}">
                <span class="glyphicon glyphicon-plus"></span>
                Add opponent
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
                <th>Matches</th>
                <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="opponent in filteredOpponents">
                <td>
                    {{ opponent.name }}
                </td>
                <td>
                    <router-link v-bind:to="{name: 'opponent', params: {opponent_id: opponent.id, uri: opponent._links.self}}">
                        {{ opponent.match_results }}
                    </router-link>
                </td>
                <td>
                    <router-link class="btn btn-warning btn-xs"
                                 v-bind:to="{name: 'opponent-edit', params: {opponent_id: opponent.id, uri: opponent._links.self}}">
                        <span class="glyphicon glyphicon-pencil"></span> Edit
                    </router-link>
                    <router-link v-if="opponent.matches.length == 0"
                                 class="btn btn-danger btn-xs"
                                 v-bind:to="{name: 'opponent-delete', params: {opponent_id: opponent.id, type: 'opponent', name: opponent.name, uri: opponent._links.self}}">
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
            opponents: [],
            searchKey: ''
        }
    },
    created() {
        axios.get(`/api/v1/opponents`)
        .then(response => {
            this.opponents = response.data
        })
        .catch(e => {
            console.log(e)
        })
    },
    computed: {
        filteredOpponents: function () {
            return this.orderedOpponents.filter(function (opponent) {
                return this.searchKey=='' || opponent.name.indexOf(this.searchKey) !== -1;
            },this);
        },
        orderedOpponents: function() {
            return _.orderBy(this.opponents, 'name')
        }
    }
}
</script>
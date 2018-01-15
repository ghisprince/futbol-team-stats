<template id="opponent-list">
    <div>
        <div class="actions" v-show="$root.current_user.is_editor">
            <router-link class="btn btn-success" v-bind:to="{path: '/add-opponent'}">
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

        <div v-show="!showTable">
            <vue-simple-spinner></vue-simple-spinner>
        </div>

        <div v-show="showTable">

            <table class="table table-striped">
                <thead>
                    <tr>
                    <th>Name</th>
                    <th title="Matches Played">MP</th>
                    <th title="Matches Won">W</th>
                    <th title="Matches Tied">D</th>
                    <th title="Matches Lost">L</th>
                    <th v-show="$root.current_user.is_editor">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="opponent in filteredOpponents" v-bind:key="opponent.id">
                    <td>
                        <router-link v-bind:to="{name: 'opponent', params: {opponent_id: opponent.id}}">
                            {{ opponent.name }}
                        </router-link>
                    </td>
                    <td>
                        {{ opponent.matches.length }}
                    </td>
                    <td>
                        {{ opponent.num_match_won }}
                    </td>
                    <td>
                        {{ opponent.num_match_tied }}
                    </td>
                    <td>
                        {{ opponent.num_match_lost }}
                    </td>
                    <td v-show="$root.current_user.is_editor">
                        <router-link class="btn btn-warning btn-xs"
                                     v-bind:to="{name: 'opponent-edit', params: {opponent_id: opponent.id}}">
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
            opponents: [],
            showTable: false,
            searchKey: ''
        }
    },
    created() {
        axios.get(`/api/v1/opponents`)
        .then(response => {
            this.opponents = _.sortBy(response.data, "name");
            this.showTable=true;
        })
    },
    components: {
        'vue-simple-spinner': Spinner
    },
    computed: {
        filteredOpponents: function () {
            return this.opponents.filter(function (opponent) {
                return this.searchKey=='' || opponent.name.indexOf(this.searchKey) !== -1;
            },this);
        }
    }
}
</script>
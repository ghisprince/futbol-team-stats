<template id="competition-list">
    <div>
        <div class="actions">
            <router-link class="btn btn-success" v-bind:to="{path: '/add-competition'}">
                <span class="glyphicon glyphicon-plus"></span>
                Add competition
            </router-link>
        </div>
        <div class="filters row">
            <div class="form-group col-sm-3">
                <label for="search-element">Name filter</label>
                <input v-model="searchKey" class="form-control" id="search-element" required/>
            </div>
        </div>
        <table class="table table-striped">
            <thead>
                <tr>
                <th>Name </th>
                <th>Result</th>
                <th title="Matches Played">MP</th>
                <th title="Matches Won">W</th>
                <th title="Matches Tied">D</th>
                <th title="Matches Lost">L</th>
                <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="competition in filteredCompetitions">
                <td>
                    <router-link v-bind:to="{name: 'competition', params: {competition_id: competition.id}}">
                        {{ competition.name }}
                    </router-link>
                </td>
                <td>
                    {{ competition.result }}
                </td>
                <td>
                    {{ competition.matches.length }}
                </td>
                <td>
                    {{ competition.num_match_won }}
                </td>
                <td>
                    {{ competition.num_match_tied }}
                </td>
                <td>
                    {{ competition.num_match_lost }}
                </td>

                <td>
                    <router-link class="btn btn-warning btn-xs"
                                 v-bind:to="{name: 'competition-edit', params: {competition_id: competition.id}}">
                        <span class="glyphicon glyphicon-pencil"></span> Edit
                    </router-link>
                    <router-link v-if="competition.matches.length == 0"
                                 class="btn btn-danger btn-xs" v-bind:to="{name: 'competition-delete', params: {competition_id: competition.id, type: 'competition', name: competition.name, uri: competition._links.self}}">
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
            competitions: [],
            searchKey: ''
        }
    },
    created() {
        axios.get(`/api/v1/competitions`)
        .then(response => {
            this.competitions = response.data
        })
        .catch(e => {
            console.log(e)
        })
    },
    computed: {
        filteredCompetitions: function () {
            return this.orderedCompetitions.filter(function (competition) {
                return this.searchKey=='' || competition.name.indexOf(this.searchKey) !== -1;
            },this);
        },
        orderedCompetitions: function() {
            return _.orderBy(this.competitions, 'name')
        }
    }
}
</script>
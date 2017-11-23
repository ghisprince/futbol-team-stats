<template id="match-list">
    <div>
        <div class="actions">
            <router-link class="btn btn-success" v-bind:to="{path: '/add-match'}">
                <span class="glyphicon glyphicon-plus"></span>
                Add match
            </router-link>
        </div>

        <div class="filters row">
            <div class="form-group col-sm-3">
                <label for="search-element">Name filter</label>
                <input v-model="searchKey" class="form-control" id="search-element" required/>
            </div>
        </div>

        <match-table v-bind:matches="matches" v-bind:showActions=true> </match-table>

        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/'">Back to editing options</router-link>

    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'
import MatchTable from '../MatchTable.vue'

export default {
    data () {
        return {
            matches: [],
            searchKey: ''
        }
    },
    created() {
        axios.get(`/api/v1/matches?expand=true`)
        .then(response => {
            this.matches = response.data
        })
    },
    components: {
        'match-table': MatchTable
    }
}
</script>
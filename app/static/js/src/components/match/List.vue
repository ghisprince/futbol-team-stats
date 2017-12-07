<template id="match-list">
    <div>
        <div class="actions" v-show="$root.current_user.is_editor">
            <router-link class="btn btn-success" v-bind:to="{path: '/add-match'}">
                <span class="glyphicon glyphicon-plus"></span>
                Add match
            </router-link>
        </div>

        <match-table v-bind:matches="matches" v-bind:showActions=true&&user.is_editor>
        </match-table>
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
            searchKey: '',
            user: {is_editor:false}
        }
    },
    created() {
        axios.get(`/api/v1/matches?expand=true`)
        .then(response => {
            this.matches = response.data
        })
        axios.get(`/api/v1/user`)
        .then(response => {
            this.user = response.data;
        })
    },
    components: {
        'match-table': MatchTable
    }

}
</script>
<template id="add-match">
    <div>
        <h2>Add new match</h2>
        <form v-on:submit="createMatch">
        
            <match :match.sync="match"></match>

            <button type="submit" class="btn btn-primary">Create</button>
            <router-link class="btn btn-default" v-bind:to="'/match-list'">
                Cancel
            </router-link>
        </form>
    </div>
</template>


<script>

import axios from 'axios'
import Match from './Match.vue'

export default {
    data () {
        return {match:
                    {date_time: null,
                     opponent: {name: null},
                     competition: {name: null},
                     at_home: null,
                     team:{id: 1}
                     },
                 opponents: [],
                 competitions: []
                }
    },
    components: {
        'match': Match
    },
    methods: {
        createMatch: function() {
            axios.post(`/api/v1/matches/`, this.match)
            .then(response => {
                this.match = response.data;

                // for convinience create matchstats also
                axios.post(`/api/v1/matchstats/`,
                           {match: {id: response.data.id}}
                )

                this.$router.push({path: '/match-list'})
            })
        }
    }
}

</script>
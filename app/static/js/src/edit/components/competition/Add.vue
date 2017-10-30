<template id="add-competition">
    <div>
        <h2>Add new competition</h2>
        <form v-on:submit="createCompetition">

            <competition :competition.sync="competition"></competition>

            <button type="submit" class="btn btn-primary">Create</button>
            <router-link class="btn btn-default" v-bind:to="'/competition-list'">Cancel</router-link>
        </form>
    </div>
</template>


<script>

import axios from 'axios'
import Competition from './Competition.vue'

export default {
    data () {
        return {competition: {name: null,
                              result: null,
                              external_url: null}
                              }
    },
    components: {
        'competition': Competition
    },
    methods: {
        createCompetition: function() {
            axios.post(`/api/v1/competitions/`, this.competition)
            .then(response => {
                this.competition = response.data
                //this.$router.go(-1)
                this.$router.push({path: '/competition-list'})
            })
            .catch(e => {
                console.log(e)
            })
        }
    }
}

</script>
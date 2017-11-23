<template id="competition-edit">
    <div>
        <h2>Edit competition</h2>
        <form v-on:submit="updateCompetition">

            <competition :competition.sync="competition"></competition>

            <button type="submit" class="btn btn-primary">Save</button>
            <router-link class="btn btn-default" v-bind:to="'/competition-list'">Cancel</router-link>
        </form>

    </div>
</template>


<script>
import axios from 'axios'
import Competition from './Competition.vue'

export default {
    props: [],
    data () {
        return {competition: {}}
    },
    components: {
        'competition': Competition
    },
    created() {
        axios.get(`/api/v1/competitions/` + this.$route.params.competition_id + `?expand=true`)
        .then(response => {
            this.competition = response.data
        })
    },
    methods: {
        updateCompetition: function() {
            axios.patch(this.competition._links.self,
                        {name: this.competition.name,
                         result: this.competition.result,
                         external_url: this.competition.external_url
                         }
            )
            .then(response => {
                this.$router.push({path: '/competition-list'})
            })
        }
    }
}
</script>
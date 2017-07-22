<template id="add-competition">
    <div>
        <h2>Add new competition</h2>
        <form v-on:submit="createCompetition">
        <div class="form-group">
            <label for="add-name">Name</label>
            <input class="form-control" id="add-name" v-model="competition.name" required/>
            <label for="add-url">Url</label>
            <input type="url" class="form-control" id="add-url" v-model="competition.url"/>
        </div>
        <button type="submit" class="btn btn-primary">Create</button>
        <router-link class="btn btn-default" v-bind:to="'/competition-list'">Cancel</router-link>
        </form>
    </div>
</template>


<script>

import axios from 'axios'

export default {
    data () {
        return {competition: {name: '', url: null}}
    },
    methods: {
        createCompetition: function() {
            axios.post(`/api/v1/competitions/`, this.competition)
            .then(response => {
                this.competition = response.data
                this.$router.go(-1)
            })
            .catch(e => {
                console.log(e)
            })
        }
    }
}

</script>
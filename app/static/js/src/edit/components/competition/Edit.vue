<template id="competition-edit">
    <div>
        <h2>Edit competition</h2>
        <form v-on:submit="updateCompetition">

        <div class="form-group">
            <label for="edit-name">Name</label>
            <input class="form-control" id="edit-name" v-model="competition.name" required/>

            <label for="edit-result">Result</label>
            <input class="form-control" id="edit-result" v-model="competition.result"/>

            <label for="edit-eurl">URL</label>
            <input class="form-control" id="edit-eurl" v-model="competition.external_url"/>
        </div>

        <button type="submit" class="btn btn-primary">Save</button>
        <router-link class="btn btn-default" v-bind:to="'/competition-list'">Cancel</router-link>
        </form>

    </div>
</template>


<script>
import axios from 'axios'

export default {
    props: ['uri'],
    data () {
        return {competition: {}}
    },
    created() {
        axios.get(this.uri)
        .then(response => {
            this.competition = response.data
        })
        .catch(e => {
            console.log(e)
        })
    },
    methods: {
        updateCompetition: function() {
            axios.patch(this.uri,
                        {name: this.competition.name,
                         result: this.competition.result,
                         external_url: this.competition.external_url
                         }
            )
            .then(response => {
                console.log("UPDATE competition successfull!!")
                this.$router.go(-1)
            })
            .catch(e => {
                alert("UPDATE competition failed")
                console.log(e)
            })
        }
    }
}
</script>
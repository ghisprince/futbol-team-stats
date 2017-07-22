<template id="opponent-edit">
    <div>
        <h2>Edit opponent</h2>
        <form v-on:submit="updateOpponent">

        <div class="form-group">
            <label for="edit-name">Name</label>
            <input class="form-control" id="edit-name" v-model="opponent.name" required/>

            <label for="edit-url">URL</label>
            <input class="form-control" id="edit-url" v-model="opponent.external_url"/>

        </div>

        <button type="submit" class="btn btn-primary">Save</button>
        <router-link class="btn btn-default" v-bind:to="'/opponent-list'">Cancel</router-link>
        </form>
    </div>
</template>


<script>
import axios from 'axios'

export default {
    props: ['uri'],
    data () {
        return {opponent: {}}
    },
    created() {
        axios.get(this.uri)
        .then(response => {
            this.opponent = response.data
        })
        .catch(e => {
            console.log(e)
        })
    },
    methods: {
        updateOpponent: function() {
            axios.patch(this.uri,
                        {name: this.opponent.name,
                         external_url: this.opponent.external_url
                        }

             )
            .then(response => {
                console.log("UPDATE Opponent successfull!!")
                this.$router.go(-1)
            })
            .catch(e => {
                console.log("UPDATE Opponent failed!!")
                console.log(e)
            })
        }
    }
}
</script>
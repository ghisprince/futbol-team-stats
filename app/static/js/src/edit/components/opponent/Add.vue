<template id="add-opponent">
    <div>
        <h2>Add new opponent</h2>
        <form v-on:submit="createOpponent">
        <div class="form-group">
            <label for="add-name">Name</label>
            <input class="form-control" id="add-name" v-model="opponent.name" required/>
            <label for="add-url">Url</label>
            <input type="url" class="form-control" id="add-url" v-model="opponent.url"/>
        </div>
        <button type="submit" class="btn btn-primary">Create</button>
        <router-link class="btn btn-default" v-bind:to="'/opponent-list'">Cancel</router-link>
        </form>
    </div>
</template>


<script>

import axios from 'axios'

export default {
    data () {
        return {opponent: {name: '', url: null}}
    },
    methods: {
        createOpponent: function() {
            axios.post(`/api/v1/opponents/`, this.opponent)
            .then(response => {
                this.opponent = response.data
                this.$router.go(-1)
            })
            .catch(e => {
                console.log(e)
            })
        }
    }
}

</script>
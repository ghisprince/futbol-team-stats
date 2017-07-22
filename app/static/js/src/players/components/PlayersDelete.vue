<template id="player-delete">
    <div>
        <h2>Delete player : {{ player.name }}</h2>
        <form v-on:submit="deletePlayer">
            <p>The action cannot be undone.</p>
            <button type="submit" class="btn btn-danger">Delete</button>
            <router-link class="btn btn-default" v-bind:to="'/'">Cancel</router-link>
        </form>
    </div>
</template>


<script>

import axios from 'axios'

export default {
    data () {
        return {player: {name: ''}}
    },
    created() {
        axios.get(`/api/v1/players/` + this.$route.params.player_id)
        .then(response => {
            this.player = response.data
        })
        .catch(e => {
            console.log(e)
        })
    },
    methods: {
        deletePlayer: function() {
            axios.delete(this.player._links.self)

            .then(response => {
                this.player = response.data
            })
            .catch(e => {
                console.log(e)
            })
        }
    }
}

</script>
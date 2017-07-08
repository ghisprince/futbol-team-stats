<template id="player-delete">
    <div>
        <h2>Delete player {{ player.name }}</h2>
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
        //return {player: findPlayer(this.$route.params.player_id)};
        return {player: {name: 'x', number: '10'}}
    },
    methods: {
        deletePlayer: function() {
            axios.delete(`/api/v1/players/` + this.$route.params.player_id)

            .then(response => {
                this.player = response.data
                console.log("PUT SUCCESS")
                console.log(this.player)
            })
            .catch(e => {
                alert(e)
                console.log(e)
            })
        }
    }
}

</script>
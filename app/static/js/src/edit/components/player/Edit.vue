<template id="player-edit">
    <div>
        <h2>Edit player</h2>
        <form v-on:submit="updatePlayer">

            <player :player.sync="player"></player>

            <button type="submit" class="btn btn-primary">Save</button>
            <router-link class="btn btn-default" v-bind:to="'/player-list'">Cancel</router-link>
        </form>
    </div>
</template>


<script>
import axios from 'axios'
import Player from './Player.vue'

export default {
    data () {
        return {player: {}}
    },
    components: {
        'player': Player
    },
    created() {
        axios.get(`/api/v1/players/` + this.$route.params.player_id + `?expand=true`)
        .then(response => {
            this.player = response.data
        })
        .catch(e => {
            console.log(e)
        })
    },
    methods: {
        updatePlayer: function() {
            axios.patch(this.player._links.self,
                        {name: this.player.name,
                         number: this.player.number,
                         active: this.player.active
                        }
            )
            .then(response => {
                console.log("UPDATE match successfull!")
                //this.$router.go(-1)
                this.$router.push({path: '/player-list'})
            })
            .catch(e => {
                alert("UPDATE match failed")
                console.log(e)
            })
        }
    }
}
</script>
<template id="player-add">
    <div>

        <h2>Add new player</h2>
        <form v-on:submit="createPlayer">

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
        return {player: {name: '',
                         number: null,
                         active: true,
                         team: {id: this.$root.current_team}
                         }
                }
    },
    components: {
        'player': Player
    },
    methods: {
        createPlayer: function() {
            axios.post(`/api/v1/players/`, this.player)
            .then(response => {
                this.player = response.data;
                this.$router.push({path: '/player-list'})
            })
        }
    }
}

</script>
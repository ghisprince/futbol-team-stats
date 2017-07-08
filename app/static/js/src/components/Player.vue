<template id="player">
    <div>
        <h2>{{ player.name }}</h2>
        <b>Number:</b>
        <div>{{ player.number}}</div>
        <br/>
        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/'">Back to player list</router-link>
    </div>
</template>


<script>
import axios from 'axios'

export default {
    data () {
        return {player: {name: 'x'}}
    },
    created() {
        axios.get(`/api/v1/players/` + this.$route.params.player_id)
        .then(response => {
            this.player = response.data
        })
        .catch(e => {
            console.log(e)
        })
    }
}

</script>
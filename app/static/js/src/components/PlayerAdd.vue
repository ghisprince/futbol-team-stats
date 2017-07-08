<template id="add-player">
    <div>
        <h2>Add new player</h2>
        <form v-on:submit="createPlayer">
        <div class="form-group">
            <label for="add-name">Name</label>
            <input class="form-control" id="add-name" v-model="player.name" required/>
        </div>
        <div class="form-group">
            <label for="add-number">Number</label>
            <input type="number" class="form-control" id="add-number" v-model="player.number"/>
        </div>
            <button type="submit" class="btn btn-primary">Create</button>
            <router-link class="btn btn-default" v-bind:to="'/'">Cancel</router-link>
        </form>
    </div>
</template>


<script>
import axios from 'axios'

export default {
    data () {
        return {player: {name: '', number: 0}}
    },
    methods: {
        createPlayer: function() {
            axios.post(`/api/v1/players/`, this.player)
            .then(response => {
                this.player = response.data
                console.log("CREATE PLAYER SUCCESSFULL")
                console.log(this.player)
            })
            .catch(e => {
                console.log("CREATE PLAYER FAILED")
                alert(e)
                console.log(e)
            })
        }
    }
}

</script>
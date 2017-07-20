<template id="player-edit">
    <div>
        <h2>Edit player</h2>
        <form v-on:submit="updatePlayer">
        <div class="form-group">
            <label for="edit-name">Name</label>
            <input class="form-control" id="edit-name" v-model="player.name" required/>
        </div>
        <div class="form-group">
            <label for="edit-number">Number</span></label>
            <input type="number" class="form-control" id="edit-number" v-model="player.number"/>
        </div>
            <button type="submit" class="btn btn-primary">Save</button>
            <router-link class="btn btn-default" v-bind:to="'/'">Cancel</router-link>
        </form>
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
    },
    methods: {
        updatePlayer: function() {
            axios.patch(`/api/v1/players/` + this.$route.params.player_id,
                        {'name': this.player.name,
                         'number': this.player.number,
                        }
             )
            .then(response => {
                this.player = response.data
            })
            .catch(e => {
                alert("UPDATE Player failed")
                console.log(e)
            })
        }
    }

}
</script>
<template id="opponent-edit">
    <div>
        <h2>Edit opponent</h2>
        <form v-on:submit="updateOpponent">

        <div class="form-group">
            <label for="edit-name">Name</label>
            <input class="form-control" id="edit-name" v-model="opponent.name" required/>
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
        return {opponent: {name: ''}}
    },
    created() {
        axios.get(`/api/v1/opponents/` + this.$route.params.opponent_id)
        .then(response => {
            this.opponent = response.data
        })
        .catch(e => {
            console.log(e)
        })
    },
    methods: {
        updateOpponent: function() {
            axios.patch(`/api/v1/opponents/` + this.$route.params.opponent_id,
                        {'name': this.opponent.name}
             )
            .then(response => {
                console.log("UPDATE Opponent successfull!!")
                this.opponent = response.data;
                this.$router.push('/');
            })
            .catch(e => {
                alert("UPDATE Opponent failed")
                console.log(e)
            })
        }
    }
}
</script>
<template id="add-opponent">
    <div>
        <h2>Add new opponent</h2>
        <form v-on:submit="createOpponent">

            <opponent :opponent.sync="opponent"></opponent>

            <button type="submit" class="btn btn-primary">Create</button>
            <router-link class="btn btn-default" v-bind:to="'/opponent-list'">Cancel</router-link>
        </form>
    </div>
</template>


<script>

import axios from 'axios'
import Opponent from './Opponent.vue'

export default {
    data () {
        return {opponent: {name: '',
                           external_url: null}}
    },
    components: {
        'opponent': Opponent
    },

    methods: {
        createOpponent: function() {
            axios.post(`/api/v1/opponents/`, this.opponent)
            .then(response => {
                this.opponent = response.data
                //this.$router.go(-1)
                this.$router.push({path: '/opponent-list'})
            })
            .catch(e => {
                console.log(e)
            })
        }
    }
}

</script>
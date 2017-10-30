<template id="opponent-edit">
    <div>
        <h2>Edit opponent</h2>
        <form v-on:submit="updateOpponent">

            <opponent :opponent.sync="opponent"></opponent>

            <button type="submit" class="btn btn-primary">Save</button>
            <router-link class="btn btn-default" v-bind:to="'/opponent-list'">Cancel</router-link>
        </form>
    </div>
</template>


<script>
import axios from 'axios'
import Opponent from './Opponent.vue'

export default {
    props: [],
    data () {
        return {opponent: {}}
    },
    components: {
        'opponent': Opponent
    },
    
    created() {
        axios.get(`/api/v1/opponents/` + this.$route.params.opponent_id + `?expand=true`)
        .then(response => {
            this.opponent = response.data
        })
        .catch(e => {
            console.log(e)
        })
    },
    methods: {
        updateOpponent: function() {
            axios.patch(this.opponent._links.self,
                        {name: this.opponent.name,
                         external_url: this.opponent.external_url
                        }

             )
            .then(response => {
                console.log("UPDATE Opponent successfull!!")
                //this.$router.go(-1)
                this.$router.push({path: '/opponent-list'})

            })
            .catch(e => {
                console.log("UPDATE Opponent failed!!")
                console.log(e)
            })
        }
    }
}
</script>
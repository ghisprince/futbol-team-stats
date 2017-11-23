<template id="playermatch-add">
    <div>
        <h2>Add player match</h2>

        <form v-on:submit="createPlayerMatch">
            <playermatch-props :playermatch.sync="playermatch"></playermatch-props>

            <button type="submit" class="btn btn-primary">Save</button>
            <a class="btn btn-default" v-on:click="goBack">
                Cancel
            </a>

        </form>

    </div>
</template>


<script>
import axios from 'axios'
import PlayerMatch from './PlayerMatch.vue'

export default {
    data () {
        return {playermatch:
                    {player: {name: ""},
                     match: {id: 0},
                     starter: false,
                     _links: ""
                    },
                players: []
               }
    },
    components: {
        'playermatch-props': PlayerMatch
    },
    methods: {
        goBack: function() {
            this.$router.go(-1)
        },
        createPlayerMatch: function() {
            axios.post(`/api/v1/playermatches/`,
                        {player: {id: this.playermatch.player.id},
                         match: {id: this.$route.params.match_id},
                         starter: this.playermatch.starter,
                         minutes: this.playermatch.minutes,
                         subbed_due_to_injury: this.playermatch.subbed_due_to_injury,
                         yellow_cards: this.playermatch.yellow_cards,
                         red_cards: this.playermatch.red_cards,
                         corners: this.playermatch.corners,
                         }

            )
            .then(response => {
                this.$router.go(-1)
            })
        }
    }
}
</script>

<style>


</style>
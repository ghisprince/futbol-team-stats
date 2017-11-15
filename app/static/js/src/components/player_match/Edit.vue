<template id="playermatch-edit">
    <div>

        <form v-on:submit="updatePlayerMatch">
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
        return {"playermatch":
                    {"player": {"name": ""},
                     "match": {"id": 0},
                     "_links": ""
                    },
                "players": [],
                "create": "zzz"
               }
    },
    components: {
        'playermatch-props': PlayerMatch
    },
    created() {
        axios.get(`/api/v1/playermatches/` + this.$route.params.playermatch_id + `?expand=true`)
        .then(response => {
            this.playermatch = response.data
        })
        .catch(e => {
            console.log(e)
        })

        axios.get(`/api/v1/players/?expand=true`)
        .then(response => {
            this.players = response.data
        })
        .catch(e => {
            console.log(e)
        })

    },
    methods: {
        goBack: function() {
            this.$router.go(-1)
        },
        updatePlayerMatch: function() {
            axios.patch(this.playermatch._links.self,
                        {player: {id: this.playermatch.player.id},
                         starter: this.playermatch.starter,
                         minutes: this.playermatch.minutes,
                         subbed_due_to_injury: this.playermatch.subbed_due_to_injury,
                         yellow_cards: this.playermatch.yellow_cards,
                         red_cards: this.playermatch.red_cards,
                         corners: this.playermatch.corners,
                         }

            )
            .then(response => {
                console.log("UPDATE playermatch successful!")
                this.$router.go(-1)
            })
            .catch(e => {
                alert("UPDATE playermatch failed")
                console.log(e)
            })
        },
        playerChanged: function(e) {
            for (var i=0; i < this.players.length; i++) {
                if (this.players[i].id == e.target.value) {
                 this.playermatch.player = this.players[i];
                 console.log(this.players[i].name);
                }
            }
            //this.$emit('opponentChanged', e.target.value);
        },

    }
}
</script>

<style>


</style>
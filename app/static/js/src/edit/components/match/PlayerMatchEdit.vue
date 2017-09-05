<template id="playermatch-edit">
    <div>
        <h2>Edit Player's match == {{ create }}</h2>


        <form v-on:submit="updatePlayerMatch">
            <div class="col-sm-3"></div>
            <div class="col-sm-9">

                <div class="form-group row">
                    <label for="edit-starter" class="col-sm-3 col-form-label">Player :</label>
                    <div class="col-sm-3">

                        <select class="form-control col-sm-4" v-on:change="playerChanged">
                            <option v-for="player in players"
                                    v-bind:value="player.id"
                                    :selected="player.name == playermatch.player.name"
                                    >
                                    {{player.name}}
                            </option>
                        </select>

                    </div>
                </div>

                <div class="form-group row">
                    <label for="edit-starter" class="col-sm-3 col-form-label">Starter :</label>
                    <div class="col-sm-3">
                        <input class="form-control"
                               type="checkbox"
                               v-model="playermatch.starter"
                               id="edit-starter">
                    </div>
                </div>

                <div class="form-group row">
                    <label for="edit-minutes" class="col-sm-3 col-form-label">Minutes Played :</label>
                    <div class="col-sm-3">
                        <input class="form-control"
                               type="number"
                               v-model="playermatch.minutes"
                               id="edit-minutes">
                    </div>
                </div>

                <div class="form-group row">
                    <label for="edit-subbed_due_to_injury" class="col-sm-3 col-form-label">Subbed Due To Injury :</label>
                    <div class="col-sm-3">
                        <input class="form-control"
                               type="checkbox"
                               v-model="playermatch.subbed_due_to_injury"
                               id="edit-subbed_due_to_injury">
                    </div>
                </div>

                <div class="form-group row">
                    <label for="edit-yellow_cards" class="col-sm-3 col-form-label">Yellow Cards :</label>
                    <div class="col-sm-3">
                        <input class="form-control"
                               type="checkbox"
                               v-model="playermatch.yellow_cards"
                               id="edit-yellow_cards">
                    </div>
                </div>

                <div class="form-group row">
                    <label for="edit-red_cards" class="col-sm-3 col-form-label">Red Cards :</label>
                    <div class="col-sm-3">
                        <input class="form-control"
                               type="checkbox"
                               v-model="playermatch.red_cards"
                               id="edit-red_cards">
                    </div>
                </div>

                <div class="form-group row">
                    <label for="edit-corners" class="col-sm-3 col-form-label">Corners :</label>
                    <div class="col-sm-3" >
                        <input class="form-control"
                               type="number"
                               v-model="playermatch.corners"
                               id="edit-corners">
                    </div>
                </div>

            </div>

            <div v-if="playermatch">
                <button type="submit" class="btn btn-primary">Save</button>
                <router-link class="btn btn-default"
                             v-bind:to="{name: 'match-edit', params: {match_id: playermatch.match.id, uri: playermatch._links.self}}">
                    Cancel
                </router-link>
            </div>

        </form>

    </div>
</template>


<script>
import axios from 'axios'

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
    components: {},
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
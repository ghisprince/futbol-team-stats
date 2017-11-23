<template id="playermatch-props">
    <div class="container-fluid">
        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-starter" class="col-sm-3 col-form-label">
                Player :
            </label>
            <div class="col-sm-4">
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
            <div class="col-sm-2"/>
            <label for="edit-starter" class="col-sm-3 col-form-label">
                Starter :
            </label>
            <div class="col-sm-4">
                <input class="form-control"
                       type="checkbox"
                       v-model="playermatch.starter"
                       id="edit-starter">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-minutes" class="col-sm-3 col-form-label">
                Minutes Played :
            </label>
            <div class="col-sm-4">
                <input class="form-control"
                       type="number"
                       v-model="playermatch.minutes"
                       id="edit-minutes">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-subbed_due_to_injury" class="col-sm-3 col-form-label">
                Subbed Due To Injury :
            </label>
            <div class="col-sm-4">
                <input class="form-control"
                       type="checkbox"
                       v-model="playermatch.subbed_due_to_injury"
                       id="edit-subbed_due_to_injury">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-yellow_cards" class="col-sm-3 col-form-label">
                Yellow Card :
            </label>
            <div class="col-sm-4">
                <input class="form-control"
                       type="checkbox"
                       v-model="playermatch.yellow_cards"
                       id="edit-yellow_cards">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-red_cards" class="col-sm-3 col-form-label">
                Red Card :
            </label>
            <div class="col-sm-4">
                <input class="form-control"
                       type="checkbox"
                       v-model="playermatch.red_cards"
                       id="edit-red_cards">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-corners" class="col-sm-3 col-form-label">
                Corners :
            </label>
            <div class="col-sm-4" >
                <input class="form-control"
                       type="number"
                       v-model="playermatch.corners"
                       id="edit-corners">
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'

export default {
    props: ['playermatch'],
    data () {
        return {
                players: [],
                selected_player: null};
    },
    created() {
        axios.get(`/api/v1/players/`)
        .then(response => {
            this.players = _.orderBy(response.data, "name");
            if (_.has(this.playermatch.player, 'id') == false) {
                this.playermatch.player = response.data[0];
            }
        })
    },
    methods: {
        playerChanged: function(e) {
            for (var i=0; i<this.players.length; i++) {
                if (this.players[i].id == e.target.value) {
                     this.playermatch.player = this.players[i];
                }
            }
        }
    }
}

</script>


<style>

</style>
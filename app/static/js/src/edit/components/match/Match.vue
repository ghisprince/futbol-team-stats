<template id="match-props">
    <div class="container-fluid">

        <div class="form-group row">
            <!-- //https://jsfiddle.net/3a2055ub/  -->

            <div class="col-sm-2"/>
            <label for="edit-date-time" class="col-sm-3 col-form-label">
                Date and time :
            </label>
            <div class="col-sm-4">
                <input class="form-control"
                       id="edit-date-time" v-model="match.date_time"
                       placeholder="2018-01-13T12:00:00"/>
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-opponent" class="col-sm-3 col-form-label">
                Opponent :
            </label>
            <div class="col-sm-4">
                <select class="form-control col-sm-4" v-on:change="opponentChanged">
                    <option v-for="opponent in opponents"
                            v-bind:value="opponent.id"
                            :selected="opponent.name == match.opponent.name"
                            >
                            {{opponent.name}}
                    </option>
                </select>
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-competition" class="col-sm-3 col-form-label">
                Competition :
            </label>
            <div class="col-sm-4">
                <select class="form-control col-sm-4" v-on:change="competitionChanged">
                    <option v-for="competition in competitions"
                            v-bind:value="competition.id"
                            :selected="competition.name == match.competition.name"
                            >
                            {{competition.name}}
                    </option>
                </select>
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-at-home" class="col-sm-3 col-form-label">Home Game :</label>
            <div class="col-sm-4">
                <input type="checkbox"
                       class="form-control col-sm-4"
                       id="edit-at-home"
                       v-model="match.at_home"/>
            </div>

        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    props: ['match'],
    data () {
        return {opponents: [],
                competitions: [],
                selected_opponent: null,
                selected_competition: null};
    },
    created() {
        axios.get(`/api/v1/opponents/`)
        .then(response => {
            this.opponents = response.data;
            if (_.has(this.match.opponent, 'id') == false) {
                this.match.opponent = response.data[0];
            }
        })
        axios.get(`/api/v1/competitions/`)
        .then(response => {
            this.competitions = response.data;
            if (_.has(this.match.competition, 'id') == false) {
                this.match.competition = response.data[0];
            }
        })

    },
    methods: {
        opponentChanged: function(e) {
            for (var i=0; i<this.opponents.length; i++) {
                if (this.opponents[i].id == e.target.value) {
                 this.match.opponent = this.opponents[i];
                 console.log(this.opponents[i].name);
                }
            }
            //this.$emit('opponentChanged', e.target.value);
        },

        competitionChanged: function(e) {
            for (var i=0; i<this.competitions.length; i++) {
                if (this.competitions[i].id == e.target.value) {
                     this.match.competition = this.competitions[i];
                     console.log(this.competitions[i].name);
                }
            }
        }
    }
}

</script>
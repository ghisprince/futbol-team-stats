<template id="match-props">
    <div>
        <div class="form-group">
            <!-- //https://jsfiddle.net/3a2055ub/  -->
            <label for="edit-date-time">Date and time</label>
            <input type="datetime-local" class="form-control"
                   id="edit-date-time" v-model="match.date_time"/>

            <label for="edit-opponent">Opponent</label>
            <select class="form-control" v-on:change="opponentChanged">
                <option v-for="opponent in opponents"
                        v-bind:value="opponent.id"
                        :selected="opponent.name == match.opponent.name"
                        >
                        {{opponent.name}}
                </option>
            </select>

            <label for="edit-competition">Competition</label>
            <select class="form-control" v-on:change="competitionChanged">
                <option v-for="competition in competitions"
                        v-bind:value="competition.id"
                        :selected="competition.name == match.competition.name"
                        >
                        {{competition.name}}
                </option>
            </select>

            <label for="edit-at-home">At Home</label>
            <input type="checkbox" class="form-control" id="edit-at-home" v-model="match.at_home"/>
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
                selected_opponent: null};
    },
    created() {
        axios.get(`/api/v1/opponents/`)
        .then(response => {
            this.opponents = response.data
        })
        axios.get(`/api/v1/competitions/`)
        .then(response => {
            this.competitions = response.data
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
            //this.$emit('competitionChanged', e.target.value);
            }
        }
}

</script>
<template id="opponent">
    <div>
        <h2>{{ opponent.name }}</h2>

        <div v-if="opponent.external_url">
            <a v-bind:href="opponent.external_url">Team's gotsoccer web site</a>
        </div>

        <p>Below are the team's results against this opponent </p>
        <table class="table">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Competition</th>
                    <th>Result</th>
                    <th>Goals</th>
                    <th>Goals against</th>
                    <th>Shots</th>
                    <th>Shots against</th>
                    <th>Match details</th>
                </tr>
            </thead>
            <tfoot>
                <tr>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                    <td>99</td>
                    <td>-</td>
                </tr>
            </tfoot>
            <tbody>
                <tr v-for="match in orderedMatches">
                    <td>
                        {{ match.date_time | formatDate }}
                    </td>
                    <td>
                        {{ match.competition.name }}
                    </td>
                    <td>
                        {{ match.result }}
                    </td>
                    <td>
                        {{ match.num_goals }}
                    </td>
                    <td>
                        {{ match.num_goals_against }}
                    </td>
                    <td>
                        {{ match.num_shots }}
                    </td>
                    <td>
                        {{ match.num_shots_against }}
                    </td>
                    <td>
                        -link-
                    </td>
                </tr>
            </tbody>
        </table>
        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/opponent-list'">Back to opponent list</router-link>
    </div>
</template>


<script>

import axios from 'axios'
import _ from 'lodash'

export default {
    props: ['uri'],
    data () {
        return {opponent: {name: ''}}
    },
    created() {
        // get opponent data
        axios.get(this.uri + `?expand=true`)
        .then(response => {
            this.opponent = response.data
        })
    },
    computed: {
        orderedMatches: function() {
            return _.orderBy(this.opponent.matches, 'date_time', 'desc')
        }
    }
}

</script>

<style>
</style>
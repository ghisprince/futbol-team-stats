<template id="opponent">
    <div>
        <h2>{{ opponent.name }}</h2>
        <p>Below are the team's results against this opponent </p>
        <table class="table">
            <thead>
                <tr>
                    <th>date</th>
                    <th>competition</th>
                    <th>result</th>
                    <th>goals</th>
                    <th>goals against</th>
                    <th>shots</th>
                    <th>goals against</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="match in orderedMatches">
                    <td align="left">
                        {{ match.date_time | formatDate }}
                    </td>
                    <td align="left">
                        {{ match.competition.name }}
                    </td>
                    <td align="left">
                        {{ match.result }}
                    </td>
                    <td align="left">
                        {{ match.num_goals }}
                    </td>
                    <td align="left">
                        {{ match.num_goals_against }}
                    </td>
                    <td align="left">
                        {{ match.num_shots }}
                    </td>
                    <td align="left">
                        {{ match.num_shots_against }}
                    </td>
                </tr>
            </tbody>
        </table>
        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/'">Back to opponent list</router-link>
    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'

export default {
    data () {
        return {opponent: {name: ''},
                matches: {}
                }
    },
    created() {
        // get opponent data
        axios.get(`/api/v1/opponents/` + this.$route.params.opponent_id + `?expand=true`)
        .then(response => {
            this.opponent = response.data
            this.matches = response.data['matches']
        })
    },
    computed: {
        orderedMatches: function() {
            return _.orderBy(this.matches, 'date_time', 'desc')
        }
    }
}

</script>
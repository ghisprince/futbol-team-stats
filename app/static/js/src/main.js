import Vue from 'vue'
import App from './App.vue'
import router from './router/index.js'
import moment from 'moment'
import Spinner from 'vue-simple-spinner'
import axios from 'axios'


new Vue({
    el: '#app-container',
    router,
    components: {
        Spinner
    },
    data: {
        "current_user": {"username": "Ghis"},
        "current_team": {"name": "Ghis Team"},
    },
    created() {
        // get match data
        axios.get(`/api/v1/user` )
        .then(response => {
            this.current_user = response.data;

            // hard coding currentTeam pending support for multiple
            axios.get(`/api/v1/teams/` + response.data.teams[0])
            .then(response => {
                    this.current_team = response.data;
            })
        })
    },
    render: h => h(App)
})

Vue.filter('formatDate', function(value) {
    if (value) {
        return moment.utc(String(value)).format('YYYY/MM/DD hh:mm a')
    }
})
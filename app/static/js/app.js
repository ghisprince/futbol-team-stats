

// register the grid component
Vue.component('demo-grid', {
  template: '#grid-template',
  props: {
    data: Array,
    columns: Array,
    filterKey: String
  },
  data: function () {
    var sortOrders = {}
    this.columns.forEach(function (key) {
      sortOrders[key] = 1
    })
    return {
      sortKey: '',
      sortOrders: sortOrders
    }
  },
  computed: {
    filteredData: function () {
      var sortKey = this.sortKey
      var filterKey = this.filterKey && this.filterKey.toLowerCase()
      var order = this.sortOrders[sortKey] || 1
      var data = this.data
      if (filterKey) {
        data = data.filter(function (row) {
          return Object.keys(row).some(function (key) {
            return String(row[key]).toLowerCase().indexOf(filterKey) > -1
          })
        })
      }
      if (sortKey) {
        data = data.slice().sort(function (a, b) {
          a = a[sortKey]
          b = b[sortKey]
          return (a === b ? 0 : a > b ? 1 : -1) * order
        })
      }
      return data
    }
  },
  filters: {
    capitalize: function (str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
    }
  },
  methods: {
    sortBy: function (key) {
      this.sortKey = key
      this.sortOrders[key] = this.sortOrders[key] * -1
    }
  }
})


var groupByPlayer = function(xs, key) {
  return xs.reduce(function(rv, x) {
    (rv[x['player']['name']] = rv[x['player']['name']] || []).push(x);
    return rv;
  }, {});
};


var sumList = function(arr, key) {
    var sum = 0;
    for (var i in arr){
        if (arr[i].hasOwnProperty(key)){
            sum += arr[i][key];
        }
    }
    return sum;
};


// bootstrap the demo
var playersAggView = new Vue({
  el: '#demo',
  data: {
    searchQuery: '',
    gridColumns: ['player', 'starter', 'minutes',
                  'goals', 'assists', 'shots'],
    gridData: []
  },
    created() {
        axios.get('/api/v1/playermatches/')
        .then(response => {

            var data = groupByPlayer(response.data, 'player');

            for (var i in data){
                console.log(i);
                var row = {};
                row['player'] = i;
                row['minutes'] = sumList(data[i], 'minutes');
                row['shots'] = sumList(data[i], 'num_shots');
                row['assists'] = sumList(data[i], 'num_assists');
                row['goals'] = sumList(data[i], 'num_goals');
                row['saves'] = sumList(data[i], 'num_saves');
                row['starter'] = sumList(data[i], 'starter');
                this.gridData.push(row);
            }
        })
        .catch(e => {
            console.log("Yo, failed to get matchList");
            console.log(e);
        });
    },
})

// bootstrap the demo
var matchesView = new Vue({
  el: '#demo2',
  data: {
    searchQuery: '',
    gridColumns: ['date', 'opponent', 'competition', 'result',
                  'goals for', 'goals against',
                  'shots for', 'shots against'],
    gridData: [
      {  }
    ]
  },
    created() {
        axios.get('/api/v1/matches/')
        .then(response => {
            this.gridData = response.data.map(function(obj){
                obj['date'] = obj['date_time'].slice(0,-9);
                obj['opponent'] = obj['opponent']['name'];
                obj['competition'] = obj['competition']['name'];
                obj['goals for'] = obj['num_goals'];
                obj['goals against'] = obj['num_goals_against'];
                obj['shots for'] = obj['num_shots'];
                obj['shots against'] = obj['num_shots_against'];
                return obj
            });
        })
        .catch(e => {
            console.log("Yo, failed to get matchList");
            console.log(e);
        });
    },

})

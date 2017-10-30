<template>
<div id="app-style">
    <router-view></router-view>
</div>
</template>

<script>
export default {
    name: 'app',
    components: {},
    data () {
        return {}
    }
}
</script>

<style>

#app-style {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}

td {
    text-align: left;
}

tfoot > tr > td {
    font-weight: bold;
}

#section{
    text-align: left;
}


label{
    text-align: left;
}


#sub-table-note{
    text-align: left;
    font-size:small;
    vertical-align: text-top;
    }


</style>
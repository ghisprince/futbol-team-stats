<template id="player-props">
    <div class="container-fluid">

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-name" class="col-sm-3 col-form-label">Name :</label>
            <div class="col-sm-4">
                <input class="form-control" id="edit-name" v-model="player.name" required/>
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-number" class="col-sm-3 col-form-label">Number :</label>

            <div class="col-sm-4">
                <input type="number" class="form-control" id="edit-number" v-model="player.number"/>
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-active" class="col-sm-3 col-form-label">Active :</label>
            <div class="col-sm-4">
                <input type="checkbox" class="form-control" id="edit-active" v-model="player.active"/>
            </div>

        </div>
    </div>
</template>


<script>

export default {
    props: ['player'],
    data () {
        return {};
    }
}

</script>
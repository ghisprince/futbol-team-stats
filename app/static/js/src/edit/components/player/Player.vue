<template id="player-props">
    <div>
        <div class="form-group">
            <label for="edit-name">Name</label>
            <input class="form-control" id="edit-name" v-model="player.name" required/>

            <label for="edit-number">Number</span></label>
            <input type="number" class="form-control" id="edit-number" v-model="player.number"/>
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
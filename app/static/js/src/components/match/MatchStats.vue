<template id="match-stats">
    <div class="container-fluid">


        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-opponent-corners" class="col-sm-3 col-form-label">
                Opponent Corners :
            </label>
            <div class="col-sm-2" >
                <input class="form-control"
                       type="number"
                       v-model="match_stats.opponent_corners"
                       id="edit-opponent-corners">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-opponent-yellow-cards" class="col-sm-3 col-form-label">
                Opponent Yellow Cards :
            </label>
            <div class="col-sm-2" >
                <input class="form-control"
                       type="number"
                       v-model="match_stats.opponent_yellow_cards"
                       id="edit-opponent-yellow-cards">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-opponent-red-cards" class="col-sm-3 col-form-label">
                Opponent Red Cards :
            </label>
            <div class="col-sm-2" >
                <input class="form-control"
                       type="number"
                       v-model="match_stats.opponent_red_cards"
                       id="edit-opponent-red-cards">
            </div>
        </div>


        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-opponent-fouls" class="col-sm-3 col-form-label">
                Opponent Fouls :
            </label>
            <div class="col-sm-2" >
                <input class="form-control"
                       type="number"
                       v-model="match_stats.opponent_fouls"
                       id="edit-opponent-fouls">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-passes" class="col-sm-3 col-form-label">
                Passes :
            </label>
            <div class="col-sm-2" >
                <input class="form-control"
                       type="number"
                       v-model="match_stats.passes"
                       id="edit-passes">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-pass_strings" class="col-sm-3 col-form-label">
                Pass Strings :
            </label>
            <div class="col-sm-2" >
                <input class="form-control"
                       type="number"
                       v-model="match_stats.pass_strings"
                       id="edit-pass_strings">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-pass_pct" class="col-sm-3 col-form-label">
                Pass % :
            </label>
            <div class="col-sm-2" >
                <input class="form-control"
                       type="number"
                       step="any"
                       v-model="match_stats.pass_pct"
                       id="edit-pass_pct">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-possession" class="col-sm-3 col-form-label">
                Possession :
            </label>
            <div class="col-sm-2" >
                <input class="form-control"
                       type="number"
                       v-model="match_stats.possession"
                       id="edit-possession">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-opponent-passes" class="col-sm-3 col-form-label">
                Opponent Passes :
            </label>
            <div class="col-sm-2" >
                <input class="form-control"
                       type="number"
                       v-model="match_stats.opponent_passes"
                       id="edit-opponent-passes">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-opponent-pass-strings" class="col-sm-3 col-form-label">
                Opponent Pass Strings :
            </label>
            <div class="col-sm-2" >
                <input class="form-control"
                       type="number"
                       v-model="match_stats.opponent_pass_strings"
                       id="edit-opponent-pass-strings">
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-opponent-pass-pct" class="col-sm-3 col-form-label">
                Opponent Pass % :
            </label>
            <div class="col-sm-2" >
                <input class="form-control"
                       type="number"
                       step="any"
                       v-model="match_stats.opponent_pass_pct"
                       id="edit-opponent-pass-pct">
            </div>
        </div>


    </div>
</template>

<script>

export default {
    props: ['match_stats'],
    data () {
        return {opponent_corners: null,
                opponent_yellow_cards: null,
                opponent_red_cards: null,
                opponent_fouls: null,

                passes: null,
                pass_strings: null,
                pass_pct: null,
                possession: null,

                opponent_passes: null,
                opponent_pass_strings: null,
                opponent_pass_pct: null

                }
    }
}

</script>
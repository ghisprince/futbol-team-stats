<template id="shot-graph">
    <div class="container">
        <h2 id="section">Shot data</h2>

        <div class="row">
            <div class="col-sm-6" id="convas-container">
                <canvas id="canvas" width=452 height=352></canvas>
                <p id="sub-table-note">
                    <i>Grey: not on goal, Blue: on goal, Red: scored.</i>
                </p>
            </div>

            <div class="col-sm-6">
                <div class="cliente">

                    <h4 style="text-decoration: underline">Shot details</h4>
                    <div v-if="selectedShot">
                        <form class="form-horizontal">

                            <div class="form-group">
                                <label for="shotPlayer" class="col-sm-4 control-label">
                                       Player :
                                </label>
                                <div class="col-sm-4">
                                    <select class="form-control" v-on:change="updateShotPlayerMatch">
                                        <option
                                            v-for="player_match in player_matches"
                                            v-bind:value="player_match.id"
                                            :selected="player_match.player.name == selectedShot.player_match.player.name"
                                            :disabled="enableEditing == 0"
                                            >
                                            {{ player_match.player.name }}
                                        </option>
                                     </select>
                                </div>
                            </div>

                            <div class="form-group" v-if="enableEditing">
                                <label for="byOpponent"
                                       class="col-sm-4 control-label">By Opponent :
                                </label>
                                <div class="col-sm-2">
                                    <input v-on:change="updateShotByOpponent"
                                           type="checkbox"
                                           class="form-control"
                                           id="shotByOpponent"
                                           v-model="selectedShot.by_opponent">
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="shotOnGoal"
                                       class="col-sm-4 control-label">On Goal :
                                </label>
                                <div class="col-sm-2">
                                    <input v-on:change="updateShotOnTarget"
                                           type="checkbox"
                                           class="form-control"
                                           id="shotOnGoal"
                                           v-model="selectedShot.on_target"
                                           :disabled="enableEditing == 0">
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="shotIsPk"
                                       class="col-sm-4 control-label">Penalty Kick :
                                </label>
                                <div class="col-sm-2">
                                    <input v-on:change="updateShotIsPK"
                                           type="checkbox"
                                           class="form-control"
                                           id="shotIsPk"
                                           v-model="selectedShot.pk"
                                           :disabled="enableEditing == 0">
                                </div>
                                <div class="col-sm-6"></div>
                            </div>


                            <div v-if="selectedShot.goal">
                                <h4 style="text-decoration: underline">Goal info</h4>

                                <div class="form-group" >
                                    <label for="goalTime"
                                           class="col-sm-4 control-label">Time :
                                    </label>
                                    <div class="col-sm-4">
                                        <input v-on:change="updateGoalTime"
                                               type="number disabled"
                                               class="form-control"
                                               id="goalTime"
                                               v-model="selectedShot.goal.time"
                                               :disabled="enableEditing == 0">
                                    </div>
                                    <a class="btn btn-danger" v-if="enableEditing" v-on:click="deleteGoal">
                                        <span class="glyphicon glyphicon-remove"></span> Goal
                                    </a>
                                </div>


                                <div class="form-group">
                                        <label for="assist"
                                               class="col-sm-4 control-label">Assist :
                                        </label>

                                    <div v-if="selectedShot.goal.assist">
                                        <a class="btn btn-danger" v-if="enableEditing" v-on:click="deleteAssist">
                                            <span class="glyphicon glyphicon-remove"></span> Assist
                                        </a>
                                        <div class="col-sm-4">
                                            <select class="form-control" v-on:change="updateAssist">
                                                <option
                                                    v-for="player_match in player_matches"
                                                    v-bind:value="player_match.id"
                                                    :selected="player_match.player.name == selectedShot.goal.assist.player_match.player.name"
                                                    :disabled="enableEditing == 0"
                                                    >
                                                    {{ player_match.player.name }}
                                                </option>
                                             </select>
                                        </div>


                                    </div>
                                    <div v-if="enableEditing && !selectedShot.goal.assist">
                                        <div class="col-sm-4"> - </div>
                                        <div>
                                            <a class="btn btn-success" v-on:click="addAssist">
                                                <span class="glyphicon glyphicon-plus"></span> Assist
                                            </a>
                                        </div>
                                    </div>
                                </div>


                            </div>
                            <div v-else-if="enableEditing">
                                <a class="btn btn-success" v-on:click="addGoal">
                                    <span class="glyphicon glyphicon-plus"></span> Goal
                                </a>
                            </div>

                        </form>
                        <hr>
                        <div v-if="enableEditing">
                            <a class="btn btn-danger" v-on:click="deleteShot">Delete Shot</a>
                        </div>
                    </div>
                    <div v-else-if="enableEditing">
                            Click on shot to modify <br/> or <br/>
                            <a class="btn btn-primary" v-on:click="addShot">Add a Shot</a><br/>
                    </div>
                    <div v-else="enableEditing">
                            Click on shot for details.
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<script>

import axios from 'axios'
import { fabric } from 'fabric'
import _ from 'lodash'


export default {
    props: {enableEditing: {default: false}
    },
    data () {
        return {
            shots: [],
            player_matches: [],
            circles: [],
            canvas: null,
            selectedShot: "",
            selectedShotIsModified: false
            }
    },
    ready (){
    },
    created() {
        //var parent = this; // delete this
        var by_opponent_arg = "&by_opponent=false";
        if (this.enableEditing) {
            by_opponent_arg = "";
        }
        axios.get(`/api/v1/shots/?match_id=` + this.$route.params.match_id
                                             + by_opponent_arg
                                             + `&expand=true`)
        .then(response => {
            this.shots = response.data;
            this.drawShotsOnCanvas()
        })
        axios.get(`/api/v1/playermatches/?match_id=` + this.$route.params.match_id + `&expand=true`)
        .then(response => {
            this.player_matches = _.orderBy(response.data, "player.name");
        })

    },
    mounted() {
        var parent = this;
        var canvas = new fabric.Canvas('canvas');

        canvas.selection = false; // disable group selection
        canvas.on('mouse:down', function(options) {
            if (options.target) {
                //console.log(' - id     : ' + options.target.shot.id);
                parent.selectedShot = options.target.shot.id;
                parent.selectedShot = JSON.parse(JSON.stringify(options.target.shot));

            }
            else {
                parent.selectedShot = "";
            }
        });
        this.canvas = canvas

    },
    computed: {
    },
    methods: {
        drawShotsOnCanvas: function(event){
            var parent = this;
            var canvas = this.canvas; // keeps adding to same canvas

            canvas.clear()
            for (var iii = 0; iii < this.shots.length; iii++) {
                var shot = this.shots[iii];

                var color = '';
                if (shot.scored) {
                    color = 'rgb(250,15,15)'; //red
                } else if (shot.on_target) {
                    color = 'rgb(15,100,200)'; //blue
                } else {
                    color = 'grey'; //grey
                }

                var stroke_color = 'rgb(5,5,5)';
                if (shot.by_opponent) {
                    stroke_color = 'rgb(240,240,240)';
                }

                var circle = new fabric.Circle({
                                    radius: 7,
                                    fill: color,
                                    opacity: 0.9,
                                    stroke: stroke_color,
                                    strokeWidth: 2,
                                    originX: 'center',
                                    originY: 'center',
                                    lockMovementX: this.enableEditing == false,
                                    lockMovementY: this.enableEditing == false
                                    })

                // use player's # to label shot, else use "?"
                try {
                    var player_number = shot.player_match.player.number.toString();
                }
                catch (err) {
                    var player_number = "?";
                }

                var text = new fabric.Text(player_number,
                                           {fontSize: 10,
                                            originX: 'center',
                                            originY: 'center'
                                           }
                );

                var group = new fabric.Group([circle, text],
                                             {hasControls: false,
                                              left: shot.x,
                                              top: shot.y,
                                              angle: 0
                                              }
                );

                group.toObject = (function(toObject) {
                  return function() {
                    return fabric.util.object.extend(toObject.call(this), {
                      shot: this.shot
                    });
                  };
                })(group.toObject);
                group.shot = shot

                group.on('modified', function(){
                    //console.log('moved ' + this.shot.player_match.player.name + '(' + this.left + ', ' + this.top + ')')
                    parent.selectedShot.x = this.left;
                    parent.selectedShot.y = this.top;
                    parent.selectedShotIsModified = true;
                    axios.patch(parent.selectedShot._links.self,
                                {x: this.left,
                                 y: this.top }
                    )
                    .then(response => {
                        parent.refreshShot(response.data._links.self);
                    })
                })
                canvas.add(group)
            }
            canvas.setBackgroundImage("static/assets/soccer-pitch.png",
                                      canvas.renderAll.bind(canvas),
                                      {backgroundImageOpacity: 0.5,
                                       backgroundImageStretch: false
                                      }
            );
        },
        refreshShot: function (uri){
            axios.get(uri + `?expand=true`)
            .then(response => {
                var shot = response.data;
                this.selectedShot = response.data;
                var index = _.findIndex(this.shots, {id: shot.id});
                this.shots.splice(index, 1, shot);
                this.drawShotsOnCanvas();
            })
        },
        addShot: function (event) {
            axios.post(`/api/v1/shots/`,
                    {by_opponent: false,
                     player_match:{id: this.player_matches[0].id}
                    }
            )
            .then(response => {
                var data = response.data;
                data['player_match'] = this.player_matches[0];
                this.shots.push(data);
                this.drawShotsOnCanvas()
            })
        },
        deleteShot: function (event) {
            // capture the seleected shot info
            var selectedShotUri = this.selectedShot._links.self
            var selectedShotId = this.selectedShot.id

            // clear selectedShot so control goes to default mode
            this.selectedShot = ""

            // delete the shot
            axios.delete(selectedShotUri)
            _.remove(this.shots, {id: selectedShotId})
            this.drawShotsOnCanvas()
        },
        updateShotOnTarget: function(e){
            axios.patch(this.selectedShot._links.self,
                    {on_target:e.target.checked}
            )
            .then(response => {
                this.refreshShot(this.selectedShot._links.self);
            })
        },
        updateShotByOpponent: function(e){
            axios.patch(this.selectedShot._links.self,
                    {by_opponent:e.target.checked}
            )
            .then(response => {
                this.refreshShot(this.selectedShot._links.self);
            })
        },
        updateShotIsPK: function(e){
            axios.patch(this.selectedShot._links.self,
                    {pk:e.target.checked}
            )
            .then(response => {
                this.refreshShot(this.selectedShot._links.self);
            })
        },
        updateShotPlayerMatch: function(e) {
            axios.patch(this.selectedShot._links.self,
                        {player_match: {id: e.target.value}}
            )
            .then(response => {
                this.refreshShot(this.selectedShot._links.self);
            })
        },
        addGoal: function(event){
            if (!this.selectedShot.on_target) {
                axios.patch(this.selectedShot._links.self,
                        {on_target:true}
                )
            }
            axios.post(`/api/v1/goals/`,
                    {shot:{id: this.selectedShot.id}}
            )
            .then(response => {
                this.refreshShot(this.selectedShot._links.self);
            })
        },
        deleteGoal: function(event){
            axios.delete(this.selectedShot.goal._links.self,
            )
            axios.patch(this.selectedShot._links.self,
                    {goal: null}
            )
            .then(response => {
                this.refreshShot(this.selectedShot._links.self);
            })
        },
        updateGoalTime: function(e) {
            if (e.type == "change") {
                axios.patch(this.selectedShot.goal._links.self,
                            {time: parseInt(e.target.value)}
                )
                .then(response => {
                    this.refreshShot(this.selectedShot._links.self);
                })
            }
        },
        addAssist: function(event){
            axios.post(`/api/v1/assists/`,
                    {goal: {id: this.selectedShot.goal.id},
                     player_match:{id: this.player_matches[0].id}
                     }
            )
            .then(response => {
                this.refreshShot(this.selectedShot._links.self);
            })

        },
        deleteAssist: function(event){
            axios.delete(this.selectedShot.goal.assist._links.self,
            )
            axios.patch(this.selectedShot._links.self,
                    {assist: null}
            )
            .then(response => {
                this.refreshShot(this.selectedShot._links.self);
            })

        },
        updateAssist: function(e) {
            axios.patch(this.selectedShot.goal.assist._links.self,
                        {player_match:{id: e.target.value}}
            )
            .then(response => {
                this.refreshShot(this.selectedShot._links.self);
            })
        }
    }
}

</script>


<style>

#canvas {
    padding: 0;
    margin: auto;
    display: block;
    width: 500px;
}

.cliente {
	margin-top:10px;
	border: #cdcdcd medium solid;
	border-radius: 10px;
	-moz-border-radius: 10px;
	-webkit-border-radius: 10px;
}

</style>
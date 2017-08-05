<template id="shot-graph">
    <div id="convas-container">
        <canvas id="canvas" width=500 height=400  ></canvas>
        <p>Shot id: {{ selectedShot }}</p>
        <button v-on:click="refreshCanvas">Refresh</button>
    </div>
</template>


<script>
import axios from 'axios'
import { fabric } from 'fabric'
import _ from 'lodash'

class ColoredCircle {
    constructor (pCanvas, pColor, pLeft, pTop) {
        this._canvas = pCanvas
        this._circle = new fabric.Circle({
            radius: 4,
            strokeWidth: 2,
            stroke: 'rgba(10,10,10,0.5)',
            transformMatrix: [ 2, 0, 0, 2, 0, 0 ],
            fill: pColor,
            left: pLeft,
            top: pTop,
            opacity: 1.0,
            selectable: true
        });
        this._color = pColor
        pCanvas.add(this._circle)
    }
    get color(){
        return this._color
    }
    set color(pColor){
        this._circle.set('fill', pColor);
        this._canvas.renderAll()
        return this._color
    }
}

export default {
    props: ["player_matches"],
    data () {
        return {
            shots: [],
            circles: [],
            canvas: null,
            selectedShot: -999
        }
    },
    ready (){
        console.log("READY");
        console.log("player_matches.length " + this.player_matches.length);
    },
    created() {
        console.log("CREATED");
        console.log("shots.length " + this.shots.length);
        axios.get(`http://127.0.0.1:5000/api/v1/shots/?match_id=` + this.$route.params.match_id + `&expand=true`)
        .then(response => {
            var shots = response.data;
            this.shots = shots

            console.log("LOOPING");
            console.log(shots.length);
            var canvas = this.canvas; // keeps adding to same canvas
            //canvas = new fabric.Canvas('canvas');
            var iii = 0;
            for (iii = 0; iii < this.shots.length; iii++) {
                var shot = this.shots[iii];
                var color = 'black';
                if (shot.scored) {
                    color = 'red';
                } else if (shot.on_goal) {
                    color = 'blue';
                } else {
                    color = 'grey';
                }

                //var circle = new ColoredCircle(canvas, color, shot.x, shot.y)
                var circle = new fabric.Circle({left: shot.x * 10,
                                                top: shot.y * 10,
                                                radius: 7,
                                                fill: color,
                                                hasControls: false,
                                                opacity: 0.9,
                                                stroke: 'rgba(10,10,10,0.5)',
                                                //transformMatrix: [ 0, 0, 0, 0, 0, 0 ],
                                                strokeWidth: 2
                                                })

                circle.toObject = (function(toObject) {
                  return function() {
                    return fabric.util.object.extend(toObject.call(this), {
                      shot: this.shot
                    });
                  };
                })(circle.toObject);
                circle.shot  = shot

                circle.on('modified', function(){
                    console.log('moved ' + this.shot.player_match.player.name)
                })
                canvas.add(circle)
            }

            this.canvas.renderAll()
        })
        console.log("player_matches.length " + this.player_matches.length);
        console.log("shots.length " + this.shots.length);
    },
    mounted() {
        console.log("MOUNTED");
        console.log("player_matches.length " + this.player_matches.length);
        var canvas = new fabric.Canvas('canvas');
        var parent = this;
        canvas.setBackgroundImage("static/assets/soccer-pitch.png");
        canvas.selection = false; // disable group selection
        //canvas.renderAll()
        canvas.on('mouse:down', function(options) {
            console.log(options.e.clientX, options.e.clientY);
            if (options.target) {
                console.log('Shot clicked ');
                console.log(' - id     : ' + options.target.shot.id);
                console.log(' - player : ' + options.target.shot.player_match.player.name);
                console.log(' - scored : ' + options.target.shot.scored);
                parent.selectedShot = options.target.shot.id;

            }
        });
        this.canvas = canvas


    },
    computed: {
        //console.log("shots.length " + this.shots.length);
        //refreshCanvas()
        //var circle = new ColoredCircle(canvas, 'blue', 60, 20)
        selectedShotData: function () {
            return _.find(this.shots, {id: this.selectedShot})
        }

    },
    methods: {
        refreshCanvas: function (event) {
            console.log("REFRESH CANVAS")
            console.log("player_matches.length " + this.player_matches.length);


        },
        refreshCanvas2: function (event) {
            alert("refreshCanvas2");
        },
        highlightShot: function (event) {
            //http://fabricjs.com/docs/fabric.Circle.html
            //circle.bringToFront
            //circle.transform(


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

</style>
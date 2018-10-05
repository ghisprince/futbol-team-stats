<template>
  <div class="container">
    SHOTS
    {{ _shots }}
    <canvas id="canvas" width=452 height=352></canvas>
    <p id="sub-table-note">
      <i>Grey: off target, Blue: on target, Red: scored.</i>
    </p>

  </div>
</template>

<script>

import { fabric } from 'fabric'

export default {
  props: [ 'shots' ],
  data () {
    return {
      canvas: null
    }
  },
  ready (){
  },
  created () {
    //this.drawShotsOnCanvas()
    //this._canvas = ""
  },
  mounted () {
    
    this.drawShotsOnCanvas()
  },
  computed: {
    _shots: function () {
      this.drawShotsOnCanvas()
      return this.shots
    }
  },
  methods: {
    drawShotsOnCanvas: function() {
      console.log("shots " + this.shots.length + " " + this._canvas)
      if (!this._canvas) {
        this._canvas = new fabric.Canvas('canvas');
      }
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
                  radius: 9,
                  fill: color,
                  opacity: 0.9,
                  stroke: stroke_color,
                  strokeWidth: 2,
                  originX: 'center',
                  originY: 'center'
                  })

        // use player's # to label shot, else use "?"
        try {
          var player_number = shot.player_match.player.number.toString();
        }
        catch (err) {
          var player_number = "?";
        }

        var text = new fabric.Text(player_number,
                       {fontSize: 12,
                      originX: 'center',
                      originY: 'center'
                       }
        );

        var group = new fabric.Group([circle, text],
                       {hasControls: false,
                        left: shot.x,
                        top: shot.y,
                        angle: 0,
                        lockMovementX: this.enableEditing == false,
                        lockMovementY: this.enableEditing == false
                        }
        );

        group.toObject = (function(toObject) {
          return function () {
          return fabric.util.object.extend(toObject.call(this), {
            shot: this.shot
          });
          };
        })(group.toObject);
        group.shot = shot

        group.on('modified', function(){
          //console.log('moved ' + this.shot.player_match.player.name + '(' + this.left + ', ' + this.top + ')')
          console.log("modified shot")
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
        this._canvas.add(group)
      }

      //this._canvas.setBackgroundImage("static/assets/soccer-pitch.png",
      //              this._canvas.renderAll.bind(this._canvas),
      //              {backgroundImageOpacity: 0.5,
      //               backgroundImageStretch: false
      //              }
      //);
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
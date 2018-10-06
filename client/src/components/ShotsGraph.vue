<template>
  <div>
    <svg id="shots-chart"></svg>
    <p>Grey: off target, Green on target, Red: scored.</p>
  </div>
</template>

<script>
import * as d3 from 'd3';
function handleMouseOver0 (d, i) {
  console.log(d)
  d3.select(this).attr({fill: "orange"})
}


export default {
  props: ['shots'],
  data () {
    return {
      _svg: "",
      width: 450,
      height: 700
    }
  },
  mounted: function() {
    this.$nextTick(this.load)
  },
  methods: {
    load () {
    let fieldLinesRects = [
      // top half
      {x: 10, y:20, width: 430, height: 330},
      {x: 100, y:20, width: 245, height: 100},
      {x: 170, y:20, width: 115, height: 30},

      // bottom half
      {x: 10, y:350, width: 430, height: 330},
      {x: 100, y:580, width: 245, height: 100},
      {x: 170, y:650, width: 115, height: 30},
      ]

    let shotFillColor = { off_target: "grey", 
                      on_target: "PaleGreen", 
                      scored: "red" }

    let shotStrokeColor = { by_opponent: "white", 
                        by_team: "black"}

    let svg  = d3.select('#shots-chart')
      .attr("width", this.width)
      .attr("height", this.height)
      .style("background-color", "DarkGreen")
      .style('border', '1px solid black')

    svg.selectAll('rect')
      .data(fieldLinesRects)
      .enter()
      .append('rect')
      .attr("x", function (d) { return d.x } )
      .attr("y", function (d) { return d.y })
      .attr("width", function (d) { return d.width })
      .attr("height", function (d) { return d.height })
      .attr('stroke', 'green')
      .attr('stroke-width', 3)
      .attr("fill", "transparent")

    let svgPoints = svg.selectAll("circleShot")
      .data(this.shots)
      .enter()
      .append("circle")

    let svgPointAtts = svgPoints
      .attr("class", "dot")
      .style("opacity", 0.75)
      .style("stroke", function (pt) { 
        return shotStrokeColor[pt.by_opponent ? 'by_opponent' : 'by_team']
      })
      .attr("fill", function(pt) {
        if (pt.scored) {
          return shotFillColor['scored']
        }
        return (shotFillColor[pt.on_target ? 'on_target' : 'off_target' ] )
      })
      .attr("cx", function(pt) { return pt.x })
      .attr("cy", function(pt) { return pt.y })
      .attr("r", 10)

      /*.attr("transform", function(d) { 
        return "translate(" + d + ")"; 
      })*/
      // a
      .on("mouseover", function(d, i) {
        d3.select(this)
          .attr("r", 20)
      })
      .on("mouseout", function(d,i) {
        d3.select(this)
          .attr("r", 10)
      })

    let svgPointsText = svg.selectAll("text")
      .data(this.shots)
      .enter()
      .append("text")

    let svgPointsTextAtts = svgPointsText
      .attr("x", function(pt) { return pt.x })
      .attr("y", function(pt) { return pt.y })
      .attr("text-anchor", "middle") // set anchor y justification
      .attr("dy", "5px")
      .text(function(pt) { return pt.player_number.toString() })

    // onclick
    svg.on("click",function () {
      let coords = d3.mouse(this)
      console.log(coords)
    }) 

    },
    handleMouseOver (d, i) {
      console.log("########")
      console.log(d)
      d3.select('circle')
        .attr({"fill": "orange"})
        .attr("r", 7)
    }
  },
  watch: {
    shots: function dataChanged(n, o) {
      console.log("changed")
      this.load()
    }
  },
  computed: {
    cshots: function () {
      var vertices = d3.range(100).map(function(d) {
        return [Math.random() * 500, Math.random() * 300];
      })
      return vertices
    }
  }
}
</script>
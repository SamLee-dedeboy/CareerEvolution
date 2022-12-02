<template>
  <div id="legend"></div>
</template>

<script>
    import * as d3 from "d3";

    export default {
        name: 'Legend',
        data() { // pass data to others
            return {
                
            }
        },
        props:{ // received data from others
        },
        watch: { 
        },
        mounted(){ 
            this.drawText("#legend");
        },
        methods: {
            drawText(id){

                let width = d3.select(id).node().getBoundingClientRect().width;
                let height = d3.select(id).node().getBoundingClientRect().height;

                d3.selectAll(".infotext").remove();
                let svg = d3.select(id).append("svg")
                    .attr("class", "infotext")
                    .attr("viewBox", [0, 0, width, height])
                    .attr("width", width)
                    .attr("height", height);

                const info_rect = svg.append('rect')
                    .attr('x', 0)
                    .attr('y', 0)
                    .attr('height', 20)
                    .attr('width', 20)
                    .attr('fill', "red");
            }
        }
    }

</script>


<style>

    #legend {
        width:  100%;
        height: 100%;
    }
</style>
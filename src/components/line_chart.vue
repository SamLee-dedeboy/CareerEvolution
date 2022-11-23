<template>
    <div id="lines"></div>
</template>

<script>
    import * as d3 from "d3";

    export default {
        name: 'LineChart',
        data() { // pass data to others
            return {
                prepared_data: undefined,
                colorScale: undefined
            }
        },
        props:{ // received data from others
            myData: Object,
        },
        watch: { 
            myData: function(newVal, oldVal) { // watch it
                // this.prepareData(this.myBarchartData, this.mySelection);
                // if (this.mySelection.id===1 || this.mySelection.id===2 || this.mySelection.id===3 || this.mySelection.id===4 || this.mySelection.id===5){
                //     console.log(this.mySelection.id, "bar");
                //     this.drawBarChart(this.prepared_data, "#bar", this.mySelection)
                // }
                // else{
                //     console.log(this.mySelection.id, "stacked");
                //     this.drawStackedBarChart(this.prepared_data, "#bar")
                // }
            },
        },
        mounted(){ // actually drawing
            console.log("In linechart: ", this.myData);
            // let localData = testData['data'];
            // this.prepareData(localData);
            // this.drawLineChart(localData, "#lines");
        },
        methods: {
            prepareData(data) {
                
            },
            drawLineChart(data, id) {

            }
        }
    }

</script>


<style>
    #bar {
        width:  100%;
        height: 100%;
    }
</style>
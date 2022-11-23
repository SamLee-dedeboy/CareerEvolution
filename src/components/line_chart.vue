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
            this.prepareData(this.myData);
            // this.drawLineChart(localData, "#lines");
        },
        methods: {
            prepareData(data) {
                let group_offset = {"0": 5, "1": 55, "2": 105, "3": 155, "4": 205, "5": 255};
                let group_counter = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0};

                // rank the initial order for all ppl.
                let ppl_order = [];
                Object.keys(data).forEach(key => {
                    let tmp = {
                        bin: data[key]['pop_bin'][0],
                        id: key
                    };
                    ppl_order.push(tmp)
                });
                ppl_order.sort(function(a, b){
                    if(a.bin < b.bin) { return -1; }
                    if(a.bin > b.bin) { return 1; }
                    return 0;
                });
                console.log(ppl_order);

                // create line coordinates for all ppl in the subset.
                let ppl_lines = [];
                ppl_order.forEach(ppl => {
                    let ppl_line = [];
                    let bin_used = {};
                    for (let idx=0; idx<data[ppl.id]['pop_bin'].length; idx++){
                        let ppl_year = {
                            id: ppl.id,
                            year: idx,
                            bin: group_offset[String(data[ppl.id]['pop_bin'][idx])] + 2*group_counter[String(data[ppl.id]['pop_bin'][idx])],
                        };
                        
                        bin_used[String(data[ppl.id]['pop_bin'][idx])] = "true";
                        ppl_line.push(ppl_year);
                    }
                    for (let idx=0; idx<=5; idx++){
                        if (idx in bin_used){
                            group_counter[idx] += 1;
                        }
                    }
                    ppl_lines.push(ppl_line);
                });
                console.log(ppl_lines);
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
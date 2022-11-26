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
                colorScale: undefined,
                data_years: undefined,
                plateau_length: 0.5,
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
            this.drawLineChart(this.prepared_data, "#lines");
        },
        methods: {
            prepareData(data) {
                let group_offset = {"0": 5, "1": 55, "2": 105, "3": 155, "4": 205, "5": 255};
                let group_counter = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0};

                // rank the initial order for all ppl.
                let ppl_order = [];
                Object.keys(data).forEach(key => {
                    this.data_years = data[key]['pop_bin'].length;
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
                        let ppl_year_pre = {
                            id: ppl.id,
                            year: idx,
                            bin: group_offset[String(data[ppl.id]['pop_bin'][idx])] + 2*group_counter[String(data[ppl.id]['pop_bin'][idx])],
                        };
                        let ppl_year_next = {
                            id: ppl.id,
                            year: idx + this.plateau_length,
                            bin: group_offset[String(data[ppl.id]['pop_bin'][idx])] + 2*group_counter[String(data[ppl.id]['pop_bin'][idx])],
                        };
                        
                        bin_used[String(data[ppl.id]['pop_bin'][idx])] = "true";
                        ppl_line.push(ppl_year_pre);
                        ppl_line.push(ppl_year_next);
                    }
                    for (let idx=0; idx<=5; idx++){
                        if (idx in bin_used){
                            group_counter[idx] += 1;
                        }
                    }
                    ppl_lines.push(ppl_line);
                });
                console.log(ppl_lines);
                this.prepared_data = ppl_lines;
            },

            drawLineChart(data, id) {
                const margin = {left: 10, right: 10, top: 10, bottom: 10};
                const width = 1000;
                const height = 700;

                const xRange = [margin.left, width - margin.right];
                const yRange = [margin.top, height - margin.bottom];

                const xScale = d3.scaleLinear([0, this.data_years-1 + this.plateau_length], xRange);
                const yScale = d3.scaleLinear([305, 5], yRange);

                const xAxis = d3.axisBottom(xScale).ticks(width / 100).tickSizeOuter(0);
                const yAxis = d3.axisLeft(yScale).ticks(height / 50);

                d3.selectAll(".linechart").remove();
                let svg = d3.select(id).append("svg")
                    .attr("class", "linechart")
                    .attr("viewBox", [0, 0, width, height])
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom);
                
                // add rects for popilarity groups background.
                const rect_0 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(55))
                    .attr('height', height/6)
                    .attr('width', width)
                    .attr("fill", "#FFE5CC");
                const rect_1 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(105))
                    .attr('height', height/6)
                    .attr('width', width)
                    .attr("fill", "#FFFFCC");
                const rect_2 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(155))
                    .attr('height', height/6)
                    .attr('width', width)
                    .attr("fill", "#E5FFCC");
                const rect_3 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(205))
                    .attr('height', height/6)
                    .attr('width', width)
                    .attr("fill", "#CCFFFF");
                const rect_4 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(255))
                    .attr('height', height/6)
                    .attr('width', width)
                    .attr("fill", "#CCCCFF");
                const rect_5 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(305))
                    .attr('height', height/6)
                    .attr('width', width)
                    .attr("fill", "#FFCCE5");

                data.forEach(chartData => {
                    const X = d3.map(chartData, d => d.year);
                    const Y = d3.map(chartData, d => d.bin);
                    const I = d3.range(X.length);

                    // Construct a line generator.
                    const line = d3.line()
                        .x(i => xScale(X[i]))
                        .y(i => yScale(Y[i]));
                    
                    // draw line for movie.
                    const lines = svg.append('path')
                        .attr('fill', 'none')
                        .attr('stroke', "steelblue")
                        .attr('stroke-width', 1.5)
                        .attr('d', line(I))
                        .attr('index', i => i)
                        .on('mouseover', function (d){
                            d3.select(this).raise();
                            d3.select(this).transition()
                                .duration('50')
                                .attr('stroke-width', 3)
                                .attr('stroke', 'red')
                        })
                        .on('mouseout', function (d, i){
                            d3.select(this).transition()
                                .duration('50')
                                .attr('stroke-width', 1.5)
                                .attr('stroke', 'steelblue')
                        });
                });
                
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
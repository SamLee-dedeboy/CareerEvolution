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
                selected_actor: undefined,
                if_selected: false,
                selected_color: undefined
            }
        },
        props:{ // received data from others
            myData: Object,
            mySubsetName: String
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
                        id: key,
                        name: data[key]['name'],
                        role: data[key]['role'],
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
                            name: ppl.name,
                            bin: group_offset[String(data[ppl.id]['pop_bin'][idx])] + 2*group_counter[String(data[ppl.id]['pop_bin'][idx])],
                            m_name: data[ppl.id]['movie_name'][idx],
                        };
                        if (ppl.role == "actor")    ppl_year_pre.role = 0;
                        else if (ppl.role == "director")    ppl_year_pre.role = 1;
                        else if (ppl.role == "writer")    ppl_year_pre.role = 2;
                        else if (ppl.role == "producer")    ppl_year_pre.role = 3;

                        let ppl_year_next = {
                            id: ppl.id,
                            year: idx + this.plateau_length,
                            name: ppl.name,
                            bin: group_offset[String(data[ppl.id]['pop_bin'][idx])] + 2*group_counter[String(data[ppl.id]['pop_bin'][idx])],
                            m_name: data[ppl.id]['movie_name'][idx]
                        };
                        if (ppl.role == "actor")    ppl_year_next.role = 0;
                        else if (ppl.role == "director")    ppl_year_next.role = 1;
                        else if (ppl.role == "writer")    ppl_year_next.role = 2;
                        else if (ppl.role == "producer")    ppl_year_next.role = 3;
                        
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
                const parent_this = this;

                const margin = {left: 15, right: 150, top: 50, bottom: 100};
                const width = 1000;
                const height = 700;

                const xRange = [margin.left, width - margin.right];
                const yRange = [margin.top, height - margin.bottom];

                const xScale = d3.scaleLinear([0, this.data_years-1 + this.plateau_length], xRange);
                const yScale = d3.scaleLinear([305, 5], yRange);

                const xAxis = d3.axisBottom(xScale).ticks(width / 100).tickSizeOuter(0);
                const yAxis = d3.axisLeft(yScale).ticks(height / 1);

                d3.selectAll(".linechart").remove();
                let svg = d3.select(id).append("svg")
                    .attr("class", "linechart")
                    .attr("viewBox", [0, 0, width, height])
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom);
                
                svg.append("text")
                    .attr("x", margin.left + width/2)
                    .attr("y", margin.top-5)
                    .text("Lord of the Ring Cast Career Evolution")
                    .style("font-size", "30px")
                    .attr("font-weight", "bold")
                    .attr("text-anchor", "middle")
                    .style('fill', 'steelblue');

                // add rects for popilarity groups background.
                const rect_0 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(55))
                    .attr('height', height/6)
                    .attr('width', width - margin.left)
                    .attr("fill", "#FFE5CC");
                const rect_1 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(105))
                    .attr('height', height/6)
                    .attr('width', width - margin.left)
                    .attr("fill", "#FFFF99");
                const rect_2 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(155))
                    .attr('height', height/6)
                    .attr('width', width - margin.left)
                    .attr("fill", "#FFCC99");
                const rect_3 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(205))
                    .attr('height', height/6)
                    .attr('width', width - margin.left)
                    .attr("fill", "#CCFFFF");
                const rect_4 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(255))
                    .attr('height', height/6)
                    .attr('width', width - margin.left)
                    .attr("fill", "#CCCCFF");
                const rect_5 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(305))
                    .attr('height', height/6)
                    .attr('width', width - margin.left)
                    .attr("fill", "#FFCCE5");

                data.forEach(chartData => {
                    const X = d3.map(chartData, d => d.year);
                    const Y = d3.map(chartData, d => d.bin);
                    const I = d3.range(X.length);
                    const N = d3.map(chartData, d => d.name);
                    const M = d3.map(chartData, d => d.m_name);
                    const C = d3.map(chartData, d => d.role);
                    // [actor: blue, director: green, writer: purple, producer: brown]
                    const colors = ["steelblue", "#4C9900", "#990099", "#999900"]; 

                    // Construct a line generator.
                    const line = d3.line()
                        .x(i => xScale(X[i]))
                        .y(i => yScale(Y[i]));
                    
                    function movies(indices) {
                        let movie_names = [];
                        let display_handler = true;
                        let offset = 8;
                        for (let m_idx=0; m_idx<indices; m_idx++){
                            if (M[m_idx] == 0.0) continue;
                            else if (X[m_idx]%1 != 0) continue;
                            let movie_tmp = {
                                x: xScale(X[m_idx]),
                                y: yScale(Y[m_idx]),
                                m_name: M[m_idx]
                            };
                            if (display_handler){
                                if (offset == 8)    offset -= 8;
                                else    offset = 8;
                                movie_tmp.y += 11;
                                movie_tmp.y += offset;
                            }    
                            else {
                                movie_tmp.y -= 2;
                                movie_tmp.y -= offset;
                            }    
                            display_handler = !display_handler;
                            movie_names.push(movie_tmp);
                        }
                        return movie_names;
                    }
                    const text_actor = movies(X.length);
                    
                    // draw line for movie.
                    const lines = svg.append('path')
                        .attr('fill', 'none')
                        .attr('stroke', colors[C[0]])
                        .attr('stroke-width', 1.5)
                        .attr('d', line(I))
                        .attr('name', N[0])
                        .attr("class", "all_lines")
                        .on('mouseover', function (d){
                            if (parent_this.if_selected == false){
                                parent_this.selected_color = this.getAttribute("stroke");
                                d3.select(this).raise();
                                d3.select(this).transition()
                                    .duration('0')
                                    .attr('stroke-width', 3)
                                    .attr('stroke', 'red');
                                
                                svg.append("text")
                                    .attr("class", "click_line")
                                    .attr("x", margin.left + 5)
                                    .attr("y", margin.top + 20)
                                    .text(this.getAttribute('name'))
                                    .style("font-size", "20px")
                                    .attr("font-weight", "bold")
                                    .style('fill', 'red');
                            }
                            else;
                        })
                        .on('mouseout', function (d, i){
                            // console.log(parent_this.if_selected);
                            if (parent_this.if_selected == false) {
                                d3.selectAll(".click_line").remove();
                                d3.select(this).transition()
                                    .duration('0')
                                    .attr('stroke-width', 1.5)
                                    .attr("stroke", parent_this.selected_color);
                            }
                            else;
                        })
                        .on('click', function (d){
                            if (parent_this.if_selected == false){
                                parent_this.if_selected = true;
                                d3.selectAll(".all_lines").transition()
                                    .duration('50')
                                    .attr('opacity', '0.1');
                                
                                d3.select(this).raise();
                                d3.select(this).transition()
                                    .duration('50')
                                    .attr('stroke-width', 3)
                                    .attr('stroke', 'red')
                                    .attr('opacity', '1');
                                
                                svg.append("text")
                                    .attr("class", "click_line")
                                    .attr("x", margin.left + 5)
                                    .attr("y", margin.top + 20)
                                    .text(this.getAttribute('name'))
                                    .style("font-size", "20px")
                                    .attr("font-weight", "bold")
                                    .style('fill', 'red');

                                for (let text_idx=0; text_idx<text_actor.length; text_idx++){
                                    let text_tmp = text_actor[text_idx];
                                    const texts = svg.append('text')
                                        .attr("class", "click_line")
                                        .attr("x", text_tmp.x)
                                        .attr("y", text_tmp.y)
                                        .text(text_tmp.m_name)
                                        .style("font-size", "9px")
                                        .attr("font-weight", "bold")
                                        .style('fill', 'red');
                                }
                            }
                            else {
                                parent_this.if_selected = false;
                                d3.selectAll(this).transition()
                                    .duration('50')
                                    .attr("stroke", parent_this.selected_color);
                                d3.selectAll(".all_lines").transition()
                                    .duration('50')
                                    .attr('opacity', '1');
                            }
                        });
                    
                        function clickLine(x, y) {
                            // d3.selectAll(".click_line").remove();
                            // svg.append("text")
                            //     .attr("class", "click_line")
                            //     .attr("x", margin.left + 300)
                            //     .attr("y", height -15)
                            //     .text("80-100")
                            //     .style("font-size", "9px")
                            //     .attr("alignment-baseline","middle")
                        }
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
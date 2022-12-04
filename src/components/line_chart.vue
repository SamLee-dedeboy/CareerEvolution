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
                selected_actor: {},
                if_selected: false,
                selected_color: undefined,
            }
        },
        props:{ // received data from others
            myData: Object,
            mySubsetName: String
        },
        watch: { 
            myData: function(newVal, oldVal) { // watch it
                this.if_selected = false;
                this.prepareData(this.myData);
                this.drawLineChart(this.prepared_data, "#lines");
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
                        roles: data[key]['roles'],
                        img: data[key]['img']
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
                            role_name: ppl.role,
                            roles: ppl.roles,
                            img:ppl.img
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
                            m_name: data[ppl.id]['movie_name'][idx],
                            role_name: ppl.role,
                            roles: ppl.roles,
                            img:ppl.img
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

                const margin = {left: 100, right: 150, top: 35, bottom: 100};
                // let width  = d3.select(id).node().getBoundingClientRect().width;
                // let height = d3.select(id).node().getBoundingClientRect().height;
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
                    .text(this.mySubsetName + " Cast Career Evolution")
                    .style("font-size", "30px")
                    .attr("font-weight", "bold")
                    .attr("text-anchor", "middle")
                    .style('fill', 'steelblue');

                // add rects for popilarity groups background.
                const rect_0 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(55))
                    .attr('height', (height - margin.top - margin.bottom)/6)
                    .attr('width', width - margin.left)
                    .attr("fill", "#FEF0D5");
                const rect_1 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(105))
                    .attr('height', (height - margin.top - margin.bottom)/6)
                    .attr('width', width - margin.left)
                    .attr("fill", "#FDE1AC");
                const rect_2 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(155))
                    .attr('height', (height - margin.top - margin.bottom)/6)
                    .attr('width', width - margin.left)
                    .attr("fill", "#FCD382");
                const rect_3 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(205))
                    .attr('height', (height - margin.top - margin.bottom)/6)
                    .attr('width', width - margin.left)
                    .attr("fill", "#FBC459");
                const rect_4 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(255))
                    .attr('height', (height - margin.top - margin.bottom)/6)
                    .attr('width', width - margin.left)
                    .attr("fill", "#FAB52F");
                const rect_5 = svg.append("rect")
                    .attr('x', xScale(0))
                    .attr('y', yScale(305))
                    .attr('height', (height - margin.top - margin.bottom)/6)
                    .attr('width', width - margin.left)
                    .attr("fill", "#F9A706");

                let ppl_count = 0;
                data.forEach(chartData => {
                    const X = d3.map(chartData, d => d.year);
                    const Y = d3.map(chartData, d => d.bin);
                    const I = d3.range(X.length);
                    const N = d3.map(chartData, d => d.name);
                    const M = d3.map(chartData, d => d.m_name);
                    const C = d3.map(chartData, d => d.role);
                    const R = d3.map(chartData, d => d.role_name);
                    const Rs = d3.map(chartData, d => d.roles);
                    const D = d3.map(chartData, d => d.id);
                    const P = d3.map(chartData, d => d.img);
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
                        .attr('id', D[0])
                        .attr('role', R[0])
                        .attr('roles', Rs[0])
                        .attr('actor_id', D[0])
                        .attr("class", "all_lines")
                        .attr("count", String(ppl_count))
                        .on('mouseover', function (d){
                            if (parent_this.if_selected == false){
                                parent_this.selected_color = this.getAttribute("stroke");
                                d3.select("#count_"+this.getAttribute("count")).transition()
                                    .duration('0')
                                    .attr('opacity', '1');
                                d3.selectAll(".all_lines").transition()
                                    .duration('0')
                                    .attr('opacity', '0.5');
                                d3.select(this).raise();
                                d3.select(this).transition()
                                    .duration('0')
                                    .attr('stroke-width', 3)
                                    .attr('opacity', '1');
                                    // .attr('stroke', 'red');
                                
                                svg.append("text")
                                    .attr("class", "click_line")
                                    .attr("x", margin.left + 5)
                                    .attr("y", margin.top + 20)
                                    .text(this.getAttribute('name') + " (" + this.getAttribute('roles') + ")")
                                    .style("font-size", "20px")
                                    .attr("font-weight", "bold")
                                    .style('fill', this.getAttribute("stroke"));
                                    // .style('fill', 'red');
                            }
                            else;
                        })
                        .on('mouseout', function (d, i){
                            // console.log(parent_this.if_selected);
                            if (parent_this.if_selected == false) {
                                d3.select("#count_"+this.getAttribute("count")).transition()
                                    .duration('0')
                                    .attr('opacity', '0.3');
                                d3.selectAll(".all_lines").transition()
                                    .duration('0')
                                    .attr('opacity', '1');
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
                                parent_this.selected_actor = {
                                    id: this.getAttribute('actor_id'),
                                    name: this.getAttribute('name')
                                };
                                parent_this.$emit('selectedChange', parent_this.selected_actor);
                                d3.selectAll(".all_lines").transition()
                                    .duration('50')
                                    .attr('opacity', '0.1');
                                
                                d3.select(this).raise();
                                d3.select(this).transition()
                                    .duration('50')
                                    .attr('stroke-width', 3)
                                    .attr('opacity', '1');
                                    // .attr('stroke', 'red')
                                
                                if (P[0] != 0) {
                                    svg.append("image")
                                        .attr("class", "actor_img")
                                        .attr('x', 0)
                                        .attr('y', 0)
                                        .attr('width', 50)
                                        .attr('height', 50)
                                        .attr("xlink:href", P[0])
                                }
                                
                                svg.append("text")
                                    .attr("class", "click_line")
                                    .attr("x", margin.left + 5)
                                    .attr("y", margin.top + 20)
                                    .text(this.getAttribute('name'))
                                    .style("font-size", "20px")
                                    .attr("font-weight", "bold")
                                    .style('fill', parent_this.selected_color);
                                    // .style('fill', 'red');

                                for (let text_idx=0; text_idx<text_actor.length; text_idx++){
                                    let text_tmp = text_actor[text_idx];
                                    const texts = svg.append('text')
                                        .attr("class", "click_line")
                                        .attr("x", text_tmp.x)
                                        .attr("y", text_tmp.y)
                                        .text(text_tmp.m_name)
                                        .style("font-size", "9px")
                                        .attr("font-weight", "bold")
                                        .style('fill', parent_this.selected_color);
                                        // .style('fill', 'red');
                                }
                            }
                            else {
                                parent_this.if_selected = false;
                                parent_this.selected_actor = {};
                                parent_this.$emit('selectedChange', parent_this.selected_actor);
                                d3.selectAll(this).transition()
                                    .duration('50')
                                    .attr("stroke", parent_this.selected_color);
                                d3.selectAll(".all_lines").transition()
                                    .duration('50')
                                    .attr('opacity', '1');
                                d3.selectAll(".actor_img").remove();
                                
                            }
                        });
                    
                    svg.append("text")
                        .attr("x", 2)
                        .attr("y", height - margin.bottom - ppl_count*(height - margin.bottom - margin.top)/Object.keys(this.myData).length)
                        .text(N[0])
                        .style("font-size", "10px")
                        .attr("font-weight", "bold")
                        .style('fill', colors[C[0]])
                        .attr('color', colors[C[0]])
                        .attr('opacity', '0.3')
                        .attr('name', N[0])
                        .attr('roles', Rs[0])
                        .attr('actor_id', D[0])
                        .attr('id', "count_"+String(ppl_count))
                        .on('mouseover', function(d){
                            if (parent_this.if_selected == false){
                                parent_this.selected_color = this.getAttribute("color");
                                d3.selectAll(".all_lines").transition()
                                    .duration('0')
                                    .attr('opacity', '0.5');
                                d3.select(this).transition()
                                    .duration('0')
                                    .attr('opacity', '1');
                                // highlight the line
                                d3.select("#"+D[0]).raise();
                                d3.select("#"+D[0]).transition()
                                    .duration('0')
                                    .attr('stroke-width', 3)
                                    .attr('opacity', '1');
                                    // .attr('stroke', 'red');
                                
                                svg.append("text")
                                    .attr("class", "click_line")
                                    .attr("x", margin.left + 5)
                                    .attr("y", margin.top + 20)
                                    .text(this.getAttribute('name') + " (" + this.getAttribute('roles') + ")")
                                    .style("font-size", "20px")
                                    .attr("font-weight", "bold")
                                    .style('fill', this.getAttribute("color"));
                            }
                            else;
                        })
                        .on('mouseout', function(d, i){
                            if (parent_this.if_selected == false) {
                                d3.selectAll(".all_lines").transition()
                                    .duration('0')
                                    .attr('opacity', '1');
                                d3.select(this).transition()
                                    .duration('0')
                                    .attr('opacity', '0.3');

                                d3.selectAll(".click_line").remove();
                                d3.select("#"+D[0]).transition()
                                    .duration('0')
                                    .attr('stroke-width', 1.5)
                                    .attr("stroke", parent_this.selected_color);
                            }
                            else;
                        })
                        .on('click', function (d){
                            if (parent_this.if_selected == false){
                                parent_this.if_selected = true;
                                parent_this.selected_actor = {
                                    id: this.getAttribute('actor_id'),
                                    name: this.getAttribute('name')
                                };
                                parent_this.$emit('selectedChange', parent_this.selected_actor);
                                d3.selectAll(".all_lines").transition()
                                    .duration('50')
                                    .attr('opacity', '0.1');
                                
                                d3.select("#"+D[0]).raise();
                                d3.select("#"+D[0]).transition()
                                    .duration('50')
                                    .attr('stroke-width', 3)
                                    .attr('opacity', '1');
                                    // .attr('stroke', 'red')
                                
                                if (P[0] != 0) {
                                    svg.append("image")
                                        .attr("class", "actor_img")
                                        .attr('x', 0)
                                        .attr('y', 0)
                                        .attr('width', 50)
                                        .attr('height', 50)
                                        .attr("xlink:href", P[0])
                                }
                                
                                svg.append("text")
                                    .attr("class", "click_line")
                                    .attr("x", margin.left + 5)
                                    .attr("y", margin.top + 20)
                                    .text(this.getAttribute('name'))
                                    .style("font-size", "20px")
                                    .attr("font-weight", "bold")
                                    .style('fill', parent_this.selected_color);

                                for (let text_idx=0; text_idx<text_actor.length; text_idx++){
                                    let text_tmp = text_actor[text_idx];
                                    const texts = svg.append('text')
                                        .attr("class", "click_line")
                                        .attr("x", text_tmp.x)
                                        .attr("y", text_tmp.y)
                                        .text(text_tmp.m_name)
                                        .style("font-size", "9px")
                                        .attr("font-weight", "bold")
                                        .style('fill', parent_this.selected_color);
                                }
                            }
                            else {
                                parent_this.if_selected = false;
                                parent_this.selected_actor = {};
                                parent_this.$emit('selectedChange', parent_this.selected_actor);
                                d3.selectAll("#"+D[0]).transition()
                                    .duration('50')
                                    .attr("stroke", parent_this.selected_color);
                                d3.selectAll(".all_lines").transition()
                                    .duration('50')
                                    .attr('opacity', '1');
                                d3.selectAll(".actor_img").remove();
                            }
                        });
                    ppl_count += 1;

                });
            },
        }
    }

</script>


<style>
    #lines {
        width:  100%;
        height: 100%;
    }
</style>
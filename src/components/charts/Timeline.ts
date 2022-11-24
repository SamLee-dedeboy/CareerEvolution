import * as d3 from "d3"
import { line } from "d3"

const track_index2name = ['actor', 'director', 'writer', 'producer']
interface Margin {
    top: number,
    bottom: number,
    left: number,
    right: number
}
export class TimelineConfig {
    width: number = 600  
	height: number = 600
	margin: Margin = {top: 20, right: 20, bottom: 20, left: 20}
    interval: number = 230
    xScale: any;
    tracks: any;
}
export class Timeline {
    svg: any;
    svgSelector: any;
    svgWidth: number;
    svgHeight: number;
    contentHeight: number;
    cfg: TimelineConfig;
    options: any;
    data: any;
    timeline_margin_top: number;

    public constructor(svgSelector, options) {
        this.svgSelector = svgSelector 
        this.cfg = new TimelineConfig()
        this.options = options
        this.svgWidth = this.cfg.width
        this.svgHeight = this.cfg.height
        this.contentHeight = this.cfg.height
        this.timeline_margin_top = 100
    }

    init(data) {
        this.data = data
        this.svg = d3.select(this.svgSelector)
        // setup configs
        if('undefined' !== typeof this.options){
            for(var i in this.options) {
                if('undefined' !== typeof this.options[i]){ (this.cfg as any)[i] = this.options[i]; }
			}
		}
        // calculate height of the view from timeline length
        const timeline_length = data.reduce((total, step) => total + step.movies.length, 0)
        this.contentHeight = timeline_length * this.cfg.interval
        this.svgWidth = this.cfg.width + this.cfg.margin.left + this.cfg.margin.right
        this.svgHeight = this.contentHeight + this.cfg.margin.top + this.cfg.margin.bottom

        // setup scales
        this.cfg.xScale = d3.scaleBand()
                .domain(Object.keys(this.cfg.tracks))
                .range([0, this.svgWidth])

        this.svg
            .attr("width",  this.svgWidth)
            .attr("height", this.svgHeight)

		this.svg.append("g")
            .attr("class", "canvas")
            .attr("transform", "translate(" + (this.cfg.margin.left) + "," + (this.cfg.margin.top) + ")");

        this.setupTracks()
        this.setupTimeline(data)

    }

    activate(index) {
        const active_stage_index: number = this.getSectionIndex(index)
        const text_sections = d3.selectAll(".section")
            .each(function(this: any) {
                if(+d3.select(this).attr("id").split("_")[1] == active_stage_index) {
                    this.classList.add("active")
                } else {
                    this.classList.remove("active")
                }
            })
        return
        const active_movies = this.data[index].movies
        let index_in_timeline = 0
        this.data.forEach((section, section_index) => {
            if(section_index >= index) return
            index_in_timeline += section.movies.length
        })
        const lines = this.svg.selectAll("line.connection")
            .each(function(this: any, d, i) {
                if(i >= index_in_timeline && i < index_in_timeline + active_movies.length - 1) {
                    d3.select(this).attr("opacity", 1)
                } else {
                    d3.select(this).attr("opacity", 0)
                }
            })
    }

    update(index, progress) {

    }

    setupTracks() {
        const canvas = this.svg.select("g.canvas")
        const track_names = Object.keys(this.cfg.tracks)
        const track_width = this.cfg.xScale.bandwidth()
        track_names.forEach((track_name, index) => {
            const track_color = this.cfg.tracks[track_name]
            canvas.append("rect")
                .attr("x", track_width * index)
                .attr("y", 0)
                .attr("width", track_width)
                .attr("height", this.contentHeight)
                .attr("fill", track_color)
        })
    }
    setupTimeline(data) {
        const canvas = this.svg.select("g.canvas")

        // TODO: fix multiple roles
        const xTranslate = (d) => this.cfg.xScale(d.role[0]) + this.cfg.xScale.bandwidth()/2 
        const sections_container = canvas.append("g").attr("class", "sections-container")
        // append sections
        const sections = sections_container.selectAll("g")
            .data(data)
            .join("g")
            .attr("class", "stage")
            .attr("id", (d, i) => `stage_${i}`)

        let self = this
        let circle_index = -1
        sections.each(function(this:any, d) {
            d3.select(this).selectAll("circle")
                .data(d.movies)
                .join("circle")
                .attr("class", "step")
                .attr("cx", d => xTranslate(d))
                .attr("cy", () => { 
                    circle_index += 1; 
                    return self.timeline_margin_top + circle_index * self.cfg.interval
                })
                .attr("r", 10)
                .attr("fill", "black")
                .style("cursor", "pointer")
                .on("mouseover", function(this: any, e, d) {
                    this.classList.add("hovered")
                    // TODO: animate hover effect in css

                })
                .on("mouseout", function(this: any, e, d) {
                    console.log(d)
                    this.classList.remove("hovered")
                })
        })
        // append lables
        let title_index = -1
        let snippet_index = -1
        sections.each(function(this:any, d) {
            // titles
            d3.select(this).selectAll("text.titles")
                .data(d.movies)
                .join("text")
                .attr("class", "titles")
                .attr("x", (d: any) => self.getTitlePosition(d.role))
                .attr("y", () => { 
                    title_index += 1; 
                    return self.timeline_margin_top + title_index * self.cfg.interval
                })
                .text((movie_data: any) => {
                    return movie_data.title
                })
                .call(wrap, self.cfg.xScale.bandwidth()/2)
            // snippets
            d3.select(this).selectAll("text.snippets")
                .data(d.movies)
                .join("text")
                .attr("class", "snippets")
                .attr("x", (d: any) => self.getSnippetPosition(d.role) + 30)
                .attr("y", () => { 
                    snippet_index += 1; 
                    return self.timeline_margin_top + snippet_index * self.cfg.interval
                })
                .text((movie_data: any) => {
                    if(movie_data.snippet.length == 0) return ""
                    return movie_data.snippet.map(snippet => snippet.snippet).join("\n")
                })
                .call(wrap, 700)
        })

        
        // append lines
        let line_data: any[] = []
        const timeline_movies = data.reduce((movies, step) => movies.concat(step.movies), [])
        timeline_movies.forEach((step, index) => {
            if(index == timeline_movies.length - 1) return
            line_data.push({
                d1: timeline_movies[index],
                d2: timeline_movies[index+1],
            })
        })

        canvas.selectAll("line")
            .data(line_data)
            .join("line")
            .attr("class", "connection")
            .attr("x1", d => xTranslate(d.d1))
            .attr("x2", d => xTranslate(d.d2))
            .attr("y1", (d, i) => this.timeline_margin_top + i * this.cfg.interval)
            .attr("y2", (d, i) => this.timeline_margin_top + (i+1) * this.cfg.interval)
            .attr("stroke", "black")
            .style("pointer-events", "none")
    }

    getSectionIndex(index) {
        for(let section_index = 0; section_index < this.data.length; section_index++) {
            const section_length = this.data[section_index].movies.length
            index -= section_length
            if(index < 0) return section_index
        }
        return this.data.length - 1
    }

    getSectionOffset() {
        return [0, 1000, 2000]
    }
    
    getTitlePosition(roles) {
        const xTranslate = (roles) => this.cfg.xScale(roles[0])
        return xTranslate(roles) + 10
    }

    getSnippetPosition(roles) {
        const xTranslate = (roles) => this.cfg.xScale(roles[0]) + this.cfg.xScale.bandwidth()/2 
        return xTranslate(roles)
    }

}
function wrap(text, width) {
    text.each(function (this: any, d, i) {
        var text = d3.select(this),
            words = text.text().split(/\s+/).reverse(),
            word,
            line: any[] = [],
            lineNumber = 0,
            lineHeight = 1.1, // ems
            x = text.attr("x"),
            y = text.attr("y"),
            dy = 0, //parseFloat(text.attr("dy")),
            tspan = text.text(null)
                .append("tspan")
                .attr("x", x)
                .attr("y", y)
                .attr("dy", dy + "em")
                .attr("text-anchor", "bottom")
                .attr("dominant-baseline", "central")
        while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(" "));
            if (tspan.node()!.getComputedTextLength() > width && line.length > 1) {
                line.pop();
                tspan.text(line.join(" "));
                line = [word];
                tspan = text.append("tspan")
                    .attr("x", x)
                    .attr("y", y)
                    .attr("dy", ++lineNumber * lineHeight + dy + "em")
                    .attr("dominant-baseline", "central")
                    .text(word);
            }
        }
        const line_num = text.selectAll("tspan").nodes().length
        const em_to_px = 16
        text.selectAll("tspan").attr("y", parseFloat(y) - em_to_px / 2 * lineHeight * (line_num - 1) / 2)
    });
}

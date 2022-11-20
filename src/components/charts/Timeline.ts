import * as d3 from "d3"

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
    interval: number = 100
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

    public constructor(svgSelector, options) {
        this.svgSelector = svgSelector 
        this.cfg = new TimelineConfig()
        this.options = options
        this.svgWidth = this.cfg.width
        this.svgHeight = this.cfg.height
        this.contentHeight = this.cfg.height
    }

    init(data) {
        this.svg = d3.select(this.svgSelector)
        // setup configs
        if('undefined' !== typeof this.options){
            for(var i in this.options) {
                if('undefined' !== typeof this.options[i]){ (this.cfg as any)[i] = this.options[i]; }
			}
		}
        // calculate height of the view from timeline length
        const timeline_length = data.length
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

        const xTranslate = (d) => this.cfg.xScale(track_index2name[d]) + this.cfg.xScale.bandwidth()/2 
        // append circles
        canvas.selectAll("circle")
            .data(data)
            .join("circle")
            .attr("class", "movie")
            .attr("cx", d => xTranslate(d))
            .attr("cy", (d, i) => i * this.cfg.interval)
            .attr("r", 10)
            .attr("fill", "black")
            .style("cursor", "pointer")
            .on("mouseover", function(this: any, e, d) {
                console.log(d)
                this.classList.add("hovered")
                // TODO: animate hover effect in css

            })
            .on("mouseout", function(this: any, e, d) {
                console.log(d)
                this.classList.remove("hovered")
            })
        
        // append lines
        let line_data: any[] = []
        data.forEach((datum, index) => {
            if(index == data.length - 1) return
            line_data.push({
                d1: data[index],
                d2: data[index+1],
            })
        })

        canvas.selectAll("line")
            .data(line_data)
            .join("line")
            .attr("class", "connection")
            .attr("x1", d => xTranslate(d.d1))
            .attr("x2", d => xTranslate(d.d2))
            .attr("y1", (d, i) => i * this.cfg.interval)
            .attr("y2", (d, i) => (i+1) * this.cfg.interval)
            .attr("stroke", "black")
    }

}
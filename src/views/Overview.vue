<template>
    <div id="overview-container">
        <div id="dropdown_view">
            <Dropdown @selectedChange="handleChange_dropdown"/>
        </div>
        <div id="lines_view">
            <LineChart v-if="dataExists" :myData="mySubset"></LineChart>
        </div>
    </div>
</template>

<script>
import * as d3 from "d3";
import LineChart from '../components/line_chart.vue';
import Dropdown from '../components/dropdown_subset.vue';
import HP from "../preprocess/HP_40.json"; /* Example of reading in data direct from file*/
import LoR from "../preprocess/LoR_60.json"; /* Example of reading in data direct from file*/

export default {
    data(){
        return {
            dataExists: false,
            mySubset: undefined,
            mySelection: undefined
        }
    },
    components: {
        Dropdown,
        LineChart,
    },
    created(){
        /* Fetch via CSV */
        this.drawFromJson()
    },
    mounted(){},
    methods: {
        drawFromJson(){
            // console.log("In overview: ", testData);
            if (this.mySelection == 0)  this.mySubset = HP;
            else if (this.mySelection == 1)  this.mySubset = LoR;
        },

        handleChange_dropdown(selected) {
            // handle here
            console.log('parent noticed change subset ' + selected.id + selected.text);
            this.dataExists = true;
            this.mySelection = selected.id;
            if (this.mySelection == 0)  this.mySubset = HP;
            else if (this.mySelection == 1)  this.mySubset = LoR;
        },
    }
}
</script>

<style>

    #overview-container {
        height: 100%;
        position: relative;
        justify-content: center;
    }
    #dropdown_view {
        height: 5%;
        width: 80%;
        position: relative;
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: auto;
        margin-right: auto;
    }
    #lines_view {
        height: 90%;
        width: 95%;
        position: relative;
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: auto;
        margin-right: auto;
    }
</style>

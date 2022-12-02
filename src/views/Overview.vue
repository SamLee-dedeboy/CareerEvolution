<template>
    <div id="overview-container">
        <div id="dropdown_text_title">
            <div v-if="!dataExists">
                This is the popularities of entertainment industry individuals in different movie series. 
            </div>
        </div>
        <div id="dropdown_text">
            <div v-if="!dataExists">
                <br/>
                What are the characteristics of different movie series? <br/>
                <!-- What does it take to be part of a certain series? <br/> -->
                How does participating in these movies help (or otherwise) these film industry workers? <br/>
                How active an individual is in his/her career life? <br/>
                <!-- Do individuals in a certain movie series tend to be part of the production team as well? <br/> -->
                How confident are individuals in the movies they participated in? <br/>
                <br/>
                Let's dive in:
            </div>
        </div>
        <div id="info_section">
            <!-- <div id="legend">
                <Legend v-if="!dataExists"></Legend>
            </div> -->
            <div id="dropdown_view">
                <Dropdown @selectedChange="handleChange_dropdown"/>
            </div>
        </div>
        <div id="lines_view">
            <LineChart v-if="dataExists" :myData="mySubset" :mySubsetName="mySelection.text" @selectedChange="handleSelectActor"></LineChart>
        </div>
    </div>
</template>


<script>
import * as d3 from "d3";
import LineChart from '../components/line_chart.vue';
import Dropdown from '../components/dropdown_subset.vue';
import Legend from '../components/legend_text.vue';
import HP from "../preprocess/HP_40.json"; /* Example of reading in data direct from file*/
// import LoR from "../preprocess/LoR_40.json"; /* Example of reading in data direct from file*/
// import Xmen from "../preprocess/Xmen_40.json"; /* Example of reading in data direct from file*/
// import StarWars from "../preprocess/StarWars_39.json"; /* Example of reading in data direct from file*/
// import JamesB from "../preprocess/JamesB_40.json"; /* Example of reading in data direct from file*/
import { useRoute } from 'vue-router'


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
        Legend
    },
    created(){
        /* Fetch via CSV */
        this.drawFromJson()
    },
    mounted(){},
    methods: {
        drawFromJson(){
            // console.log("In overview: ", testData);
            if (this.dataExists) {
                if (this.mySelection.id == 0)  this.mySubset = HP;
                else if (this.mySelection.id == 1)  this.mySubset = LoR;
                else if (this.mySelection.id == 2)  this.mySubset = Xmen;
                else if (this.mySelection.id == 3)  this.mySubset = StarWars;
                else if (this.mySelection.id == 4)  this.mySubset = JamesB;
            }
        },

        handleChange_dropdown(selected) {
            // handle here
            console.log('parent noticed change subset ' + selected.id + selected.text);
            this.dataExists = true;
            this.mySelection = selected;
            if (this.mySelection.id == 0)  this.mySubset = HP;
            else if (this.mySelection.id == 1)  this.mySubset = LoR;
            else if (this.mySelection.id == 2)  this.mySubset = Xmen;
            else if (this.mySelection.id == 3)  this.mySubset = StarWars;
            else if (this.mySelection.id == 4)  this.mySubset = JamesB;
        },
        handleSelectActor(selected) {
            console.log('parent noticed change actor ' + selected.id + selected.name);
            this.$router.push({ name: 'actorview', params: { id: selected.id } })
        }
    }
}
</script>

<style>

    #overview-container {
        height: 100%;
        position: relative;
        justify-content: center;
    }
    #info_section {
        display: flex;
        height: 5%;
        width: 30%;
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: auto;
        margin-right: auto;
    }
    #dropdown_text_title {
        font-weight: bold;
        font-size: 20px;
    }
    #dropdown_text {
        font-size: 12px;
    }
    /* #legend {
        position: relative;
        width: 5%;
    } */
    #dropdown_view {
        position: relative;
        width: 85%;
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

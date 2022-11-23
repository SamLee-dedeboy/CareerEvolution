<template>
    <div class="overview-container">
        <LineChart v-if="dataExists" :myData="mySubset"></LineChart>
    </div>
</template>

<script>
import * as d3 from "d3";
import LineChart from '../components/line_chart.vue';
import testData from "../preprocess/HP_40.json"; /* Example of reading in data direct from file*/

export default {
    data(){
        return {
            dataExists: true,
            mySubset: undefined,
        }
    },
    components: {
        LineChart,
    },
    created(){
        /* Fetch via CSV */
        this.drawFromJson()
    },
    mounted(){},
    methods: {
        drawFromJson(){
            console.log("In overview: ", testData);
            this.mySubset = testData;
        },
    }
}
</script>

<style>
    
</style>

<template>
  <div id="dropdown">
    <select v-model="selected" @change="onChange($event)" class="form-control">
       <option v-for="p in subsets" v-bind:value="{ id: p.id, text: p.name }">{{ p.name }}
       </option>
   </select>
  </div>
</template>

<script>
    import * as d3 from "d3";

    export default {
        name: 'Dropdown',
        data() { // pass data to others
            return {
                selected: undefined,
                subsets: [
                    {
                        id: 0,
                        name: "Harry Potter"
                    },
                    {
                        id: 1,
                        name: "Lord of the Rings"
                    },
                    {
                        id: 2,
                        name: "X-Men"
                    },
                    {
                        id: 3,
                        name: "Star Wars"
                    },
                    {
                        id: 4,
                        name: "James Bond (007)"
                    }
                ]
            }
        },
        props:{ // received data from others
            // myData: Array
        },
        watch: { 
            // myData: function(newVal, oldVal) { // watch it
            //     console.log(this.myData);
            //     this.subsets = this.myData;
            //     this.selected = this.myData[0];
            // }
        },
        mounted(){ 
        },
        methods: {
            onChange(event) {
                console.log(this.selected.id, this.selected.text);
                this.$emit('selectedChange', this.selected);
            }
        }
    }

</script>


<style>

    #dropdown {
        width:  100%;
        height: 100%;
    }
</style>
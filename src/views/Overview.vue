<template>
    <div class="homeview-container">
        <p> Home view</p>
        <ActorNetwork></ActorNetwork>
    </div>
</template>
<script setup lang="ts">
import ActorNetwork from '../components/ActorNetwork.vue';
import { useStore } from 'vuex'
import * as vue from "vue"
const store = useStore()
const test_store = vue.computed(() => store.state.test)
console.log(test_store.value)
</script>
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "./router"
import store from "./store"

const app = createApp(App)
app.provide('server_address', 'http://127.0.0.1:5000')
app.use(router);
app.use(store)
app.mount('#app')

import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

const app = createApp(App)
app.provide('server_address', 'http://127.0.0.1:5000')
app.mount('#app')

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


// import './assets/main.css'
import './scss/custom.scss'
import UIComponents from "./components/UI/index"
import store from "@/store";
import 'bootstrap/dist/js/bootstrap.js';
// import '@fortawesome/fontawesome-svg-core';



const app = createApp(App)

UIComponents.forEach(el =>
    app.component(el.name, el)
);

app.use(router)
app.use(store)


app.mount('#app')

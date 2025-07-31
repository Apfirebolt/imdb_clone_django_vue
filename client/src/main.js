import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import router from './routes'
import App from './App.vue'

// AOS imports
import 'aos/dist/aos.css'
import 'vue3-toastify/dist/index.css';

const app = createApp(App)
app.use(router)
app.use(createPinia())
app.mount('#app');

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router';
import MainComponent from './components/MainComponent.vue';
import App from './App.vue'
import './assets/main.css';
import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/saga-blue/theme.css'; // Или другую тему
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';

const app = createApp(App);

const routes = [
    { path: '/:address', component: MainComponent }, 
];

const router = createRouter({
    history: createWebHistory(),
    routes,
  });

// Используйте PrimeVue в вашем приложении
app.use(PrimeVue);
app.use(router);

app.mount('#app');

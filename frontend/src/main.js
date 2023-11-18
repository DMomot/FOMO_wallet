import { createApp } from 'vue'
import App from './App.vue'
// import './assets/main.css';
import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/saga-blue/theme.css'; // Или другую тему
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';

const app = createApp(App);

// Используйте PrimeVue в вашем приложении
app.use(PrimeVue);

app.mount('#app');

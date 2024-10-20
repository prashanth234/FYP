import { createApp } from 'vue'
import App from './App.vue'
import router from './router';

import { IonicVue } from '@ionic/vue';

/* Core CSS required for Ionic components to work properly */
import '@ionic/vue/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/vue/css/normalize.css';
import '@ionic/vue/css/structure.css';
import '@ionic/vue/css/typography.css';

/* Optional CSS utils that can be commented out */
import '@ionic/vue/css/padding.css';
import '@ionic/vue/css/float-elements.css';
import '@ionic/vue/css/text-alignment.css';
import '@ionic/vue/css/text-transformation.css';
import '@ionic/vue/css/flex-utils.css';
import '@ionic/vue/css/display.css';

/* Theme variables */
import './theme/variables.css';
import './theme/global.scss';

import 'vue-advanced-cropper/dist/style.css';

import { createPinia } from 'pinia';

import VueSocialSharing from 'vue-social-sharing';

import "./firebase.js"

import animateTitle from './utils/animateTitle';
import { checkAndBringUp } from './utils/manageBackend';

const pinia = createPinia()

const app = createApp(App)
  .use(IonicVue)
  .use(router)
  .use(pinia)
  .use(VueSocialSharing);
  
router.isReady().then(async () => {

  if (import.meta.env.VITE_START_APP_URL) {
    const titleContainer = animateTitle('Selfdive')
    await checkAndBringUp()
    titleContainer.remove();
  }
  
  app.mount('#app');
});
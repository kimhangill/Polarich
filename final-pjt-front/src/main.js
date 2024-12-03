import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import router from './router'
import '@/styles.css'
import { useKakao } from 'vue3-kakao-maps'
import geolocation from 'geolocation'
loadFonts()
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
useKakao()
createApp(App)
  .use(pinia)
  .use(vuetify)
  .use(router)
  .use(geolocation)
  .mount('#app')

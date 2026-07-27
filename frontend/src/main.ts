import { createPinia } from 'pinia'
import { createApp } from 'vue'
import './assets/main.css'

import App from './App.vue'
import router from './router'

import Aura from '@primeuix/themes/aura'
import PrimeVue from 'primevue/config'

import { setUnauthorizedHandler } from '@/api/api.ts'
import { useAuthStore } from '@/stores/auth.ts'
import 'primeflex/primeflex.css'
import 'primeicons/primeicons.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.use(PrimeVue, {
  theme: {
    preset: Aura,
  },
})

const authStore = useAuthStore()

setUnauthorizedHandler(() => {
  authStore.logout()
})

await authStore.initialize()

app.mount('#app')

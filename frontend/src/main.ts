import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'

import 'primeicons/primeicons.css'
import 'primeflex/primeflex.css'
import { useAuthStore } from '@/stores/auth.ts'
import { setUnauthorizedHandler } from '@/api/api.ts'

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

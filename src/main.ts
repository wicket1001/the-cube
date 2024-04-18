import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
//import { VuetifyDateAdapter } from 'vuetify/date/adapters/vuetify'
//import { aliases, fa } from 'vuetify/iconsets/fa'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

import {createPinia} from 'pinia'

const vuetify = createVuetify({
  components,
  directives,
  /*date: {
    adapter: VuetifyDateAdapter
  }*/
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})

const pinia = createPinia()

const app = createApp(App)

app.use(router)
app.use(vuetify)
app.use(pinia)

app.mount('#app')

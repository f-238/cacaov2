import { createApp } from 'vue'
import App from './App.vue'
import { applyStoredUserSettings } from './services/userSettings'

applyStoredUserSettings()
createApp(App).mount('#app')

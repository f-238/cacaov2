/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_THINGSPEAK_READ_API_KEY: string
  readonly VITE_THINGSPEAK_CHANNEL_ID: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

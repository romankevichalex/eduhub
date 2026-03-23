import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'
import { fileURLToPath, URL } from 'node:url'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      devOptions: {
        enabled: true,           // Включаем PWA в режиме разработки
        type: 'module',           // Тип сервис-воркера
        navigateFallback: 'index.html'
      },
      manifest: {
        name: "EduHub",
        short_name: "EduHub",
        start_url: "/",
        display: "standalone",  // критично важно!
        theme_color: "#ebff90",
        background_color: "#ffffff",
        icons: [
          {
            src: "/192.png",
            sizes: "192x192",
            type: "image/png"
          },
          {
            src: "/512.png",
            sizes: "512x512",
            type: "image/png"
          }
        ]
      }
    })

  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    // Разрешаем все хосты(для теста), так как они вечно меняются
    allowedHosts: true
  }
})



import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'
import { fileURLToPath, URL } from 'node:url'
import Icons from 'unplugin-icons/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Icons({
      compiler: 'vue3'
    }),
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
    allowedHosts: true,
    proxy: {
      '/api': {
        target: 'https://eduhub-uyvc.onrender.com',
        changeOrigin: true,
        //secure: false, // если нужно игнорировать SSL (иногда помогает)
        //rewrite: (path) => path.replace(/^\/api/, '') // если у вас в запросах уже есть /api
      }
    }
  }
})



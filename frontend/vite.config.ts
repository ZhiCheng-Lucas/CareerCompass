import path from 'node:path'
import vue from '@vitejs/plugin-vue'
import autoprefixer from 'autoprefixer'

import tailwind from 'tailwindcss'
import { defineConfig } from 'vite'

export default defineConfig({
  // base: '/CareerCompass/' is required for github pages.
  // You must commentout th base:'..' code below before building and uploading to netlify. 

  base: '/CareerCompass/',  // For GitHub Pages

  css: {
    postcss: {
      plugins: [tailwind(), autoprefixer()],
    },
  },
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})

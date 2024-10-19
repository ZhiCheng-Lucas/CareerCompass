<template>
    <img :src="logoSrc" alt="CareerCompass Logo" class="logo" :class="{ 'logo-dark': isDarkMode }" />
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue'
  import { useColorMode } from '@vueuse/core'
  import logoSrc from '@/assets/logo.svg'
  
  const colorMode = useColorMode()
  const isDarkMode = computed(() => colorMode.value === 'dark')
  </script>
  
  <style scoped>
  .logo {
    height: 2rem; /* Adjust this value to match your desired size */
    width: auto;
    filter: invert(0%) sepia(100%) saturate(0%) hue-rotate(145deg) brightness(100%) contrast(100%);
  }
  
  .logo-dark {
    filter: invert(100%) sepia(100%) saturate(0%) hue-rotate(137deg) brightness(106%) contrast(106%);
  }
  </style>
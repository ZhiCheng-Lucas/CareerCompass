<script setup lang="ts">
import { ref, onMounted } from 'vue'

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu'
import { Switch } from '@/components/ui/switch'

const isDyslexicFont = ref<boolean>(false)
const isHighContrast = ref<boolean>(false)

const toggleDyslexicFont = (checked: boolean): void => {
  isDyslexicFont.value = checked
  if (checked) {
    document.body.style.fontFamily = 'OpenDyslexic-Regular, sans-serif'
  } else {
    document.body.style.fontFamily = ''
  }
}

const toggleHighContrast = (checked: boolean): void => {
  isHighContrast.value = checked
  if (checked) {
    document.documentElement.classList.add('high-contrast')
  } else {
    document.documentElement.classList.remove('high-contrast')
  }
}

/**
 * Enables accessibility features (OpenDyslexic font and high contrast mode) by default when the component mounts.
 * For Gov Tech A11y Automation Testing
 *
 * The onMounted hook ensures these settings are applied after the DOM is ready:
 * - toggleDyslexicFont(true): Applies OpenDyslexic font to the entire document body
 * - toggleHighContrast(true): Adds high-contrast class to the document root
 *
 * - Settings can still be toggled off by users via the dropdown menu
 */
// onMounted(() => {
//   toggleDyslexicFont(false)
//   toggleHighContrast(false)
// })
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger
      class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2">
      Accessibility Options
    </DropdownMenuTrigger>
    <DropdownMenuContent class="w-56">
      <DropdownMenuLabel>Appearance</DropdownMenuLabel>
      <DropdownMenuSeparator />
      <DropdownMenuItem>
        <div class="flex items-center justify-between space-x-2">
          <label for="dyslexic-font">OpenDyslexic Font</label>
          <Switch id="dyslexic-font" :checked="isDyslexicFont" @update:checked="toggleDyslexicFont" />
        </div>
      </DropdownMenuItem>
      <DropdownMenuItem>
        <div class="flex items-center justify-between space-x-2">
          <label for="high-contrast">High Contrast</label>
          <Switch id="high-contrast" :checked="isHighContrast" @update:checked="toggleHighContrast" />
        </div>
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>

<style scoped>
@font-face {
  font-family: 'OpenDyslexic-Regular';
  src: url('@/assets/OpenDyslexic-Regular.otf') format('opentype');
}
</style>

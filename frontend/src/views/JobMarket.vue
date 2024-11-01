<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Card, CardHeader, CardTitle } from '@/components/ui/card'
import MarketTrends from '@/components/MarketTrends.vue'
import { getMarketTrends } from '@/services/api'
import type { SectorTrend } from '@/services/api'

const marketTrends = ref<SectorTrend[]>([])
const isLoading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    const response = await getMarketTrends()
    // Access the jobMarketTrends property from the response
    marketTrends.value = response[0]?.jobMarketTrends || []
    console.log('Market trends loaded:', marketTrends.value)
  } catch (e) {
    console.error('Error fetching market trends:', e)
    error.value = 'Failed to load market trends'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="space-y-8">
    <div class="flex justify-between items-center">
      <h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
        Job Market Insights
      </h1>
    </div>

    <div class="grid gap-8">
      <template v-if="isLoading">
        <Card>
          <CardHeader>
            <!-- Changed from CardTitle to h2 as suggested by GovTech OObee's Accessibility checker 
                 to maintain proper heading hierarchy for loading state under the main h1 -->
            <h2 class="text-2xl font-semibold tracking-tight">Loading market trends...</h2>
          </CardHeader>
        </Card>
      </template>
      
      <template v-else-if="error">
        <Card>
          <CardHeader>
            <!-- Changed from CardTitle to h2 as suggested by GovTech OObee's Accessibility checker 
                 to maintain proper heading hierarchy for error state under the main h1 -->
            <h2 class="text-2xl font-semibold tracking-tight text-destructive">{{ error }}</h2>
          </CardHeader>
        </Card>
      </template>

      <template v-else>
        <MarketTrends :trends="marketTrends" />
      </template>
    </div>
  </div>
</template>
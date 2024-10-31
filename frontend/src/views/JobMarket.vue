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
            <CardTitle>Loading market trends...</CardTitle>
          </CardHeader>
        </Card>
      </template>
      
      <template v-else-if="error">
        <Card>
          <CardHeader>
            <CardTitle class="text-destructive">{{ error }}</CardTitle>
          </CardHeader>
        </Card>
      </template>

      <template v-else>
        <MarketTrends :trends="marketTrends" />
      </template>

      <!-- Placeholder for future sections -->
      <Card>
        <CardHeader>
          <CardTitle>Additional Market Insights</CardTitle>
        </CardHeader>
      </Card>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Card, CardHeader, CardTitle } from '@/components/ui/card'
import MarketTrends from '@/components/MarketTrends.vue'
import GrowthInsights from '@/components/GrowthInsights.vue'
import LaborStats from '@/components/LaborStats.vue'
import { getMarketTrends, getIndustryGrowth, getSingaporeLaborStats } from '@/services/api'
import type { SectorTrend } from '@/services/api'
import type { IndustryGrowth } from '@/services/api'
import type { LaborStats as LaborStatsType } from '@/services/api'

const marketTrends = ref<SectorTrend[]>([])
const industryGrowth = ref<IndustryGrowth[]>([])
const laborStats = ref<LaborStatsType>({})
const isLoading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    const [marketTrendsRes, industryGrowthRes, laborStatsRes] = await Promise.all([
      getMarketTrends(),
      getIndustryGrowth(),
      getSingaporeLaborStats()
    ])

    marketTrends.value = marketTrendsRes[0]?.jobMarketTrends || []
    industryGrowth.value = industryGrowthRes
    laborStats.value = laborStatsRes
  } catch (e) {
    console.error('Error fetching data:', e)
    error.value = 'Failed to load market insights'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <!-- Added mx-auto and max-w-[95%] for mobile margins -->
  <div class="space-y-6 mx-auto max-w-[95%] lg:max-w-full">
    <!-- Header -->
    <div class="flex flex-col space-y-2">
      <h1 class="scroll-m-20 text-3xl font-extrabold tracking-tight lg:text-5xl">
        Job Market Insights
      </h1>
      <p class="text-muted-foreground">
        Comprehensive view of Singapore's employment landscape and market trends
      </p>
    </div>

    <!-- Content Grid -->
    <div class="grid gap-6">
      <template v-if="isLoading">
        <Card class="mx-auto w-full max-w-[95%] lg:max-w-full">
          <CardHeader>
            <CardTitle>Loading market insights...</CardTitle>
          </CardHeader>
        </Card>
      </template>

      <template v-else-if="error">
        <Card class="mx-auto w-full max-w-[95%] lg:max-w-full">
          <CardHeader>
            <CardTitle class="text-destructive">{{ error }}</CardTitle>
          </CardHeader>
        </Card>
      </template>

      <template v-else>
        <!-- Growth Insights and Labor Stats Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <GrowthInsights
            v-if="industryGrowth.length > 0"
            :growth-data="industryGrowth[0]"
            class="mx-auto w-full max-w-[95%] lg:max-w-full"
          />
          <LaborStats
            v-if="Object.keys(laborStats).length > 0"
            :stats="laborStats"
            class="mx-auto w-full max-w-[95%] lg:max-w-full"
          />
        </div>

        <!-- Market Trends Section -->
        <MarketTrends :trends="marketTrends" class="mx-auto w-full max-w-[95%] lg:max-w-full" />
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { LineChart } from '@/components/ui/chart-line'
import { TrendingUp, TrendingDown } from 'lucide-vue-next'
import type { IndustryGrowth } from '@/services/api'

interface Props {
  growthData: IndustryGrowth
}

const props = defineProps<Props>()

// Helper function to convert quarter to a sortable number
const quarterToNumber = (quarter: string) => {
  const year = parseInt(quarter.slice(0, -3)) // Get year (23, 24, etc)
  const q = parseInt(quarter.slice(1, 2)) // Get quarter number (1,2,3,4)
  return year * 4 + q // Convert to a single sortable number
}

// Format growth data for the chart
const chartData = computed(() => {
  return props.growthData.quarterlyGrowth
    .map((item) => ({
      quarter: item.quarter,
      Growth: item.growth,
      sortValue: quarterToNumber(item.quarter)
    }))
    .sort((a, b) => a.sortValue - b.sortValue) // Sort by our computed value
    .map(({ quarter, Growth }) => ({ quarter, Growth })) // Remove the sortValue from final data
})

const chartCategories = computed(() => ['Growth'])

// Custom Y-axis formatter for percentages
const yFormatter = (tick: number) => `${tick.toFixed(1)}%`

// Parse current forecast range
const getCurrentForecast = (forecast: string) => {
  const match = forecast.match(/(\d+\.?\d*)\s*to\s*(\d+\.?\d*)/)
  if (match) {
    const [_, lower, upper] = match
    return {
      lower: parseFloat(lower),
      upper: parseFloat(upper),
      average: (parseFloat(lower) + parseFloat(upper)) / 2
    }
  }
  return null
}

const forecast = computed(() => getCurrentForecast(props.growthData.forecast.current))
</script>

<template>
  <Card class="w-full">
    <CardHeader>
      <CardTitle class="flex items-center justify-between">
        <span>Growth Forecast</span>
        <div v-if="forecast" class="flex items-center gap-2 text-sm">
          <TrendingUp v-if="forecast.average >= 0" class="w-4 h-4 text-primary" />
          <TrendingDown v-else class="w-4 h-4 text-destructive" />
          <span :class="['font-mono', forecast.average >= 0 ? 'text-primary' : 'text-destructive']">
            {{ forecast.lower }}% - {{ forecast.upper }}%
          </span>
        </div>
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div class="space-y-6">
        <!-- Forecast Details -->
        <div class="space-y-2">
          <p class="text-sm text-muted-foreground">
            Latest forecast as of {{ growthData.forecast.date }}
          </p>
          <p class="text-sm">
            <span class="font-medium">Previous:</span> {{ growthData.forecast.previous }}
          </p>
          <p class="text-sm">
            <span class="font-medium">Current:</span> {{ growthData.forecast.current }}
          </p>
          <p class="text-xs text-muted-foreground italic">
            Source: {{ growthData.forecast.source }}
          </p>
        </div>

        <!-- Growth Chart -->
        <div class="w-full">
          <LineChart
            :data="chartData"
            index="quarter"
            :categories="chartCategories"
            :y-formatter="yFormatter"
          />
        </div>
      </div>
    </CardContent>
  </Card>
</template>

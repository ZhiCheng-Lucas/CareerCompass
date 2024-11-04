<script setup lang="ts">
import { LineChart } from '@/components/ui/chart-line'
import { computed } from 'vue'

const props = defineProps<{
  employmentData: Array<{
    year: number
    employed_percentage: number
    full_time_permanent_percentage: number
  }>
}>()

const percentageChartData = computed(() =>
  props.employmentData.map((item) => ({
    year: item.year,
    'Employed Percentage': item.employed_percentage,
    'Full-Time Percentage': item.full_time_permanent_percentage
  }))
)

const percentageFormatter = (tick: number | Date, i: number, ticks: number[] | Date[]): string => {
  if (typeof tick === 'number') {
    return `${tick.toFixed(1)}%`
  }
  return ''
}
</script>

<template>
  <div>
    <LineChart
      :data="percentageChartData"
      index="year"
      :categories="['Employed Percentage', 'Full-Time Percentage']"
      :colors="[`hsl(142, 70%, 45%)`, `hsl(12, 85%, 65%)`]"
      :y-formatter="percentageFormatter"
    />
  </div>
</template>

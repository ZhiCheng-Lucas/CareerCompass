<script setup lang="ts">
import { LineChart } from '@/components/ui/chart-line'
import { computed } from 'vue'

const props = defineProps<{
  employmentData: Array<{
    year: number
    median_gross_monthly_starting_salary: number
  }>
}>()

const salaryChartData = computed(() =>
  props.employmentData.map((item) => ({
    year: item.year,
    'Median Salary': item.median_gross_monthly_starting_salary
  }))
)

const salaryFormatter = (tick: number | Date, i: number, ticks: number[] | Date[]): string => {
  if (typeof tick === 'number') {
    return `$${new Intl.NumberFormat('en-US').format(tick)}`
  }
  return ''
}
</script>

<template>
  <div>
    <LineChart
      :data="salaryChartData"
      index="year"
      :categories="['Median Salary']"
      :y-formatter="salaryFormatter"
    />
  </div>
</template>

<script setup lang="ts">
import { LineChart } from '@/components/ui/chart-line'
import { computed } from 'vue';

const props = defineProps<{
  employmentData: Array<{
    year: number;
    employed_percentage: number;
    full_time_permanent_percentage: number;
    median_gross_monthly_starting_salary: number;
  }>
}>();

const chartData = computed(() => props.employmentData.map(item => ({
  year: item.year,
  'Employed Percentage': item.employed_percentage,
  'Full-Time Percentage': item.full_time_permanent_percentage,
  'Median Salary': item.median_gross_monthly_starting_salary
})));
</script>

<template>
  <LineChart
    :data="chartData"
    index="year"
    :categories="['Employed Percentage', 'Full-Time Percentage', 'Median Salary']"
    :y-formatter="(tick, i) => {
      if (typeof tick === 'number') {
        if (tick > 1000) {
          return `$${new Intl.NumberFormat('en-US').format(tick)}`
        }
        return `${tick.toFixed(1)}%`
      }
      return ''
    }"
  />
</template>
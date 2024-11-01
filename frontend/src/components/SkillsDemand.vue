<script setup lang="ts">
import { computed } from 'vue'
import { BarChart } from '@/components/ui/chart-bar'

const props = defineProps<{
  skillsData: Array<{ skill: string; count: number }>
}>()

const chartData = computed(() =>
  props.skillsData.map((item) => ({
    skill: item.skill,
    'Number of listings': item.count
  }))
)
</script>

<template>
  <BarChart
    :data="chartData"
    index="skill"
    :categories="['Number of listings']"
    :y-formatter="
      (tick) => {
        return typeof tick === 'number' ? tick.toString() : ''
      }
    "
  />
</template>

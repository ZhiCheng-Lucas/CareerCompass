<template>
  <div class="chart-container">
    <Bar :data="chartData" :options="chartOptions" :key="colorMode" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import type { ChartOptions } from 'chart.js'
import { useColorMode } from '@vueuse/core'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

interface SkillData {
  skill: string;
  count: number;
}

const props = defineProps<{
  skillsData: SkillData[]
}>()

const barColor = ref('rgba(34, 197, 94, 0.8)') // Keeping the explicit green color
const colorMode = useColorMode()

const getThemeColors = () => {
  const isDark = colorMode.value === 'dark'
  return {
    textColor: isDark ? 'rgba(255, 255, 255, 0.7)' : 'rgba(0, 0, 0, 0.7)',
    gridColor: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
  }
}

const themeColors = ref(getThemeColors())

watch(colorMode, () => {
  themeColors.value = getThemeColors()
})

const chartData = computed(() => ({
  labels: props.skillsData.map(item => item.skill),
  datasets: [
    {
      label: 'Skill Demand',
      data: props.skillsData.map(item => item.count),
      backgroundColor: barColor.value,
    }
  ]
}))

const chartOptions = computed<ChartOptions<'bar'>>(() => ({
  indexAxis: 'y',
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    x: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Number of Job Postings',
        color: themeColors.value.textColor
      },
      ticks: {
        color: themeColors.value.textColor
      },
      grid: {
        color: themeColors.value.gridColor
      }
    },
    y: {
      ticks: {
        callback: function(value: string | number, index: number): string {
          return props.skillsData[index]?.skill || '';
        },
        color: themeColors.value.textColor
      },
      grid: {
        display: false
      }
    }
  },
  layout: {
    padding: {
      top: 10,
      right: 20,
      bottom: 10,
      left: 10
    }
  }
}))
</script>

<style scoped>
.chart-container {
  height: 400px;
  width: 100%;
  position: relative;
}
</style>
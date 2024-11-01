<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Briefcase } from 'lucide-vue-next'

interface LaborStats {
  [period: string]: {
    [sector: string]: number;
  }
}

interface Props {
  stats: LaborStats
}

interface SectorStat {
  sector: string;
  count: number;
  percentage: number;
}

const props = defineProps<Props>()

// Get the latest period (should be "2024 2Q")
const latestPeriod = computed(() => Object.keys(props.stats)[0])

// Sort sectors by vacancy count and calculate percentages
const sectorStats = computed<SectorStat[]>(() => {
  if (!latestPeriod.value) return []

  const periodStats = props.stats[latestPeriod.value]
  // Convert all values to numbers first
  const entries = Object.entries(periodStats).map(([sector, count]) => [
    sector,
    Number(count)
  ]) as [string, number][]

  // Calculate total from the converted numbers
  const totalVacancies = entries.reduce((sum, [, count]) => sum + count, 0)

  // Create and sort stats using the converted numbers
  return entries
    .map(([sector, count]): SectorStat => ({
      sector,
      count,
      percentage: (count / totalVacancies) * 100
    }))
    .sort((a, b) => b.count - a.count)
})

// Format large numbers
const formatNumber = (num: number) => {
  return new Intl.NumberFormat('en-SG').format(num)
}
</script>

<template>
  <Card class="w-full">
    <CardHeader>
      <CardTitle class="flex items-center justify-between">
        <span>Job Vacancies</span>
        <span class="text-sm font-mono">{{ latestPeriod }}</span>
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div class="space-y-4">
        <div class="grid gap-4">
          <div v-for="stat in sectorStats" :key="stat.sector" class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center gap-2">
                <div class="p-1.5 rounded-md bg-primary/10">
                  <Briefcase class="w-3.5 h-3.5 text-primary" />
                </div>
                <span class="font-medium">{{ stat.sector }}</span>
              </div>
              <span class="font-mono">{{ formatNumber(stat.count) }}</span>
            </div>
            <Progress :model-value="stat.percentage" class="h-2" />
            <p class="text-xs text-muted-foreground text-right">
              {{ stat.percentage.toFixed(1) }}% of total vacancies
            </p>
          </div>
        </div>

        <p class="text-xs text-muted-foreground italic text-center pt-2">
          Source: Ministry of Manpower, Singapore
        </p>
      </div>
    </CardContent>
  </Card>
</template>
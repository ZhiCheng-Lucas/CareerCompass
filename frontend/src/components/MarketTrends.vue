<script setup lang="ts">
import { ref } from 'vue'
import { 
  Accordion,
  AccordionContent, 
  AccordionItem, 
  AccordionTrigger 
} from '@/components/ui/accordion'
import { Badge } from '@/components/ui/badge'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import type { SectorTrend } from '@/services/api'

interface Props {
  trends: SectorTrend[]
}

const props = withDefaults(defineProps<Props>(), {
  trends: () => []
})

const openItem = ref<string | null>(null)

const getBadgeVariant = (growth: string): 'default' | 'destructive' | 'outline' => {
  const value = parseFloat(growth)
  if (isNaN(value)) return 'default'
  if (value < 0) return 'destructive'
  // Use outline as base for positive values, we'll style it with custom class
  return 'outline'
}

const getBadgeClasses = (growth: string): string => {
  const value = parseFloat(growth)
  if (value > 0) {
    return 'border-transparent bg-primary text-primary-foreground'
  }
  return ''
}

const getBadgeContent = (growth: string): string => {
  const value = parseFloat(growth)
  if (isNaN(value)) return growth
  return value > 0 ? `+${growth}` : growth
}

const handleValueChange = (value: string) => {
  openItem.value = openItem.value === value ? null : value
}
</script>

<template>
  <Card v-if="trends.length > 0" class="w-full">
    <CardHeader>
      <CardTitle>Market Trends by Sector</CardTitle>
    </CardHeader>
    <CardContent>
      <Accordion 
        type="single"
        collapsible
        :value="openItem"
        @update:value="handleValueChange"
        class="w-full space-y-4"
      >
        <AccordionItem 
          v-for="trend in trends" 
          :key="trend.sector"
          :value="trend.sector"
          class="border rounded-lg px-4"
        >
          <AccordionTrigger class="w-full">
            <div class="flex items-center justify-between w-full">
              <span class="text-lg font-semibold">{{ trend.sector }}</span>
              <Badge 
                v-if="trend.trends[0]?.growth"
                :variant="getBadgeVariant(trend.trends[0].growth)"
                :class="[
                  'ml-2',
                  getBadgeClasses(trend.trends[0].growth)
                ]"
              >
                {{ getBadgeContent(trend.trends[0].growth) }}
              </Badge>
            </div>
          </AccordionTrigger>
          <AccordionContent class="pt-4">
            <div class="space-y-4">
              <div 
                v-for="(trendItem, index) in trend.trends" 
                :key="index"
                class="space-y-2"
              >
                <div class="flex items-center gap-2 text-sm text-muted-foreground">
                  <span class="font-medium">Period:</span>
                  <span class="capitalize">{{ trendItem.period }}</span>
                </div>
                <p class="text-sm">{{ trendItem.details }}</p>
              </div>
              <div class="mt-4 pt-4 border-t">
                <p class="text-sm text-muted-foreground italic">
                  {{ trend.source }}
                </p>
              </div>
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </CardContent>
  </Card>
  <Card v-else class="w-full">
    <CardHeader>
      <CardTitle>No market trends available</CardTitle>
    </CardHeader>
  </Card>
</template>
<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  currentStep: number
  steps?: string[]
  status?: 'wait' | 'process' | 'finish' | 'error'
}

const props = withDefaults(defineProps<Props>(), {
  steps: () => ['上传', '预处理', '识别', '批改', '完成'],
  status: 'process',
})

function getStepStatus(index: number): 'wait' | 'process' | 'finish' | 'error' {
  if (props.status === 'error') return 'error'
  if (index < props.currentStep) return 'finish'
  if (index === props.currentStep) return 'process'
  return 'wait'
}

const currentStepText = computed(() => {
  if (props.currentStep >= props.steps.length) return '完成'
  return `${props.steps[props.currentStep]}中...`
})
</script>

<template>
  <div class="grading-progress">
    <div class="progress-track">
      <div
        v-for="(step, index) in steps"
        :key="step"
        class="step"
        :class="{
          'is-finish': getStepStatus(index) === 'finish',
          'is-process': getStepStatus(index) === 'process',
          'is-error': getStepStatus(index) === 'error',
          'is-wait': getStepStatus(index) === 'wait',
        }"
      >
        <div class="step-indicator">
          <div class="step-dot">
            <svg v-if="getStepStatus(index) === 'finish'" width="12" height="12" viewBox="0 0 12 12" fill="none">
              <path d="M2.5 6L5 8.5L9.5 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div v-else-if="getStepStatus(index) === 'process'" class="step-spinner"></div>
            <svg v-else-if="getStepStatus(index) === 'error'" width="12" height="12" viewBox="0 0 12 12" fill="none">
              <path d="M3 3L9 9M9 3L3 9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <div v-if="index < steps.length - 1" class="step-line"></div>
        </div>
        <span class="step-label">{{ step }}</span>
      </div>
    </div>
    <div class="current-step-text">{{ currentStepText }}</div>
  </div>
</template>

<style scoped>
.grading-progress {
  padding: var(--space-4) 0;
}

.progress-track {
  display: flex;
  justify-content: space-between;
  position: relative;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  flex: 1;
  position: relative;
}

.step-indicator {
  display: flex;
  align-items: center;
  width: 100%;
  position: relative;
}

.step-dot {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: var(--bg-secondary);
  border: 2px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--duration-fast) var(--ease-out-quart);
  position: relative;
  z-index: 1;
  flex-shrink: 0;
}

.step.is-finish .step-dot {
  background: var(--success);
  border-color: var(--success);
  color: white;
}

.step.is-process .step-dot {
  border-color: var(--primary);
  background: rgba(79, 70, 229, 0.08);
  box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
}

.step.is-error .step-dot {
  background: var(--error);
  border-color: var(--error);
  color: white;
}

.step-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid var(--primary);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.step-line {
  position: absolute;
  top: 15px;
  left: calc(50% + 16px);
  right: calc(-50% + 16px);
  height: 2px;
  background: var(--border);
  transition: background var(--duration-fast);
}

.step.is-finish .step-line {
  background: var(--success);
}

.step-label {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
  text-align: center;
  transition: color var(--duration-fast);
}

.step.is-finish .step-label,
.step.is-process .step-label {
  color: var(--text-primary);
}

.step.is-process .step-label {
  font-weight: 500;
}

.current-step-text {
  text-align: center;
  margin-top: var(--space-4);
  font-size: 0.875rem;
  color: var(--primary);
  font-weight: 500;
}

/* Responsive */
@media (max-width: 480px) {
  .step-label {
    font-size: 0.6875rem;
  }

  .step-dot {
    width: 28px;
    height: 28px;
  }

  .step-line {
    top: 13px;
  }
}
</style>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getGradingResult } from '@/services/api'
import type { GradingResultResponse } from '@/types/api'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref<string | null>(null)
const gradingResult = ref<GradingResultResponse | null>(null)

const scorePercent = computed(() => {
  if (!gradingResult.value) return 0
  return Math.round((gradingResult.value.total_score / gradingResult.value.max_score) * 100)
})

const scoreColor = computed(() => {
  if (scorePercent.value >= 75) return 'var(--success)'
  if (scorePercent.value >= 60) return 'var(--warning)'
  return 'var(--error)'
})

const statusText = computed(() => {
  if (scorePercent.value >= 90) return '优秀'
  if (scorePercent.value >= 75) return '良好'
  if (scorePercent.value >= 60) return '及格'
  return '需努力'
})

const statusIcon = computed(() => {
  if (scorePercent.value >= 75) return 'success'
  if (scorePercent.value >= 60) return 'warning'
  return 'error'
})

onMounted(async () => {
  const gradingId = route.params.gradingId as string

  if (!gradingId) {
    error.value = '缺少批改ID'
    loading.value = false
    return
  }

  try {
    const res = await getGradingResult(gradingId)
    gradingResult.value = res.data ?? null
  } catch (err: any) {
    error.value = err.message || '获取批改结果失败'
  } finally {
    loading.value = false
  }
})

function goBack() {
  router.back()
}

function goUpload() {
  router.push('/upload')
}
</script>

<template>
  <div class="result-page">
    <!-- Loading -->
    <div v-if="loading" class="loading-state animate-fade-in">
      <div class="loading-card">
        <div class="loading-spinner">
          <div class="spinner-ring"></div>
        </div>
        <p>正在加载批改结果...</p>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error-state animate-scale-in">
      <div class="error-card">
        <div class="error-icon">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
            <circle cx="24" cy="24" r="20" stroke="currentColor" stroke-width="2"/>
            <path d="M24 14V26M24 32V34" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <h2>出错了</h2>
        <p>{{ error }}</p>
        <a-button type="primary" @click="goBack">返回上一页</a-button>
      </div>
    </div>

    <!-- Result -->
    <template v-else-if="gradingResult">
      <header class="page-header animate-fade-in-up">
        <button class="back-btn" @click="goBack">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M12 4L6 10L12 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          返回
        </button>
        <h1>批改结果</h1>
      </header>

      <div class="result-layout">
        <!-- 左侧信息面板 -->
        <aside class="info-panel animate-fade-in-up stagger-1">
          <!-- 得分卡片 -->
          <div class="score-card">
            <div class="score-visual">
              <svg class="score-ring" viewBox="0 0 120 120">
                <circle
                  cx="60" cy="60" r="52"
                  fill="none"
                  stroke="var(--border)"
                  stroke-width="8"
                />
                <circle
                  cx="60" cy="60" r="52"
                  fill="none"
                  :stroke="scoreColor"
                  stroke-width="8"
                  stroke-linecap="round"
                  :stroke-dasharray="`${scorePercent * 3.27} 327`"
                  transform="rotate(-90 60 60)"
                  class="score-progress"
                />
              </svg>
              <div class="score-value">
                <span class="score-num">{{ gradingResult.total_score ?? 0 }}</span>
                <span class="score-divider">/</span>
                <span class="score-max">{{ gradingResult.max_score ?? 10 }}</span>
              </div>
            </div>
            <div class="score-status" :class="statusIcon">
              <svg v-if="statusIcon === 'success'" width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M3 8L6.5 11.5L13 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <svg v-else-if="statusIcon === 'warning'" width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M8 5V8M8 11H8.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M5 5L11 11M11 5L5 11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <span>{{ statusText }}</span>
            </div>
          </div>

          <!-- 反馈卡片 -->
          <div class="feedback-card">
            <h3 class="card-title">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M9 16C13.4183 16 17 12.4183 17 8C17 3.58172 13.4183 0 9 0C4.58172 0 1 3.58172 1 8C1 12.4183 4.58172 16 9 16Z" stroke="currentColor" stroke-width="1.5"/>
                <path d="M9 5V9M9 12H9.01" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              总体反馈
            </h3>
            <p class="feedback-text">{{ gradingResult.feedback || '批改完成' }}</p>
          </div>

          <!-- 建议卡片 -->
          <div v-if="gradingResult.suggestions?.length" class="suggestions-card">
            <h3 class="card-title">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M9 2L10.5 6.5L15 6.5L11.5 9.5L13 14L9 11.5L5 14L6.5 9.5L3 6.5L7.5 6.5L9 2Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
              </svg>
              改进建议
            </h3>
            <ul class="suggestions-list">
              <li v-for="suggestion in gradingResult.suggestions" :key="suggestion" class="suggestion-item">
                {{ suggestion }}
              </li>
            </ul>
          </div>
        </aside>

        <!-- 右侧批改详情 -->
        <main class="detail-panel animate-fade-in-up stagger-2">
          <div class="detail-card">
            <div class="detail-header">
              <h2>分步批改详情</h2>
              <span class="detail-meta">{{ gradingResult.step_results?.length || 0 }} 个步骤</span>
            </div>

            <div class="steps-list">
              <div
                v-for="(step, index) in gradingResult.step_results"
                :key="index"
                class="step-card"
                :class="{ 'is-correct': step.is_correct, 'is-error': !step.is_correct }"
                :style="{ animationDelay: `${index * 80}ms` }"
              >
                <div class="step-header">
                  <div class="step-info">
                    <span class="step-number">{{ index + 1 }}</span>
                    <span class="step-title">{{ step.description }}</span>
                  </div>
                  <div class="step-badge" :class="step.is_correct ? 'correct' : 'error'">
                    <svg v-if="step.is_correct" width="12" height="12" viewBox="0 0 12 12" fill="none">
                      <path d="M2 6L5 9L10 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <svg v-else width="12" height="12" viewBox="0 0 12 12" fill="none">
                      <path d="M3 3L9 9M9 3L3 9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                    {{ step.is_correct ? '正确' : '错误' }}
                  </div>
                </div>

                <div class="step-body">
                  <div class="answer-row">
                    <span class="answer-label">学生答案</span>
                    <p class="answer-text">{{ step.student_answer }}</p>
                  </div>

                  <div class="score-row">
                    <span class="score-label">得分</span>
                    <div class="score-bar">
                      <div
                        class="score-fill"
                        :style="{
                          width: `${(step.score / step.max_score) * 100}%`,
                          backgroundColor: step.is_correct ? 'var(--success)' : 'var(--error)'
                        }"
                      ></div>
                    </div>
                    <span class="score-value">{{ step.score }}/{{ step.max_score }}</span>
                  </div>

                  <div v-if="step.comment" class="comment-row">
                    <span class="comment-label">批注</span>
                    <p class="comment-text">{{ step.comment }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="detail-actions">
              <a-button size="large" @click="goBack">返回</a-button>
              <a-button type="primary" size="large" @click="goUpload">
                <template #icon>
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M8 3V11M8 3L5 6M8 3L11 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </template>
                继续批改
              </a-button>
            </div>
          </div>
        </main>
      </div>
    </template>
  </div>
</template>

<style scoped>
.result-page {
  padding: var(--space-6);
  max-width: 1200px;
  margin: 0 auto;
}

/* Loading */
.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.loading-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
  color: var(--text-secondary);
}

.loading-spinner {
  width: 48px;
  height: 48px;
}

.spinner-ring {
  width: 100%;
  height: 100%;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Error */
.error-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.error-card {
  text-align: center;
  max-width: 320px;
}

.error-icon {
  color: var(--error);
  margin-bottom: var(--space-4);
}

.error-card h2 {
  margin-bottom: var(--space-2);
}

.error-card p {
  color: var(--text-secondary);
  margin-bottom: var(--space-6);
}

/* Page Header */
.page-header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.back-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border: none;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all var(--duration-fast);
}

.back-btn:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.page-header h1 {
  font-size: 1.5rem;
  font-weight: 600;
}

/* Layout */
.result-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: var(--space-6);
}

/* Info Panel */
.info-panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.score-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  text-align: center;
}

.score-visual {
  position: relative;
  width: 140px;
  height: 140px;
  margin: 0 auto var(--space-4);
}

.score-ring {
  width: 100%;
  height: 100%;
}

.score-progress {
  transition: stroke-dasharray 1s var(--ease-out-quart);
}

.score-value {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.score-num {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}

.score-divider {
  font-size: 1.25rem;
  color: var(--text-tertiary);
}

.score-max {
  font-size: 1.25rem;
  color: var(--text-tertiary);
}

.score-status {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  font-weight: 500;
  font-size: 0.875rem;
}

.score-status.success {
  background: rgba(34, 197, 94, 0.1);
  color: var(--success);
}

.score-status.warning {
  background: rgba(249, 115, 22, 0.1);
  color: var(--warning);
}

.score-status.error {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
}

/* Feedback & Suggestions */
.feedback-card,
.suggestions-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
}

.card-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 0.9375rem;
  font-weight: 600;
  margin-bottom: var(--space-3);
  color: var(--text-primary);
}

.feedback-text {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.6;
  max-width: 100%;
}

.suggestions-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.suggestion-item {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  padding-left: var(--space-4);
  position: relative;
}

.suggestion-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--primary);
}

/* Detail Panel */
.detail-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border);
}

.detail-header h2 {
  font-size: 1.125rem;
  font-weight: 600;
}

.detail-meta {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
}

/* Steps List */
.steps-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.step-card {
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  animation: fadeInUp var(--duration-normal) var(--ease-out-quart) forwards;
  opacity: 0;
}

.step-card.is-correct {
  border-left: 3px solid var(--success);
}

.step-card.is-error {
  border-left: 3px solid var(--error);
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-4);
  background: var(--bg-secondary);
}

.step-info {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.step-number {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-full);
  background: var(--bg-elevated);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.step-title {
  font-weight: 500;
  color: var(--text-primary);
}

.step-badge {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 500;
}

.step-badge.correct {
  background: rgba(34, 197, 94, 0.1);
  color: var(--success);
}

.step-badge.error {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
}

.step-body {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.answer-row,
.score-row,
.comment-row {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.answer-label,
.score-label,
.comment-label {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.answer-text {
  font-size: 0.9375rem;
  color: var(--text-primary);
  line-height: 1.6;
  font-family: 'Times New Roman', serif;
}

.score-row {
  flex-direction: row;
  align-items: center;
  gap: var(--space-3);
}

.score-bar {
  flex: 1;
  height: 6px;
  background: var(--bg-secondary);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.score-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width var(--duration-slow) var(--ease-out-quart);
}

.score-value {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
  min-width: 50px;
  text-align: right;
}

.comment-text {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-style: italic;
}

/* Actions */
.detail-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  margin-top: var(--space-6);
  padding-top: var(--space-4);
  border-top: 1px solid var(--border);
}

.detail-actions .ant-btn {
  height: 44px;
  padding: 0 var(--space-6);
  border-radius: var(--radius-md);
}

.detail-actions .ant-btn-primary {
  background: var(--primary);
  border-color: var(--primary);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

/* Animations */
.animate-fade-in {
  animation: fadeIn var(--duration-normal) var(--ease-out-quart) forwards;
}

.animate-scale-in {
  animation: scaleIn var(--duration-normal) var(--ease-spring) forwards;
}

.animate-fade-in-up {
  animation: fadeInUp var(--duration-slow) var(--ease-out-quart) forwards;
  opacity: 0;
}

.stagger-1 { animation-delay: 50ms; }
.stagger-2 { animation-delay: 100ms; }

/* Responsive */
@media (max-width: 768px) {
  .result-page {
    padding: var(--space-4);
  }

  .result-layout {
    grid-template-columns: 1fr;
  }

  .info-panel {
    order: 1;
  }

  .detail-panel {
    order: 0;
  }

  .score-card {
    padding: var(--space-4);
  }

  .score-visual {
    width: 120px;
    height: 120px;
  }

  .score-num {
    font-size: 2rem;
  }
}
</style>

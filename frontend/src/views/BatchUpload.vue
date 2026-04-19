<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { getAnswers, createBatchTask, getBatchStatus } from '@/services/api'
import type { StandardAnswer, BatchResponse } from '@/types/api'

// State
const selectedFiles = ref<File[]>([])
const selectedAnswerId = ref<string>('')
const uploading = ref(false)
const currentBatchId = ref<string | null>(null)
const batchStatus = ref<BatchResponse | null>(null)
const isDragging = ref(false)
const pollingInterval = ref<number | null>(null)

// Options
const answerOptions = ref<{ label: string; value: string }[]>([])
const loadingAnswers = ref(false)

// Computed
const canUpload = computed(() => selectedFiles.value.length > 0 && selectedAnswerId.value && !uploading.value)

const uploadProgress = computed(() => {
  if (!batchStatus.value) return 0
  const { total, completed, failed } = batchStatus.value
  if (total === 0) return 0
  return Math.round(((completed + failed) / total) * 100)
})

const fileList = computed(() =>
  selectedFiles.value.map((file, index) => ({
    id: index,
    name: file.name,
    size: formatFileSize(file.size),
    status: 'pending' as const,
  }))
)

// Methods
function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

function handleDragOver(e: DragEvent) {
  e.preventDefault()
  isDragging.value = true
}

function handleDragLeave() {
  isDragging.value = false
}

function handleDrop(e: DragEvent) {
  e.preventDefault()
  isDragging.value = false
  const files = Array.from(e.dataTransfer?.files || [])
  addFiles(files)
}

function handleFileSelect(e: Event) {
  const input = e.target as HTMLInputElement
  const files = Array.from(input.files || [])
  addFiles(files)
  input.value = ''
}

function addFiles(files: File[]) {
  const imageFiles = files.filter(f => f.type.startsWith('image/'))
  if (imageFiles.length !== files.length) {
    message.warning('已过滤非图片文件')
  }
  selectedFiles.value = [...selectedFiles.value, ...imageFiles].slice(0, 50)
}

function removeFile(index: number) {
  selectedFiles.value.splice(index, 1)
}

function clearAll() {
  selectedFiles.value = []
  selectedAnswerId.value = ''
  batchStatus.value = null
  currentBatchId.value = null
}

async function fetchAnswers() {
  loadingAnswers.value = true
  try {
    const res = await getAnswers({ page: 1, page_size: 100 })
    if (res.data?.items) {
      answerOptions.value = res.data.items.map((a: StandardAnswer) => ({
        label: `${a.question_title} (${a.chapter})`,
        value: a.answer_id,
      }))
    }
  } catch (error: any) {
    message.error(error.message || '获取标准答案失败')
  } finally {
    loadingAnswers.value = false
  }
}

async function startUpload() {
  if (!canUpload.value) return

  uploading.value = true
  try {
    const res = await createBatchTask({
      standard_answer_id: selectedAnswerId.value,
      image_ids: [], // 后端会根据文件重新处理
    })

    if (res.data?.batch_id) {
      currentBatchId.value = res.data.batch_id
      message.success('批量任务已创建，开始处理...')
      startPolling(res.data.batch_id)
    }
  } catch (error: any) {
    message.error(error.message || '创建批量任务失败')
    uploading.value = false
  }
}

function startPolling(batchId: string) {
  stopPolling()
  pollingInterval.value = window.setInterval(async () => {
    try {
      const res = await getBatchStatus(batchId)
      if (res.data) {
        batchStatus.value = res.data
        if (res.data.status === 'completed' || res.data.status === 'failed') {
          stopPolling()
          uploading.value = false
          if (res.data.status === 'completed') {
            message.success(`批量处理完成！成功 ${res.data.completed} 个，失败 ${res.data.failed} 个`)
          } else {
            message.error('批量处理失败')
          }
        }
      }
    } catch (error: any) {
      console.error('轮询状态失败:', error)
    }
  }, 2000)
}

function stopPolling() {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
    pollingInterval.value = null
  }
}

function getStatusType(status: string) {
  switch (status) {
    case 'completed': return 'success'
    case 'failed': return 'exception'
    case 'processing': return 'active'
    default: return 'normal'
  }
}

onMounted(() => {
  fetchAnswers()
})
</script>

<template>
  <div class="batch-upload-page">
    <header class="page-header animate-fade-in-up">
      <div class="header-content">
        <h1>批量上传</h1>
        <p class="header-subtitle">批量处理多张作业图片</p>
      </div>
      <a-button
        v-if="selectedFiles.length > 0"
        type="text"
        danger
        size="large"
        class="clear-btn"
        @click="clearAll"
      >
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M4 6H14M7 6V4C7 3.44772 7.44772 3 8 3H11C11.5523 3 12 3.44772 12 4V6M9 8V13M9 13V14M9 13H7M9 13H11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        清空
      </a-button>
    </header>

    <div class="batch-layout">
      <!-- Left: File Selection -->
      <div class="upload-section animate-fade-in-up stagger-1">
        <div class="section-card">
          <div class="section-header">
            <h2>选择作业图片</h2>
            <span class="file-count">{{ selectedFiles.length }} / 50 张</span>
          </div>

          <!-- Drop Zone -->
          <div
            class="drop-zone"
            :class="{ dragging: isDragging, 'has-files': selectedFiles.length > 0 }"
            @dragover="handleDragOver"
            @dragleave="handleDragLeave"
            @drop="handleDrop"
          >
            <input
              type="file"
              id="file-input"
              accept="image/*"
              multiple
              class="file-input"
              @change="handleFileSelect"
            />
            <label for="file-input" class="drop-content">
              <div class="drop-icon">
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                  <rect x="8" y="12" width="32" height="28" rx="3" stroke="currentColor" stroke-width="2" opacity="0.4"/>
                  <path d="M24 20V32M24 20L18 26M24 20L30 26" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <circle cx="16" cy="22" r="2" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
                </svg>
              </div>
              <p class="drop-text">拖拽图片到这里</p>
              <p class="drop-hint">或点击选择，最多 50 张图片</p>
            </label>
          </div>

          <!-- File List -->
          <div v-if="selectedFiles.length > 0" class="file-list">
            <div
              v-for="(file, index) in fileList"
              :key="file.id"
              class="file-item"
            >
              <div class="file-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <rect x="3" y="4" width="14" height="12" rx="2" stroke="currentColor" stroke-width="1.5"/>
                  <circle cx="7" cy="8" r="1.5" stroke="currentColor" stroke-width="1.2"/>
                  <path d="M6 13L8 10L10 12L13 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="file-info">
                <span class="file-name">{{ file.name }}</span>
                <span class="file-size">{{ file.size }}</span>
              </div>
              <a-button
                type="text"
                size="small"
                class="remove-btn"
                @click="removeFile(index)"
              >
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M4 4L10 10M10 4L4 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </a-button>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Configuration & Progress -->
      <div class="config-section animate-fade-in-up stagger-2">
        <!-- Answer Selection -->
        <div class="section-card">
          <h2>选择标准答案</h2>
          <a-select
            v-model:value="selectedAnswerId"
            :options="answerOptions"
            :loading="loadingAnswers"
            placeholder="请选择标准答案"
            class="answer-select"
            size="large"
            :disabled="uploading"
          />
        </div>

        <!-- Progress Card -->
        <div v-if="batchStatus || uploading" class="section-card progress-card">
          <h2>处理进度</h2>

          <div class="progress-stats">
            <div class="stat-item">
              <span class="stat-value">{{ batchStatus?.total || selectedFiles.length }}</span>
              <span class="stat-label">总数</span>
            </div>
            <div class="stat-item success">
              <span class="stat-value">{{ batchStatus?.completed || 0 }}</span>
              <span class="stat-label">成功</span>
            </div>
            <div class="stat-item error">
              <span class="stat-value">{{ batchStatus?.failed || 0 }}</span>
              <span class="stat-label">失败</span>
            </div>
            <div class="stat-item pending">
              <span class="stat-value">{{ batchStatus?.pending || selectedFiles.length }}</span>
              <span class="stat-label">待处理</span>
            </div>
          </div>

          <a-progress
            :percent="uploadProgress"
            :status="getStatusType(batchStatus?.status || 'processing')"
            :stroke-color="{ '0%': '#4f46e5', '100%': '#818cf8' }"
            class="upload-progress"
          />

          <p class="progress-text">
            <template v-if="uploading">
              正在处理中，请稍候...
            </template>
            <template v-else-if="batchStatus?.status === 'completed'">
              处理完成！
            </template>
            <template v-else-if="batchStatus?.status === 'failed'">
              处理失败，请重试
            </template>
            <template v-else>
              等待开始处理...
            </template>
          </p>
        </div>

        <!-- Upload Button -->
        <a-button
          type="primary"
          size="large"
          class="upload-btn"
          :disabled="!canUpload"
          :loading="uploading"
          @click="startUpload"
        >
          <template #icon>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M10 3V13M10 3L6 7M10 3L14 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M3 15V16C3 16.5523 3.44772 17 4 17H16C16.5523 17 17 16.5523 17 16V15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </template>
          {{ uploading ? '处理中...' : '开始批量处理' }}
        </a-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.batch-upload-page {
  padding: var(--space-6);
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-6);
}

.header-content h1 {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: var(--space-1);
}

.header-subtitle {
  color: var(--text-secondary);
  font-size: 0.9375rem;
}

.clear-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--error);
  height: 44px;
  padding: 0 var(--space-4);
}

/* Layout */
.batch-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: var(--space-6);
}

@media (max-width: 1024px) {
  .batch-layout {
    grid-template-columns: 1fr;
  }
}

/* Section Cards */
.section-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-5);
}

.section-header h2,
.section-card > h2 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.file-count {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
  background: var(--bg-secondary);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
}

/* Drop Zone */
.drop-zone {
  position: relative;
  border: 2px dashed var(--border);
  border-radius: var(--radius-lg);
  transition: all var(--duration-fast) var(--ease-out-quart);
  background: var(--bg-primary);
}

.drop-zone.dragging {
  border-color: var(--primary);
  background: rgba(79, 70, 229, 0.04);
}

.drop-zone.has-files {
  border-style: solid;
  border-color: var(--border-strong);
}

.file-input {
  position: absolute;
  width: 0;
  height: 0;
  opacity: 0;
}

.drop-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-12) var(--space-6);
  cursor: pointer;
  text-align: center;
}

.drop-icon {
  color: var(--text-tertiary);
  margin-bottom: var(--space-4);
  transition: all var(--duration-fast);
}

.drop-zone:hover .drop-icon,
.drop-zone.dragging .drop-icon {
  color: var(--primary);
  transform: translateY(-4px);
}

.drop-text {
  font-size: 1rem;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.drop-hint {
  font-size: 0.875rem;
  color: var(--text-tertiary);
}

/* File List */
.file-list {
  margin-top: var(--space-4);
  max-height: 320px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.file-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  animation: fadeInUp var(--duration-fast) var(--ease-out-quart) forwards;
}

.file-icon {
  color: var(--primary);
  flex-shrink: 0;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-size {
  font-size: 0.75rem;
  color: var(--text-tertiary);
}

.remove-btn {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
}

.remove-btn:hover {
  color: var(--error);
  background: rgba(239, 68, 68, 0.08);
}

/* Answer Select */
.answer-select {
  width: 100%;
  margin-top: var(--space-4);
}

/* Progress Card */
.progress-card {
  margin-top: var(--space-4);
}

.progress-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-3);
  margin: var(--space-5) 0;
}

.stat-item {
  text-align: center;
  padding: var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.stat-item .stat-value {
  display: block;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-item.success .stat-value {
  color: var(--success);
}

.stat-item.error .stat-value {
  color: var(--error);
}

.stat-item.pending .stat-value {
  color: var(--text-tertiary);
}

.stat-item .stat-label {
  font-size: 0.6875rem;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.upload-progress {
  margin: var(--space-4) 0;
}

.progress-text {
  text-align: center;
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: var(--space-2);
}

/* Upload Button */
.upload-btn {
  width: 100%;
  height: 52px;
  margin-top: var(--space-4);
  border-radius: var(--radius-lg);
  font-size: 1rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  background: var(--primary);
  border-color: var(--primary);
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
  transition: all var(--duration-fast) var(--ease-out-quart);
}

.upload-btn:not(:disabled):hover {
  background: var(--primary-dark);
  border-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.35);
}

/* Animations */
.animate-fade-in-up {
  animation: fadeInUp var(--duration-slow) var(--ease-out-quart) forwards;
  opacity: 0;
}

.stagger-1 { animation-delay: 50ms; }
.stagger-2 { animation-delay: 100ms; }

/* Responsive */
@media (max-width: 768px) {
  .batch-upload-page {
    padding: var(--space-4);
  }

  .page-header {
    flex-direction: column;
    gap: var(--space-4);
  }

  .clear-btn {
    width: 100%;
    justify-content: center;
  }

  .progress-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>

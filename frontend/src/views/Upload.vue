<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import type { UploadFile } from 'ant-design-vue'
import { uploadImage, submitGrading, getGradingStatus, getAnswers } from '@/services/api'
import type { StandardAnswer } from '@/types/api'

const router = useRouter()

const fileList = ref<UploadFile[]>([])
const standardAnswerId = ref<string>('')
const gradingId = ref<string>('')

// 批改进度状态
const uploading = ref(false)
const currentStep = ref(0)
const steps = ['上传', '预处理', '识别', '批改', '完成']
const stepStatus = ref<Array<'wait' | 'process' | 'finish' | 'error'>>(['wait', 'wait', 'wait', 'wait', 'wait'])

// 标准答案列表
const standardAnswers = ref<Array<{ value: string; label: string }>>([])

// 轮询定时器
let statusPollTimer: number | null = null

onMounted(async () => {
  try {
    const res = await getAnswers({ page: 1, page_size: 100 })
    if (res.data?.items) {
      standardAnswers.value = res.data.items.map((ans: StandardAnswer) => ({
        value: ans.answer_id,
        label: ans.question_title,
      }))
    }
  } catch (error: any) {
    standardAnswers.value = [
      { value: 'ans_001', label: '斜面物体受力分析' },
      { value: 'ans_002', label: '匀变速直线运动' },
    ]
  }
})

onUnmounted(() => {
  if (statusPollTimer) {
    clearInterval(statusPollTimer)
  }
})

function beforeUpload(file: File) {
  const isImage = file.type.startsWith('image/')
  const isPdf = file.type === 'application/pdf'
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage && !isPdf) {
    message.error('只能上传图片或 PDF 文件')
    return false
  }

  if (!isLt10M) {
    message.error('文件大小不能超过 10MB')
    return false
  }

  return true
}

function handleFileChange(info: any) {
  fileList.value = info.fileList
}

async function handleUpload() {
  if (fileList.value.length === 0) {
    message.warning('请先选择文件')
    return
  }

  const firstFile = fileList.value[0]
  const file = firstFile.originFileObj as File | undefined
  if (!file) {
    message.error('文件无效')
    return
  }

  if (!standardAnswerId.value) {
    message.warning('请选择标准答案')
    return
  }

  uploading.value = true
  currentStep.value = 0
  stepStatus.value = ['process', 'wait', 'wait', 'wait', 'wait']

  try {
    const uploadRes = await uploadImage(file)
    const imageId = uploadRes.data?.image_id
    if (!imageId) {
      throw new Error('上传失败：未获取到图片ID')
    }
    stepStatus.value[0] = 'finish'
    currentStep.value = 1
    stepStatus.value[1] = 'process'

    await new Promise(resolve => setTimeout(resolve, 800))
    stepStatus.value[1] = 'finish'
    currentStep.value = 2
    stepStatus.value[2] = 'process'

    await new Promise(resolve => setTimeout(resolve, 800))
    stepStatus.value[2] = 'finish'
    currentStep.value = 3
    stepStatus.value[3] = 'process'

    const gradingRes = await submitGrading({
      image_id: imageId,
      standard_answer_id: standardAnswerId.value,
    })
    const grdId = gradingRes.data?.grading_id
    if (!grdId) {
      throw new Error('提交失败：未获取到批改ID')
    }
    gradingId.value = grdId

    startStatusPolling(grdId)
  } catch (error: any) {
    message.error(error.message || '上传失败')
    uploading.value = false
    stepStatus.value = ['error', 'error', 'error', 'error', 'error']
  }
}

function startStatusPolling(grdId: string) {
  statusPollTimer = window.setInterval(async () => {
    try {
      const res = await getGradingStatus(grdId)

      const progress = res.data?.progress ?? 0
      if (progress >= 100) {
        clearInterval(statusPollTimer!)
        statusPollTimer = null
        stepStatus.value[3] = 'finish'
        currentStep.value = 4
        stepStatus.value[4] = 'finish'

        uploading.value = false
        message.success('批改完成')
        router.push(`/result/${grdId}`)
      }
    } catch (error) {
      console.error('轮询状态失败:', error)
    }
  }, 1000)
}
</script>

<template>
  <div class="upload-page">
    <header class="page-header animate-fade-in-up">
      <div class="header-content">
        <h1>上传作业</h1>
        <p class="header-subtitle">拍摄或选择作业照片，AI 将自动批改</p>
      </div>
    </header>

    <div class="upload-layout">
      <!-- 左侧：上传表单 -->
      <div class="upload-form-section animate-fade-in-up stagger-1">
        <div class="form-card">
          <a-form layout="vertical" class="upload-form">
            <!-- 标准答案选择 -->
            <a-form-item label="标准答案" class="form-item">
              <template #label>
                <span class="custom-label">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M3 4H13M3 8H10M3 12H7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  选择标准答案
                </span>
              </template>
              <a-select
                v-model:value="standardAnswerId"
                placeholder="请选择标准答案用于批改"
                :options="standardAnswers"
                :loading="!standardAnswers.length"
                size="large"
                class="custom-select"
              />
            </a-form-item>

            <!-- 文件上传 -->
            <a-form-item label="上传作业" class="form-item">
              <template #label>
                <span class="custom-label">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <rect x="2" y="3" width="12" height="10" rx="2" stroke="currentColor" stroke-width="1.5"/>
                    <circle cx="8" cy="8" r="2" stroke="currentColor" stroke-width="1.5"/>
                  </svg>
                  上传作业文件
                </span>
              </template>

              <a-upload
                v-model:file-list="fileList"
                :before-upload="beforeUpload"
                :max-count="1"
                list-type="picture"
                @change="handleFileChange"
                class="custom-upload"
              >
                <div class="upload-trigger">
                  <div class="upload-icon">
                    <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                      <path d="M16 8V22M16 8L12 12M16 8L20 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M6 24V26C6 26.5523 6.44772 27 7 27H25C25.5523 27 26 26.5523 26 26V24" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                  </div>
                  <div class="upload-text">
                    <span class="upload-title">点击或拖拽文件到此区域</span>
                    <span class="upload-hint">支持 JPG、PNG、PDF 格式，单个文件不超过 10MB</span>
                  </div>
                </div>
              </a-upload>
            </a-form-item>

            <!-- 提交按钮 -->
            <a-form-item class="submit-item">
              <a-button
                type="primary"
                size="large"
                block
                :loading="uploading"
                :disabled="fileList.length === 0 || !standardAnswerId"
                @click="handleUpload"
                class="submit-btn"
              >
                <template v-if="!uploading">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M10 3V13M10 3L6 7M10 3L14 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </template>
                {{ uploading ? '处理中...' : '开始批改' }}
              </a-button>
            </a-form-item>
          </a-form>

          <!-- 进度指示 -->
          <div v-if="uploading" class="progress-section">
            <div class="progress-header">
              <span class="progress-title">批改进度</span>
              <span class="progress-percent">{{ Math.min(currentStep * 25 + 10, 100) }}%</span>
            </div>
            <div class="steps-track">
              <div
                v-for="(step, index) in steps"
                :key="step"
                class="step-item"
                :class="{
                  'is-finish': stepStatus[index] === 'finish',
                  'is-process': stepStatus[index] === 'process',
                  'is-error': stepStatus[index] === 'error',
                }"
              >
                <div class="step-dot">
                  <svg v-if="stepStatus[index] === 'finish'" width="12" height="12" viewBox="0 0 12 12" fill="none">
                    <path d="M2.5 6L5 8.5L9.5 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <div v-else-if="stepStatus[index] === 'process'" class="step-spinner"></div>
                </div>
                <span class="step-label">{{ step }}</span>
                <div v-if="index < steps.length - 1" class="step-line"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：说明卡片 -->
      <div class="upload-tips-section animate-fade-in-up stagger-2">
        <div class="tips-card">
          <h3 class="tips-title">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.5"/>
              <path d="M10 6V10M10 14H10.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            上传须知
          </h3>
          <ul class="tips-list">
            <li class="tips-item">
              <span class="tips-icon success">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M2.5 7L5.5 10L11.5 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              <span>确保照片清晰，光线充足</span>
            </li>
            <li class="tips-item">
              <span class="tips-icon success">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M2.5 7L5.5 10L11.5 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              <span>文字方向正确，不要倾斜</span>
            </li>
            <li class="tips-item">
              <span class="tips-icon success">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M2.5 7L5.5 10L11.5 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              <span>单张图片不超过 10MB</span>
            </li>
            <li class="tips-item">
              <span class="tips-icon warning">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M7 4V7M7 10H7.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </span>
              <span>请提前准备好标准答案</span>
            </li>
          </ul>
        </div>

        <div class="tips-card">
          <h3 class="tips-title">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M10 2L12.5 7.5L18 8L14 12L15 18L10 15L5 18L6 12L2 8L7.5 7.5L10 2Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
            </svg>
            AI 批改优势
          </h3>
          <ul class="tips-list">
            <li class="tips-item">
              <span class="tips-icon primary">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M2.5 7L5.5 10L11.5 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              <span>秒级完成批改</span>
            </li>
            <li class="tips-item">
              <span class="tips-icon primary">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M2.5 7L5.5 10L11.5 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              <span>详细步骤评分</span>
            </li>
            <li class="tips-item">
              <span class="tips-icon primary">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M2.5 7L5.5 10L11.5 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              <span>个性化改进建议</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.upload-page {
  padding: var(--space-6);
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: var(--space-8);
}

.header-content h1 {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: var(--space-1);
}

.header-subtitle {
  color: var(--text-secondary);
  font-size: 0.9375rem;
  max-width: 100%;
}

.upload-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: var(--space-6);
}

/* 表单卡片 */
.form-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: var(--space-8);
}

.upload-form :deep(.ant-form-item) {
  margin-bottom: var(--space-6);
}

.custom-label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-weight: 500;
  color: var(--text-primary);
}

.custom-select {
  height: 48px;
}

.custom-select :deep(.ant-select-selector) {
  height: 48px !important;
  border-radius: var(--radius-md) !important;
  border-color: var(--border) !important;
}

.custom-select :deep(.ant-select-selector:hover) {
  border-color: var(--primary) !important;
}

/* 上传区域 */
.custom-upload {
  width: 100%;
}

.upload-trigger {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  padding: var(--space-8);
  border: 2px dashed var(--border);
  border-radius: var(--radius-lg);
  background: var(--bg-primary);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out-quart);
}

.upload-trigger:hover {
  border-color: var(--primary);
  background: rgba(79, 70, 229, 0.04);
}

.upload-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-lg);
  background: rgba(79, 70, 229, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
}

.upload-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
  text-align: center;
}

.upload-title {
  font-weight: 500;
  color: var(--text-primary);
}

.upload-hint {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
}

/* 提交按钮 */
.submit-item {
  margin-bottom: 0;
  margin-top: var(--space-6);
}

.submit-btn {
  height: 52px;
  font-size: 1rem;
  font-weight: 500;
  border-radius: var(--radius-md);
  background: var(--primary);
  border-color: var(--primary);
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  transition: all var(--duration-fast) var(--ease-out-quart);
}

.submit-btn:hover:not(:disabled) {
  background: var(--primary-dark);
  border-color: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
}

.submit-btn:disabled {
  background: var(--bg-secondary);
  border-color: var(--border);
  color: var(--text-tertiary);
}

/* 进度指示 */
.progress-section {
  margin-top: var(--space-8);
  padding-top: var(--space-6);
  border-top: 1px solid var(--border);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.progress-title {
  font-weight: 500;
  color: var(--text-primary);
}

.progress-percent {
  font-size: 0.875rem;
  color: var(--primary);
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.steps-track {
  display: flex;
  justify-content: space-between;
  position: relative;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  position: relative;
  flex: 1;
}

.step-dot {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-full);
  background: var(--bg-secondary);
  border: 2px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--duration-fast) var(--ease-out-quart);
  z-index: 1;
}

.step-item.is-finish .step-dot {
  background: var(--success);
  border-color: var(--success);
  color: white;
}

.step-item.is-process .step-dot {
  border-color: var(--primary);
  background: rgba(79, 70, 229, 0.1);
}

.step-item.is-error .step-dot {
  background: var(--error);
  border-color: var(--error);
  color: white;
}

.step-spinner {
  width: 12px;
  height: 12px;
  border: 2px solid var(--primary);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.step-label {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
  transition: color var(--duration-fast);
}

.step-item.is-finish .step-label,
.step-item.is-process .step-label {
  color: var(--text-primary);
}

.step-line {
  position: absolute;
  top: 14px;
  left: calc(50% + 16px);
  right: calc(-50% + 16px);
  height: 2px;
  background: var(--border);
}

.step-item.is-finish .step-line {
  background: var(--success);
}

/* 提示卡片 */
.tips-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  margin-bottom: var(--space-4);
}

.tips-card:last-child {
  margin-bottom: 0;
}

.tips-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 0.9375rem;
  font-weight: 600;
  margin-bottom: var(--space-4);
  color: var(--text-primary);
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.tips-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: 0.8125rem;
  color: var(--text-secondary);
}

.tips-icon {
  width: 20px;
  height: 20px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tips-icon.success {
  background: rgba(34, 197, 94, 0.1);
  color: var(--success);
}

.tips-icon.warning {
  background: rgba(249, 115, 22, 0.1);
  color: var(--warning);
}

.tips-icon.primary {
  background: rgba(79, 70, 229, 0.1);
  color: var(--primary);
}

/* 动画 */
.animate-fade-in-up {
  animation: fadeInUp var(--duration-slow) var(--ease-out-quart) forwards;
  opacity: 0;
}

.stagger-1 { animation-delay: 50ms; }
.stagger-2 { animation-delay: 100ms; }

/* 响应式 */
@media (max-width: 768px) {
  .upload-page {
    padding: var(--space-4);
  }

  .upload-layout {
    grid-template-columns: 1fr;
  }

  .form-card {
    padding: var(--space-5);
  }

  .steps-track {
    gap: var(--space-2);
  }

  .step-label {
    font-size: 0.6875rem;
  }
}
</style>

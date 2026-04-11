<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Upload, message, Select, Spin } from 'ant-design-vue'
import type { UploadFile } from 'ant-design-vue'

const router = useRouter()

const fileList = ref<UploadFile[]>([])
const standardAnswerId = ref<string>('')
const loading = ref(false)
const gradingId = ref<string>('')

const standardAnswers = ref([
  { value: 'ans_001', label: '斜面物体受力分析' },
  { value: 'ans_002', label: '匀变速直线运动' },
])

const uploading = ref(false)
const currentStep = ref(0)
const steps = ['上传', '预处理', '识别', '批改', '完成']

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

  if (!standardAnswerId.value) {
    message.warning('请选择标准答案')
    return
  }

  uploading.value = true
  currentStep.value = 0

  // 模拟批改流程
  for (let i = 0; i < steps.length; i++) {
    currentStep.value = i
    await new Promise(resolve => setTimeout(resolve, 800))
  }

  gradingId.value = 'grd_' + Math.random().toString(36).substr(2, 12)
  uploading.value = false
  message.success('批改完成')

  router.push(`/result/${gradingId.value}`)
}
</script>

<template>
  <div class="upload-page">
    <h1>上传作业</h1>

    <a-card class="upload-card">
      <a-form layout="vertical">
        <a-form-item label="标准答案" required>
          <a-select
            v-model:value="standardAnswerId"
            placeholder="请选择标准答案"
            :options="standardAnswers"
          />
        </a-form-item>

        <a-form-item label="上传作业文件">
          <a-upload
            v-model:file-list="fileList"
            :before-upload="beforeUpload"
            :max-count="1"
            list-type="picture"
            @change="handleFileChange"
          >
            <a-button>
              <UploadOutlined /> 选择文件
            </a-button>
          </a-upload>
          <div class="upload-hint">支持 JPG、PNG、PDF 格式，单个文件不超过 10MB</div>
        </a-form-item>

        <a-form-item>
          <a-button
            type="primary"
            size="large"
            :loading="uploading"
            :disabled="fileList.length === 0 || !standardAnswerId"
            @click="handleUpload"
          >
            {{ uploading ? '处理中...' : '开始批改' }}
          </a-button>
        </a-form-item>
      </a-form>

      <div v-if="uploading" class="progress-section">
        <a-steps :current="currentStep" size="small">
          <a-step v-for="step in steps" :key="step" :title="step" />
        </a-steps>
        <div class="current-step">{{ steps[currentStep] }}中...</div>
      </div>
    </a-card>
  </div>
</template>

<style scoped>
.upload-page h1 {
  margin-bottom: 24px;
}

.upload-card {
  max-width: 600px;
}

.upload-hint {
  margin-top: 8px;
  color: #8c8c8c;
  font-size: 12px;
}

.progress-section {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

.current-step {
  text-align: center;
  margin-top: 16px;
  color: #1890ff;
}
</style>

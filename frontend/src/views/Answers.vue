<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { getAnswers, createAnswer, updateAnswer, deleteAnswer } from '@/services/api'
import type { StandardAnswer, AnswerStep } from '@/types/api'

const columns = [
  { title: '题目', dataIndex: 'question_title', key: 'question_title' },
  { title: '学科', dataIndex: 'subject', key: 'subject' },
  { title: '年级', dataIndex: 'grade', key: 'grade' },
  { title: '章节', dataIndex: 'chapter', key: 'chapter' },
  { title: '总分', dataIndex: 'total_score', key: 'total_score', width: 80 },
  { title: '操作', key: 'action', width: 120 },
]

const data = ref<StandardAnswer[]>([])
const loading = ref(false)

const visible = ref(false)
const modalLoading = ref(false)
const isEdit = ref(false)
const currentAnswerId = ref<string | null>(null)

const formRef = ref()
const form = ref({
  question_title: '',
  subject: '物理',
  grade: '高一',
  chapter: '',
  steps: [{ order: 1, description: '', content: '', formula: '', score: 0 } as AnswerStep],
  total_score: 10,
  tags: [] as string[],
})

const subjectOptions = [
  { value: '物理', label: '物理' },
]

const gradeOptions = [
  { value: '高一', label: '高一' },
  { value: '高二', label: '高二' },
  { value: '高三', label: '高三' },
]

async function fetchData() {
  loading.value = true
  try {
    const res = await getAnswers({ page: 1, page_size: 100 })
    if (res.data?.items) {
      data.value = res.data.items
    }
  } catch (error: any) {
    message.error(error.message || '获取数据失败')
  } finally {
    loading.value = false
  }
}

function initForm() {
  form.value = {
    question_title: '',
    subject: '物理',
    grade: '高一',
    chapter: '',
    steps: [{ order: 1, description: '', content: '', formula: '', score: 0 }],
    total_score: 10,
    tags: [],
  }
  currentAnswerId.value = null
  isEdit.value = false
}

function handleCreate() {
  initForm()
  visible.value = true
}

function handleEdit(record: StandardAnswer | Record<string, any>) {
  const ans = record as StandardAnswer
  currentAnswerId.value = ans.answer_id
  isEdit.value = true
  form.value = {
    question_title: ans.question_title,
    subject: ans.subject,
    grade: ans.grade,
    chapter: ans.chapter,
    steps: [...ans.steps],
    total_score: ans.total_score,
    tags: ans.tags || [],
  }
  visible.value = true
}

async function handleDelete(answerId: string) {
  try {
    await deleteAnswer(answerId)
    message.success('删除成功')
    fetchData()
  } catch (error: any) {
    message.error(error.message || '删除失败')
  }
}

function addStep() {
  const newOrder = form.value.steps.length + 1
  form.value.steps.push({
    order: newOrder,
    description: '',
    content: '',
    formula: '',
    score: 0,
  })
  updateTotalScore()
}

function removeStep(index: number) {
  if (form.value.steps.length <= 1) {
    message.warning('至少需要一个步骤')
    return
  }
  form.value.steps.splice(index, 1)
  form.value.steps.forEach((step, i) => {
    step.order = i + 1
  })
  updateTotalScore()
}

function updateTotalScore() {
  form.value.total_score = form.value.steps.reduce((sum, step) => sum + (step.score || 0), 0)
}

function onScoreChange() {
  updateTotalScore()
}

async function handleSubmit() {
  try {
    await formRef.value.validate()

    modalLoading.value = true

    const submitData = {
      question_title: form.value.question_title,
      subject: form.value.subject,
      grade: form.value.grade,
      chapter: form.value.chapter,
      steps: form.value.steps.filter(s => s.description && s.content),
      total_score: form.value.total_score,
      tags: form.value.tags,
    }

    if (isEdit.value && currentAnswerId.value) {
      await updateAnswer(currentAnswerId.value, submitData)
      message.success('更新成功')
    } else {
      await createAnswer(submitData)
      message.success('创建成功')
    }

    visible.value = false
    fetchData()
  } catch (error: any) {
    if (error.message) {
      message.error(error.message)
    }
  } finally {
    modalLoading.value = false
  }
}

function handleCancel() {
  visible.value = false
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="answers-page">
    <header class="page-header animate-fade-in-up">
      <div class="header-content">
        <h1>标准答案管理</h1>
        <p class="header-subtitle">管理题目与评分标准</p>
      </div>
      <a-button type="primary" size="large" class="create-btn" @click="handleCreate">
        <template #icon>
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path d="M9 3V15M3 9H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </template>
        新建答案
      </a-button>
    </header>

    <div class="table-card animate-fade-in-up stagger-1">
      <a-table
        :columns="columns"
        :data-source="data"
        :loading="loading"
        row-key="answer_id"
        :pagination="{ pageSize: 10 }"
        class="custom-table"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <a-button type="link" size="small" class="action-edit" @click="handleEdit(record)">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M10 2L12 4L5 11H3V9L10 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                编辑
              </a-button>
              <a-popconfirm
                title="确定删除这条标准答案？"
                ok-text="确定"
                cancel-text="取消"
                @confirm="handleDelete(record.answer_id)"
              >
                <a-button type="link" danger size="small" class="action-delete">
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M3 4H11M5 4V3C5 2.44772 5.44772 2 6 2H8C8.55228 2 9 2.44772 9 3V4M10 4V11C10 11.5523 9.55228 12 9 12H5C4.44772 12 4 11.5523 4 11V4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  删除
                </a-button>
              </a-popconfirm>
            </a-space>
          </template>
        </template>

        <template #emptyText>
          <div class="empty-state">
            <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
              <rect x="8" y="12" width="48" height="40" rx="4" stroke="currentColor" stroke-width="2" opacity="0.3"/>
              <path d="M20 24H44M20 32H36M20 40H28" stroke="currentColor" stroke-width="2" stroke-linecap="round" opacity="0.3"/>
            </svg>
            <p>暂无标准答案</p>
            <a-button type="primary" @click="handleCreate">创建第一个答案</a-button>
          </div>
        </template>
      </a-table>
    </div>

    <!-- Modal -->
    <a-modal
      v-model:open="visible"
      :title="isEdit ? '编辑标准答案' : '新建标准答案'"
      width="720px"
      :footer="null"
      @cancel="handleCancel"
      class="answer-modal"
    >
      <a-form
        ref="formRef"
        :model="form"
        layout="vertical"
        @finish="handleSubmit"
        class="answer-form"
      >
        <div class="form-grid">
          <a-form-item
            label="题目名称"
            name="question_title"
            :rules="[{ required: true, message: '请输入题目名称' }]"
            class="full-width"
          >
            <a-input v-model:value="form.question_title" placeholder="请输入题目名称" size="large" />
          </a-form-item>

          <a-form-item label="总分" name="total_score" class="score-field">
            <a-input-number
              v-model:value="form.total_score"
              :min="0"
              :max="200"
              disabled
              size="large"
              class="score-input"
            />
          </a-form-item>

          <a-form-item label="学科" name="subject" class="subject-field">
            <a-select v-model:value="form.subject" :options="subjectOptions" size="large" />
          </a-form-item>

          <a-form-item label="年级" name="grade" class="grade-field">
            <a-select v-model:value="form.grade" :options="gradeOptions" size="large" />
          </a-form-item>

          <a-form-item
            label="章节"
            name="chapter"
            :rules="[{ required: true, message: '请输入章节' }]"
            class="chapter-field"
          >
            <a-input v-model:value="form.chapter" placeholder="如：牛顿定律" size="large" />
          </a-form-item>
        </div>

        <a-divider class="step-divider">解题步骤</a-divider>

        <div class="steps-container">
          <div
            v-for="(step, index) in form.steps"
            :key="index"
            class="step-item"
            :class="{ 'is-first': index === 0 }"
          >
            <div class="step-header">
              <span class="step-number">{{ step.order }}</span>
              <span class="step-label">步骤</span>
            </div>
            <div class="step-fields">
              <a-form-item
                :name="['steps', index, 'description']"
                :rules="[{ required: true, message: '请输入步骤描述' }]"
                class="desc-field"
              >
                <a-input v-model:value="step.description" placeholder="步骤描述，如：受力分析" />
              </a-form-item>
              <a-form-item
                :name="['steps', index, 'content']"
                :rules="[{ required: true, message: '请输入答案内容' }]"
                class="content-field"
              >
                <a-input v-model:value="step.content" placeholder="答案内容" />
              </a-form-item>
              <a-form-item
                :name="['steps', index, 'score']"
                :rules="[{ required: true, message: '请输入分数' }]"
                class="score-field"
              >
                <a-input-number
                  v-model:value="step.score"
                  :min="0"
                  :max="100"
                  placeholder="分数"
                  @change="onScoreChange"
                  class="step-score"
                />
              </a-form-item>
              <a-button
                type="text"
                danger
                class="remove-btn"
                @click="removeStep(index)"
                :disabled="form.steps.length <= 1"
              >
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M4 8H12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </a-button>
            </div>
          </div>

          <button type="button" class="add-step-btn" @click="addStep">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M8 3V13M3 8H13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            添加步骤
          </button>
        </div>

        <div class="form-actions">
          <a-button @click="handleCancel">取消</a-button>
          <a-button type="primary" html-type="submit" :loading="modalLoading" class="submit-btn">
            {{ isEdit ? '保存' : '创建' }}
          </a-button>
        </div>
      </a-form>
    </a-modal>
  </div>
</template>

<style scoped>
.answers-page {
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
  max-width: 100%;
}

.create-btn {
  height: 44px;
  padding: 0 var(--space-6);
  border-radius: var(--radius-md);
  background: var(--primary);
  border-color: var(--primary);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25);
  transition: all var(--duration-fast) var(--ease-out-quart);
}

.create-btn:hover {
  background: var(--primary-dark);
  border-color: var(--primary-dark);
  transform: translateY(-1px);
}

/* Table */
.table-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.custom-table :deep(.ant-table-thead > tr > th) {
  background: var(--bg-secondary);
  font-weight: 600;
  font-size: 0.8125rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--text-secondary);
}

.custom-table :deep(.ant-table-tbody > tr > td) {
  padding: var(--space-4) var(--space-5);
}

.custom-table :deep(.ant-table-tbody > tr:hover > td) {
  background: var(--bg-secondary);
}

.action-edit,
.action-delete {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1) var(--space-2);
  height: auto;
}

.action-edit {
  color: var(--primary);
}

.action-delete {
  color: var(--error);
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-12) var(--space-4);
  color: var(--text-tertiary);
}

.empty-state p {
  margin: var(--space-4) 0;
  color: var(--text-secondary);
}

/* Modal */
.answer-modal :deep(.ant-modal-content) {
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.answer-modal :deep(.ant-modal-header) {
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--border);
}

.answer-modal :deep(.ant-modal-title) {
  font-size: 1.125rem;
  font-weight: 600;
}

.answer-modal :deep(.ant-modal-body) {
  padding: var(--space-6);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 120px 100px 100px 1fr;
  gap: var(--space-4);
  align-items: start;
}

.full-width {
  grid-column: 1 / -1;
}

.score-field {
  width: 100px;
}

.score-input {
  width: 100%;
}

.step-divider {
  margin: var(--space-6) 0;
  border-color: var(--border);
}

.step-divider::before,
.step-divider::after {
  border-color: var(--border);
}

/* Steps */
.steps-container {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.step-item {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  transition: border-color var(--duration-fast);
}

.step-item:hover {
  border-color: var(--primary);
}

.step-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
  min-width: 48px;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
}

.step-label {
  font-size: 0.6875rem;
  color: var(--text-tertiary);
  text-transform: uppercase;
}

.step-fields {
  display: flex;
  flex: 1;
  gap: var(--space-3);
  align-items: flex-start;
}

.desc-field {
  flex: 1;
}

.content-field {
  flex: 2;
}

.step-score {
  width: 80px;
}

.remove-btn {
  width: 32px;
  height: 32px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 4px;
}

.add-step-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  width: 100%;
  padding: var(--space-4);
  border: 2px dashed var(--border);
  border-radius: var(--radius-lg);
  background: transparent;
  color: var(--text-secondary);
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--duration-fast);
}

.add-step-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
  background: rgba(79, 70, 229, 0.04);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  margin-top: var(--space-6);
  padding-top: var(--space-4);
  border-top: 1px solid var(--border);
}

.submit-btn {
  min-width: 100px;
  height: 40px;
  background: var(--primary);
  border-color: var(--primary);
}

/* Animations */
.animate-fade-in-up {
  animation: fadeInUp var(--duration-slow) var(--ease-out-quart) forwards;
  opacity: 0;
}

.stagger-1 { animation-delay: 50ms; }

/* Responsive */
@media (max-width: 768px) {
  .answers-page {
    padding: var(--space-4);
  }

  .page-header {
    flex-direction: column;
    gap: var(--space-4);
  }

  .create-btn {
    width: 100%;
    justify-content: center;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .step-fields {
    flex-wrap: wrap;
  }

  .desc-field,
  .content-field {
    flex: 1 1 100%;
  }
}
</style>

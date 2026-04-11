<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getHistory } from '@/services/api'

const router = useRouter()

const columns = [
  { title: '批改ID', dataIndex: 'grading_id', key: 'grading_id', align: 'center' },
  { title: '学生姓名', dataIndex: 'student_name', key: 'student_name', align: 'center' },
  { title: '题目', dataIndex: 'question_title', key: 'question_title', align: 'center' },
  { title: '得分', key: 'total_score', width: 100, align: 'center' },
  { title: '批改时间', dataIndex: 'created_at', key: 'created_at', align: 'center' },
  { title: '操作', key: 'action', width: 100, align: 'center' },
]

const data = ref<any[]>([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const res = await getHistory({ page: 1, page_size: 50 })
    if (res.data?.items) {
      data.value = res.data.items
    }
  } catch (error) {
    // Mock data on error
    data.value = [
      {
        grading_id: 'grd_001',
        student_name: '张三',
        question_title: '斜面物体受力分析',
        total_score: 8.5,
        max_score: 10,
        created_at: '2026-04-11 14:30:00',
      },
      {
        grading_id: 'grd_002',
        student_name: '李四',
        question_title: '匀变速直线运动',
        total_score: 7.0,
        max_score: 10,
        created_at: '2026-04-11 14:35:00',
      },
    ]
  } finally {
    loading.value = false
  }
})

function viewResult(record: any) {
  router.push(`/result/${record.grading_id}`)
}

function getScoreType(record: any): 'success' | 'warning' | 'error' {
  const percent = (record.total_score / record.max_score) * 100
  if (percent >= 75) return 'success'
  if (percent >= 60) return 'warning'
  return 'error'
}
</script>

<template>
  <div class="history-page">
    <header class="page-header animate-fade-in-up">
      <div class="header-content">
        <h1>批改历史</h1>
        <p class="header-subtitle">查看所有批改记录</p>
      </div>
    </header>

    <div class="table-card animate-fade-in-up stagger-1">
      <a-table
        :columns="columns"
        :data-source="data"
        :loading="loading"
        row-key="grading_id"
        class="custom-table"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'total_score'">
            <div class="score-cell" :class="getScoreType(record)">
              <span class="score-value">{{ record.total_score }}</span>
              <span class="score-divider">/</span>
              <span class="score-max">{{ record.max_score }}</span>
            </div>
          </template>
          <template v-if="column.key === 'action'">
            <a-button type="link" size="small" class="action-btn" @click="viewResult(record)">
              查看详情
            </a-button>
          </template>
        </template>

        <template #emptyText>
          <div class="empty-state">
            <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
              <circle cx="32" cy="32" r="24" stroke="currentColor" stroke-width="2" opacity="0.3"/>
              <path d="M32 20V34" stroke="currentColor" stroke-width="2" stroke-linecap="round" opacity="0.3"/>
              <path d="M32 40V42" stroke="currentColor" stroke-width="2" stroke-linecap="round" opacity="0.3"/>
            </svg>
            <p>暂无批改记录</p>
          </div>
        </template>
      </a-table>
    </div>
  </div>
</template>

<style scoped>
.history-page {
  padding: var(--space-6);
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
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
  padding: var(--space-5) var(--space-6);
}

.custom-table :deep(.ant-table-tbody > tr:hover > td) {
  background: var(--bg-secondary);
}

/* Score Cell */
.score-cell {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  font-variant-numeric: tabular-nums;
}

.score-cell.success {
  background: rgba(34, 197, 94, 0.1);
}

.score-cell.success .score-value {
  color: var(--success);
  font-weight: 600;
}

.score-cell.warning {
  background: rgba(249, 115, 22, 0.1);
}

.score-cell.warning .score-value {
  color: var(--warning);
  font-weight: 600;
}

.score-cell.error {
  background: rgba(239, 68, 68, 0.1);
}

.score-cell.error .score-value {
  color: var(--error);
  font-weight: 600;
}

.score-divider,
.score-max {
  color: var(--text-tertiary);
  font-size: 0.8125rem;
}

.action-btn {
  color: var(--primary);
  padding: var(--space-1) var(--space-2);
  height: auto;
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
  margin-top: var(--space-4);
  color: var(--text-secondary);
}

/* Animations */
.animate-fade-in-up {
  animation: fadeInUp var(--duration-slow) var(--ease-out-quart) forwards;
  opacity: 0;
}

.stagger-1 { animation-delay: 50ms; }

/* Responsive */
@media (max-width: 768px) {
  .history-page {
    padding: var(--space-4);
  }
}
</style>

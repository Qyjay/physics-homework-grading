<script setup lang="ts">
import { ref } from 'vue'

const columns = [
  { title: '班级名称', dataIndex: 'class_name', key: 'class_name' },
  { title: '年级', dataIndex: 'grade', key: 'grade' },
  { title: '学生数', dataIndex: 'student_count', key: 'student_count' },
  { title: '教师', dataIndex: 'teacher', key: 'teacher' },
  { title: '操作', key: 'action', width: 100 },
]

const data = ref([
  {
    class_id: 'cls_001',
    class_name: '高三物理A班',
    grade: '高三',
    student_count: 45,
    teacher: '赵麒杰',
  },
  {
    class_id: 'cls_002',
    class_name: '高二物理B班',
    grade: '高二',
    student_count: 42,
    teacher: '李老师',
  },
])

const selectedClass = ref<any>(null)

function viewSummary(record: any) {
  selectedClass.value = record
}
</script>

<template>
  <div class="classes-page">
    <header class="page-header animate-fade-in-up">
      <div class="header-content">
        <h1>班级管理</h1>
        <p class="header-subtitle">管理班级与学生信息</p>
      </div>
      <a-button type="primary" size="large" class="add-btn">
        <template #icon>
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path d="M9 3V15M3 9H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </template>
        新建班级
      </a-button>
    </header>

    <!-- Stats -->
    <div class="stats-row animate-fade-in-up stagger-1">
      <div class="stat-card">
        <div class="stat-icon" style="--accent: var(--primary)">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <rect x="3" y="6" width="18" height="14" rx="2" stroke="currentColor" stroke-width="2"/>
            <path d="M8 6V4C8 2.89543 8.89543 2 10 2H14C15.1046 2 16 2.89543 16 4V6" stroke="currentColor" stroke-width="2"/>
            <circle cx="12" cy="13" r="2" stroke="currentColor" stroke-width="2"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-label">班级数量</span>
          <span class="stat-value">{{ data.length }}</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="--accent: var(--physics-blue)">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <circle cx="9" cy="7" r="3" stroke="currentColor" stroke-width="2"/>
            <circle cx="15" cy="7" r="3" stroke="currentColor" stroke-width="2"/>
            <path d="M3 19C3 16.2386 5.23858 14 8 14H12C14.7614 14 17 16.2386 17 19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-label">学生总数</span>
          <span class="stat-value">{{ data.reduce((sum, c) => sum + c.student_count, 0) }}</span>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-card animate-fade-in-up stagger-2">
      <a-table
        :columns="columns"
        :data-source="data"
        row-key="class_id"
        class="custom-table"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-button type="link" size="small" class="action-btn" @click="viewSummary(record)">
              查看详情
            </a-button>
          </template>
        </template>
      </a-table>
    </div>

    <!-- Summary Panel -->
    <div v-if="selectedClass" class="summary-panel animate-scale-in">
      <div class="summary-card">
        <div class="summary-header">
          <h3>{{ selectedClass.class_name }}</h3>
          <span class="summary-badge">{{ selectedClass.grade }}</span>
        </div>

        <div class="summary-stats">
          <div class="summary-stat">
            <span class="stat-value">{{ selectedClass.student_count }}</span>
            <span class="stat-label">学生数</span>
          </div>
          <div class="summary-stat">
            <span class="stat-value">120</span>
            <span class="stat-label">批改次数</span>
          </div>
          <div class="summary-stat">
            <span class="stat-value">7.85</span>
            <span class="stat-label">平均分</span>
          </div>
          <div class="summary-stat">
            <span class="stat-value success">82%</span>
            <span class="stat-label">通过率</span>
          </div>
        </div>

        <a-divider />
        <div class="summary-info">
          <div class="info-row">
            <span class="info-label">班主任</span>
            <span class="info-value">{{ selectedClass.teacher }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">创建时间</span>
            <span class="info-value">2026-03-01</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.classes-page {
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

.add-btn {
  height: 44px;
  padding: 0 var(--space-6);
  border-radius: var(--radius-md);
  background: var(--primary);
  border-color: var(--primary);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

/* Stats */
.stats-row {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-5);
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  min-width: 200px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: color-mix(in oklch, var(--accent) 10%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.stat-label {
  font-size: 0.8125rem;
  color: var(--text-secondary);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
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

.custom-table :deep(.ant-table-tbody > tr:hover > td) {
  background: var(--bg-secondary);
}

.action-btn {
  color: var(--primary);
  padding: var(--space-1) var(--space-2);
  height: auto;
}

/* Summary Panel */
.summary-panel {
  margin-top: var(--space-6);
}

.summary-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
}

.summary-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-6);
}

.summary-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
}

.summary-badge {
  padding: var(--space-1) var(--space-3);
  background: rgba(79, 70, 229, 0.1);
  color: var(--primary);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 500;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
}

.summary-stat {
  text-align: center;
  padding: var(--space-4);
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
}

.summary-stat .stat-value {
  display: block;
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: var(--space-1);
}

.summary-stat .stat-value.success {
  color: var(--success);
}

.summary-stat .stat-label {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
}

.summary-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: var(--space-2) 0;
}

.info-label {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.info-value {
  color: var(--text-primary);
  font-weight: 500;
  font-size: 0.875rem;
}

/* Animations */
.animate-fade-in-up {
  animation: fadeInUp var(--duration-slow) var(--ease-out-quart) forwards;
  opacity: 0;
}

.animate-scale-in {
  animation: scaleIn var(--duration-normal) var(--ease-spring) forwards;
}

.stagger-1 { animation-delay: 50ms; }
.stagger-2 { animation-delay: 100ms; }

/* Responsive */
@media (max-width: 768px) {
  .classes-page {
    padding: var(--space-4);
  }

  .page-header {
    flex-direction: column;
    gap: var(--space-4);
  }

  .add-btn {
    width: 100%;
    justify-content: center;
  }

  .stats-row {
    flex-direction: column;
  }

  .stat-card {
    min-width: 100%;
  }

  .summary-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>

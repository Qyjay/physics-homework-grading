<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { message, Modal } from 'ant-design-vue'
import { getClasses, getClassSummary } from '@/services/api'
import type { ClassInfo, StudentSummary } from '@/types/api'

// Types
interface ClassFormData {
  class_name: string
  grade: string
  description?: string
}

// Table columns
const columns = [
  { title: '班级名称', dataIndex: 'class_name', key: 'class_name', align: 'left' as const },
  { title: '年级', dataIndex: 'grade', key: 'grade', align: 'center' as const },
  { title: '学生数', dataIndex: 'student_count', key: 'student_count', width: 100, align: 'center' as const },
  { title: '班主任', key: 'teacher', align: 'center' as const },
  { title: '操作', key: 'action', width: 160, align: 'center' as const },
]

// State
const classes = ref<ClassInfo[]>([])
const loading = ref(false)
const selectedClass = ref<ClassInfo | null>(null)
const classSummary = ref<StudentSummary[]>([])

// Modal state
const classModalVisible = ref(false)
const classModalLoading = ref(false)
const isEditClass = ref(false)
const editingClassId = ref<string | null>(null)
const classFormRef = ref()
const classForm = ref<ClassFormData>({
  class_name: '',
  grade: '高一',
  description: '',
})

// Student Modal state
const studentModalVisible = ref(false)
const studentModalLoading = ref(false)
const editingStudent = ref<StudentSummary | null>(null)
const studentName = ref('')

// Grade options
const gradeOptions = [
  { value: '高一', label: '高一' },
  { value: '高二', label: '高二' },
  { value: '高三', label: '高三' },
]

// Mock data for demo
const mockStudents: StudentSummary[] = [
  { student_name: '张小明', grading_count: 12, average_score: 85.5 },
  { student_name: '李雨萱', grading_count: 10, average_score: 92.3 },
  { student_name: '王浩然', grading_count: 8, average_score: 78.0 },
  { student_name: '刘思琪', grading_count: 15, average_score: 88.7 },
  { student_name: '陈逸凡', grading_count: 11, average_score: 81.2 },
]

// Computed
const hasSelectedClass = computed(() => selectedClass.value !== null)

// Methods
async function fetchClasses() {
  loading.value = true
  try {
    const res = await getClasses()
    if (res.data) {
      classes.value = res.data
    }
  } catch (error: any) {
    message.error(error.message || '获取班级列表失败')
  } finally {
    loading.value = false
  }
}

async function fetchClassSummary(classId: string) {
  try {
    const res = await getClassSummary(classId)
    if (res.data?.students) {
      classSummary.value = res.data.students
    }
  } catch (error: any) {
    // Use mock data for demo
    classSummary.value = mockStudents
  }
}

function viewClassDetail(record: ClassInfo) {
  selectedClass.value = record
  fetchClassSummary(record.class_id)
}

function closeDetail() {
  selectedClass.value = null
  classSummary.value = []
}

// Class CRUD
function openCreateClass() {
  classForm.value = {
    class_name: '',
    grade: '高一',
    description: '',
  }
  isEditClass.value = false
  editingClassId.value = null
  classModalVisible.value = true
}

function openEditClass(record: ClassInfo) {
  classForm.value = {
    class_name: record.class_name,
    grade: record.grade,
    description: record.description,
  }
  isEditClass.value = true
  editingClassId.value = record.class_id
  classModalVisible.value = true
}

async function handleClassSubmit() {
  try {
    await classFormRef.value.validate()
    classModalLoading.value = true

    // API call would go here
    if (isEditClass.value) {
      // await updateClass(editingClassId.value, classForm.value)
      message.success('班级信息已更新')
    } else {
      // await createClass(classForm.value)
      message.success('班级创建成功')
    }

    classModalVisible.value = false
    fetchClasses()
  } catch (error: any) {
    if (error.message) {
      message.error(error.message)
    }
  } finally {
    classModalLoading.value = false
  }
}

function confirmDeleteClass(record: ClassInfo) {
  Modal.confirm({
    title: '确认删除',
    content: `确定要删除班级"${record.class_name}"吗？此操作不可恢复。`,
    okText: '确认删除',
    okType: 'danger',
    cancelText: '取消',
    onOk() {
      // await deleteClass(record.class_id)
      message.success('班级已删除')
      if (selectedClass.value?.class_id === record.class_id) {
        closeDetail()
      }
      fetchClasses()
    },
  })
}

// Student management
function openAddStudent() {
  editingStudent.value = null
  studentName.value = ''
  studentModalVisible.value = true
}

function openEditStudent(student: StudentSummary) {
  editingStudent.value = student
  studentName.value = student.student_name
  studentModalVisible.value = true
}

async function handleStudentSubmit() {
  if (!studentName.value.trim()) {
    message.warning('请输入学生姓名')
    return
  }

  studentModalLoading.value = true
  try {
    if (editingStudent.value) {
      // Edit existing student
      message.success('学生信息已更新')
    } else {
      // Add new student
      message.success('学生添加成功')
    }
    studentModalVisible.value = false
    if (selectedClass.value) {
      fetchClassSummary(selectedClass.value.class_id)
    }
  } catch (error: any) {
    message.error(error.message || '操作失败')
  } finally {
    studentModalLoading.value = false
  }
}

function confirmRemoveStudent(student: StudentSummary) {
  Modal.confirm({
    title: '移除学生',
    content: `确定要从班级中移除学生"${student.student_name}"吗？`,
    okText: '确认',
    okType: 'danger',
    cancelText: '取消',
    onOk() {
      message.success('学生已移除')
      if (selectedClass.value) {
        fetchClassSummary(selectedClass.value.class_id)
      }
    },
  })
}

function getScoreColor(score: number): string {
  if (score >= 90) return 'var(--success)'
  if (score >= 75) return 'var(--physics-blue)'
  if (score >= 60) return 'var(--warning)'
  return 'var(--error)'
}

onMounted(() => {
  fetchClasses()
})
</script>

<template>
  <div class="classes-page">
    <header class="page-header animate-fade-in-up">
      <div class="header-content">
        <h1>班级管理</h1>
        <p class="header-subtitle">管理班级与学生信息</p>
      </div>
      <a-button type="primary" size="large" class="add-btn" @click="openCreateClass">
        <template #icon>
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path d="M9 3V15M3 9H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </template>
        新建班级
      </a-button>
    </header>

    <div class="classes-layout">
      <!-- Left: Class List -->
      <div class="class-list-section animate-fade-in-up stagger-1">
        <!-- Stats -->
        <div class="stats-row">
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
              <span class="stat-value">{{ classes.length }}</span>
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
              <span class="stat-value">{{ classes.reduce((sum, c) => sum + c.student_count, 0) }}</span>
            </div>
          </div>
        </div>

        <!-- Table -->
        <div class="table-card">
          <a-table
            :columns="columns"
            :data-source="classes"
            :loading="loading"
            row-key="class_id"
            :pagination="{ pageSize: 10 }"
            class="custom-table"
          >
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'teacher'">
                <span class="teacher-name">{{ record.teacher?.username || '—' }}</span>
              </template>
              <template v-if="column.key === 'action'">
                <a-space>
                  <a-button type="link" size="small" class="action-btn" @click="viewClassDetail(record)">
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                      <circle cx="7" cy="7" r="5" stroke="currentColor" stroke-width="1.5"/>
                      <path d="M7 4V7L9 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                    详情
                  </a-button>
                  <a-button type="link" size="small" class="action-btn" @click="openEditClass(record)">
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                      <path d="M10 2L12 4L5 11H3V9L10 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    编辑
                  </a-button>
                  <a-popconfirm
                    title="确定删除这个班级？"
                    ok-text="确定"
                    cancel-text="取消"
                    @confirm="confirmDeleteClass(record)"
                  >
                    <a-button type="link" danger size="small" class="action-btn">
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
                  <rect x="8" y="16" width="48" height="36" rx="4" stroke="currentColor" stroke-width="2" opacity="0.3"/>
                  <path d="M20 16V12C20 9.79086 21.7909 8 24 8H40C42.2091 8 44 9.79086 44 12V16" stroke="currentColor" stroke-width="2" opacity="0.3"/>
                  <circle cx="32" cy="34" r="6" stroke="currentColor" stroke-width="2" opacity="0.3"/>
                </svg>
                <p>暂无班级</p>
                <a-button type="primary" @click="openCreateClass">创建第一个班级</a-button>
              </div>
            </template>
          </a-table>
        </div>
      </div>

      <!-- Right: Class Detail Panel -->
      <div v-if="hasSelectedClass" class="detail-section animate-fade-in-up stagger-2">
        <div class="detail-card">
          <!-- Header -->
          <div class="detail-header">
            <div class="detail-title">
              <h2>{{ selectedClass.class_name }}</h2>
              <span class="grade-badge">{{ selectedClass.grade }}</span>
            </div>
            <a-button type="text" class="close-btn" @click="closeDetail">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M6 6L14 14M14 6L6 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </a-button>
          </div>

          <!-- Overview Stats -->
          <div class="overview-stats">
            <div class="overview-stat">
              <span class="stat-value">{{ selectedClass.student_count }}</span>
              <span class="stat-label">学生</span>
            </div>
            <div class="overview-stat">
              <span class="stat-value">{{ classSummary.reduce((s, st) => s + st.grading_count, 0) }}</span>
              <span class="stat-label">批改次数</span>
            </div>
            <div class="overview-stat">
              <span class="stat-value" :style="{ color: getScoreColor(classSummary.length ? classSummary.reduce((s, st) => s + st.average_score, 0) / classSummary.length : 0) }">
                {{ classSummary.length ? (classSummary.reduce((s, st) => s + st.average_score, 0) / classSummary.length).toFixed(1) : '—' }}
              </span>
              <span class="stat-label">平均分</span>
            </div>
            <div class="overview-stat">
              <span class="stat-value success">{{ classSummary.length ? Math.round((classSummary.filter(s => s.average_score >= 60).length / classSummary.length) * 100) : 0 }}%</span>
              <span class="stat-label">通过率</span>
            </div>
          </div>

          <!-- Info -->
          <div class="detail-info">
            <div class="info-row">
              <span class="info-label">班主任</span>
              <span class="info-value">{{ selectedClass.teacher?.username || '—' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">创建时间</span>
              <span class="info-value">{{ selectedClass.created_at || '2026-03-01' }}</span>
            </div>
          </div>

          <a-divider />

          <!-- Student List Header -->
          <div class="student-header">
            <h3>学生列表</h3>
            <a-button type="primary" size="small" @click="openAddStudent">
              <template #icon>
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M7 3V11M3 7H11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </template>
              添加学生
            </a-button>
          </div>

          <!-- Student List -->
          <div class="student-list">
            <div
              v-for="student in classSummary"
              :key="student.student_name"
              class="student-item"
            >
              <div class="student-avatar">
                {{ student.student_name.charAt(0) }}
              </div>
              <div class="student-info">
                <span class="student-name">{{ student.student_name }}</span>
                <span class="student-meta">{{ student.grading_count }} 次批改</span>
              </div>
              <div class="student-score" :style="{ color: getScoreColor(student.average_score) }">
                {{ student.average_score.toFixed(1) }}
              </div>
              <a-space class="student-actions">
                <a-button type="text" size="small" @click="openEditStudent(student)">
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                    <path d="M8.5 2L10 3.5L4 9.5H2.5V8L8.5 2Z" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </a-button>
                <a-popconfirm
                  title="移除此学生？"
                  ok-text="确定"
                  cancel-text="取消"
                  @confirm="confirmRemoveStudent(student)"
                >
                  <a-button type="text" danger size="small">
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                      <path d="M2 4H10M4 4V3C4 2.44772 4.44772 2 5 2H7C7.55228 2 8 2.44772 8 3V4M9 4V9C9 9.55228 8.55228 10 8 10H4C3.44772 10 3 9.55228 3 9V4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                    </svg>
                  </a-button>
                </a-popconfirm>
              </a-space>
            </div>

            <div v-if="classSummary.length === 0" class="empty-students">
              <p>暂无学生</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Class Modal -->
    <a-modal
      v-model:open="classModalVisible"
      :title="isEditClass ? '编辑班级' : '新建班级'"
      :footer="null"
      class="class-modal"
    >
      <a-form
        ref="classFormRef"
        :model="classForm"
        layout="vertical"
        @finish="handleClassSubmit"
      >
        <a-form-item
          label="班级名称"
          name="class_name"
          :rules="[{ required: true, message: '请输入班级名称' }]"
        >
          <a-input v-model:value="classForm.class_name" placeholder="如：高三物理A班" size="large" />
        </a-form-item>

        <a-form-item
          label="年级"
          name="grade"
          :rules="[{ required: true, message: '请选择年级' }]"
        >
          <a-select v-model:value="classForm.grade" :options="gradeOptions" size="large" />
        </a-form-item>

        <a-form-item label="描述" name="description">
          <a-textarea v-model:value="classForm.description" placeholder="班级的简要描述..." :rows="3" />
        </a-form-item>

        <div class="modal-actions">
          <a-button @click="classModalVisible = false">取消</a-button>
          <a-button type="primary" html-type="submit" :loading="classModalLoading">
            {{ isEditClass ? '保存' : '创建' }}
          </a-button>
        </div>
      </a-form>
    </a-modal>

    <!-- Student Modal -->
    <a-modal
      v-model:open="studentModalVisible"
      :title="editingStudent ? '编辑学生' : '添加学生'"
      :footer="null"
      class="student-modal"
    >
      <a-form layout="vertical" @finish="handleStudentSubmit">
        <a-form-item label="学生姓名">
          <a-input v-model:value="studentName" placeholder="请输入学生姓名" size="large" />
        </a-form-item>

        <div class="modal-actions">
          <a-button @click="studentModalVisible = false">取消</a-button>
          <a-button type="primary" html-type="submit" :loading="studentModalLoading">
            {{ editingStudent ? '保存' : '添加' }}
          </a-button>
        </div>
      </a-form>
    </a-modal>
  </div>
</template>

<style scoped>
.classes-page {
  padding: var(--space-6);
  max-width: 1400px;
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

/* Layout */
.classes-layout {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: var(--space-6);
}

@media (max-width: 1200px) {
  .classes-layout {
    grid-template-columns: 1fr;
  }
}

/* Stats */
.stats-row {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-5);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-5);
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  flex: 1;
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

/* Table Card */
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

.teacher-name {
  color: var(--text-secondary);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--space-1);
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
  margin: var(--space-4) 0;
  color: var(--text-secondary);
}

/* Detail Section */
.detail-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  position: sticky;
  top: 88px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-6);
}

.detail-title {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.detail-title h2 {
  font-size: 1.25rem;
  font-weight: 600;
}

.grade-badge {
  padding: var(--space-1) var(--space-3);
  background: rgba(79, 70, 229, 0.1);
  color: var(--primary);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 500;
}

.close-btn {
  width: 32px;
  height: 32px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
}

.close-btn:hover {
  color: var(--text-primary);
  background: var(--bg-secondary);
}

/* Overview Stats */
.overview-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-3);
  margin-bottom: var(--space-6);
}

.overview-stat {
  text-align: center;
  padding: var(--space-4);
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
}

.overview-stat .stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.overview-stat .stat-value.success {
  color: var(--success);
}

.overview-stat .stat-label {
  font-size: 0.6875rem;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Detail Info */
.detail-info {
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

/* Student Header */
.student-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.student-header h3 {
  font-size: 1rem;
  font-weight: 600;
}

/* Student List */
.student-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  max-height: 400px;
  overflow-y: auto;
}

.student-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  transition: background var(--duration-fast);
}

.student-item:hover {
  background: var(--bg-primary);
}

.student-avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary) 0%, var(--physics-blue) 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.student-info {
  flex: 1;
  min-width: 0;
}

.student-name {
  display: block;
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--text-primary);
}

.student-meta {
  font-size: 0.75rem;
  color: var(--text-tertiary);
}

.student-score {
  font-size: 1.125rem;
  font-weight: 700;
}

.student-actions {
  opacity: 0;
  transition: opacity var(--duration-fast);
}

.student-item:hover .student-actions {
  opacity: 1;
}

.empty-students {
  text-align: center;
  padding: var(--space-8);
  color: var(--text-tertiary);
}

/* Modal */
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  margin-top: var(--space-6);
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

  .overview-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>

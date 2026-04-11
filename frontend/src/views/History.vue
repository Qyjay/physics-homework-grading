<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Table, Tag, Button } from 'ant-design-vue'

const router = useRouter()

const columns = [
  { title: '批改ID', dataIndex: 'grading_id', key: 'grading_id' },
  { title: '学生姓名', dataIndex: 'student_name', key: 'student_name' },
  { title: '题目', dataIndex: 'question_title', key: 'question_title' },
  { title: '得分', dataIndex: 'total_score', key: 'total_score' },
  { title: '批改时间', dataIndex: 'created_at', key: 'created_at' },
  { title: '操作', key: 'action' },
]

const data = ref([
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
    question_title: '斜面物体受力分析',
    total_score: 7.0,
    max_score: 10,
    created_at: '2026-04-11 14:35:00',
  },
])

function viewResult(record: any) {
  router.push(`/result/${record.grading_id}`)
}
</script>

<template>
  <div class="history-page">
    <h1>批改历史</h1>

    <a-card>
      <a-table :columns="columns" :data-source="data" row-key="grading_id">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'total_score'">
            <a-tag :color="record.total_score >= 6 ? 'green' : 'red'">
              {{ record.total_score }} / {{ record.max_score }}
            </a-tag>
          </template>
          <template v-if="column.key === 'action'">
            <a-button type="link" size="small" @click="viewResult(record)">查看详情</a-button>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<style scoped>
.history-page h1 {
  margin-bottom: 24px;
}
</style>

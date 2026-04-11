<script setup lang="ts">
import { ref } from 'vue'
import { Table, Card, Statistic, Row, Col } from 'ant-design-vue'

const columns = [
  { title: '班级名称', dataIndex: 'class_name', key: 'class_name' },
  { title: '年级', dataIndex: 'grade', key: 'grade' },
  { title: '学生数', dataIndex: 'student_count', key: 'student_count' },
  { title: '教师', dataIndex: 'teacher', key: 'teacher' },
  { title: '操作', key: 'action' },
]

const data = ref([
  {
    class_id: 'cls_001',
    class_name: '高三物理A班',
    grade: '高三',
    student_count: 45,
    teacher: '赵麒杰',
  },
])

const selectedClass = ref<any>(null)

function viewSummary(record: any) {
  selectedClass.value = record
}
</script>

<template>
  <div class="classes-page">
    <h1>班级管理</h1>

    <a-row :gutter="16" class="stats-row">
      <a-col :span="6">
        <a-card>
          <Statistic title="班级数量" :value="data.length" />
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card>
          <Statistic title="学生总数" :value="data.reduce((sum, c) => sum + c.student_count, 0)" />
        </a-card>
      </a-col>
    </a-row>

    <a-card title="班级列表">
      <a-table :columns="columns" :data-source="data" row-key="class_id">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-button type="link" size="small" @click="viewSummary(record)">查看详情</a-button>
          </template>
        </template>
      </a-table>
    </a-card>

    <a-card v-if="selectedClass" :title="`${selectedClass.class_name} - 批改汇总`" class="summary-card">
      <a-descriptions :column="2">
        <a-descriptions-item label="班级">{{ selectedClass.class_name }}</a-descriptions-item>
        <a-descriptions-item label="年级">{{ selectedClass.grade }}</a-descriptions-item>
        <a-descriptions-item label="批改次数">120</a-descriptions-item>
        <a-descriptions-item label="平均分">7.85</a-descriptions-item>
        <a-descriptions-item label="通过率">82%</a-descriptions-item>
      </a-descriptions>
    </a-card>
  </div>
</template>

<style scoped>
.classes-page h1 {
  margin-bottom: 24px;
}

.stats-row {
  margin-bottom: 24px;
}

.summary-card {
  margin-top: 24px;
}
</style>

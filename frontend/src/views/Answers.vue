<script setup lang="ts">
import { ref } from 'vue'
import { Table, Button, Modal, Form, Input, message } from 'ant-design-vue'

const columns = [
  { title: '题目', dataIndex: 'question_title', key: 'question_title' },
  { title: '学科', dataIndex: 'subject', key: 'subject' },
  { title: '年级', dataIndex: 'grade', key: 'grade' },
  { title: '总分', dataIndex: 'total_score', key: 'total_score' },
  { title: '操作', key: 'action' },
]

const data = ref([
  {
    answer_id: 'ans_001',
    question_title: '斜面物体受力分析',
    subject: '物理',
    grade: '高一',
    chapter: '牛顿定律',
    total_score: 10,
    step_count: 3,
  },
])

const visible = ref(false)
</script>

<template>
  <div class="answers-page">
    <div class="page-header">
      <h1>标准答案管理</h1>
      <a-button type="primary" @click="visible = true">新建答案</a-button>
    </div>

    <a-card>
      <a-table :columns="columns" :data-source="data" row-key="answer_id">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <a-button type="link" size="small">编辑</a-button>
              <a-button type="link" danger size="small">删除</a-button>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <a-modal v-model:open="visible" title="新建标准答案" width="600px" :footer="null">
      <a-form layout="vertical">
        <a-form-item label="题目名称" required>
          <a-input placeholder="请输入题目名称" />
        </a-form-item>
        <a-form-item label="学科">
          <a-input value="物理" disabled />
        </a-form-item>
        <a-form-item label="年级">
          <a-select placeholder="请选择年级" />
        </a-form-item>
        <a-form-item label="章节">
          <a-input placeholder="请输入章节" />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" block>保存</a-button>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
</style>

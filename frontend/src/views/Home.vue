<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Card, Statistic, Row, Col } from 'ant-design-vue'

const router = useRouter()

const stats = ref({
  totalGradings: 0,
  todayGradings: 0,
  averageScore: 0,
  passRate: 0,
})

function goToUpload() {
  router.push('/upload')
}

function goToAnswers() {
  router.push('/answers')
}
</script>

<template>
  <div class="home">
    <h1>欢迎使用高中物理作业智能批改系统</h1>

    <a-row :gutter="16" class="stats-row">
      <a-col :span="6">
        <a-card>
          <Statistic title="总批改数" :value="stats.totalGradings" />
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card>
          <Statistic title="今日批改" :value="stats.todayGradings" />
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card>
          <Statistic title="平均分" :value="stats.averageScore" suffix="/ 10" />
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card>
          <Statistic title="通过率" :value="stats.passRate" suffix="%" />
        </a-card>
      </a-col>
    </a-row>

    <div class="quick-actions">
      <h2>快速开始</h2>
      <div class="action-buttons">
        <a-button type="primary" size="large" @click="goToUpload">
          上传作业批改
        </a-button>
        <a-button size="large" @click="goToAnswers">
          管理标准答案
        </a-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home h1 {
  margin-bottom: 24px;
}

.stats-row {
  margin-bottom: 32px;
}

.quick-actions h2 {
  margin-bottom: 16px;
}

.action-buttons {
  display: flex;
  gap: 16px;
}
</style>

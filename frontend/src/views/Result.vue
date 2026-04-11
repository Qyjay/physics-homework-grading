<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Card, Progress, Tag } from 'ant-design-vue'

defineProps<{
  gradingId: string
}>()

const route = useRoute()

const gradingResult = ref({
  grading_id: '',
  total_score: 0,
  max_score: 10,
  step_results: [
    {
      step: 1,
      description: '受力分析',
      student_answer: '对物体A进行受力分析...',
      is_correct: true,
      score: 3,
      max_score: 3,
      comment: '受力分析正确',
    },
    {
      step: 2,
      description: '建立方程',
      student_answer: 'F - mg·sin(θ) = ma',
      is_correct: true,
      score: 3,
      max_score: 3,
      comment: '方程建立正确',
    },
    {
      step: 3,
      description: '求解计算',
      student_answer: 'a = 2.5 m/s²',
      is_correct: false,
      score: 2,
      max_score: 4,
      comment: '计算结果偏小',
    },
  ],
  feedback: '整体解题思路正确，主要错误在第三步的计算。建议复习三角函数基础知识。',
  suggestions: ['重新检查 sinθ 的取值', '加强三角函数运算练习'],
})

const scorePercent = ref(0)

onMounted(() => {
  const id = route.params.gradingId as string
  gradingResult.value.grading_id = id
  scorePercent.value = Math.round((gradingResult.value.total_score / gradingResult.value.max_score) * 100)
})
</script>

<template>
  <div class="result-page">
    <h1>批改结果</h1>

    <a-row :gutter="24">
      <a-col :span="8">
        <a-card>
          <div class="score-display">
            <a-progress
              type="circle"
              :percent="scorePercent"
              :format="() => `${gradingResult.total_score}/${gradingResult.max_score}`"
              :stroke-color="scorePercent >= 60 ? '#52c41a' : '#ff4d4f'"
            />
            <div class="score-label">总分</div>
          </div>
        </a-card>

        <a-card title="总体反馈" class="feedback-card">
          <p>{{ gradingResult.feedback }}</p>
        </a-card>

        <a-card title="改进建议">
          <a-tag v-for="suggestion in gradingResult.suggestions" :key="suggestion" color="blue">
            {{ suggestion }}
          </a-tag>
        </a-card>
      </a-col>

      <a-col :span="16">
        <a-card title="分步批改">
          <div v-for="step in gradingResult.step_results" :key="step.step" class="step-item">
            <div class="step-header">
              <span class="step-title">第 {{ step.step }} 步：{{ step.description }}</span>
              <a-tag :color="step.is_correct ? 'success' : 'error'">
                {{ step.is_correct ? '正确' : '错误' }}
              </a-tag>
            </div>
            <div class="step-content">
              <div class="student-answer">
                <strong>学生答案：</strong>
                <span>{{ step.student_answer }}</span>
              </div>
              <div class="score-info">
                <span>得分：{{ step.score }} / {{ step.max_score }}</span>
              </div>
              <div class="comment">
                <strong>批注：</strong>
                <span>{{ step.comment }}</span>
              </div>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<style scoped>
.result-page h1 {
  margin-bottom: 24px;
}

.score-display {
  text-align: center;
}

.score-label {
  margin-top: 16px;
  font-size: 16px;
  color: #8c8c8c;
}

.feedback-card {
  margin-top: 16px;
}

.step-item {
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.step-item:last-child {
  border-bottom: none;
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.step-title {
  font-size: 16px;
  font-weight: 500;
}

.step-content {
  padding-left: 8px;
}

.student-answer,
.score-info,
.comment {
  margin-bottom: 8px;
}

.comment {
  color: #8c8c8c;
}
</style>

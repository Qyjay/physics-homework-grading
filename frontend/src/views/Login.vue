<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { message } from 'ant-design-vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isLogin = ref(true)
const loading = ref(false)

const form = ref({
  username: '',
  password: '',
  email: '',
  role: 'teacher',
})

async function handleSubmit() {
  loading.value = true
  try {
    if (isLogin.value) {
      await authStore.login(form.value.username, form.value.password)
      message.success('登录成功')
    } else {
      await authStore.register(form.value.username, form.value.password, form.value.email, form.value.role)
      message.success('注册成功')
      isLogin.value = true
    }

    const redirect = route.query.redirect as string || '/'
    router.push(redirect)
  } catch (error: any) {
    message.error(error.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}

function toggleMode() {
  isLogin.value = !isLogin.value
}
</script>

<template>
  <div class="login-container">
    <a-card class="login-card">
      <template #title>
        <h2>高中物理作业智能批改系统</h2>
      </template>

      <a-form :model="form" layout="vertical" @finish="handleSubmit">
        <a-form-item label="用户名" name="username" :rules="[{ required: true, message: '请输入用户名' }]">
          <a-input v-model:value="form.username" placeholder="请输入用户名" size="large" />
        </a-form-item>

        <a-form-item label="密码" name="password" :rules="[{ required: true, message: '请输入密码' }]">
          <a-input-password v-model:value="form.password" placeholder="请输入密码" size="large" />
        </a-form-item>

        <template v-if="!isLogin">
          <a-form-item label="邮箱" name="email" :rules="[{ required: true, message: '请输入邮箱' }]">
            <a-input v-model:value="form.email" placeholder="请输入邮箱" size="large" />
          </a-form-item>

          <a-form-item label="角色" name="role">
            <a-radio-group v-model:value="form.role">
              <a-radio value="teacher">教师</a-radio>
              <a-radio value="student">学生</a-radio>
            </a-radio-group>
          </a-form-item>
        </template>

        <a-form-item>
          <a-button type="primary" html-type="submit" size="large" block :loading="loading">
            {{ isLogin ? '登录' : '注册' }}
          </a-button>
        </a-form-item>

        <div class="toggle-mode">
          <a @click="toggleMode">
            {{ isLogin ? '还没有账号？去注册' : '已有账号？去登录' }}
          </a>
        </div>
      </a-form>
    </a-card>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 400px;
  max-width: 90vw;
}

.login-card h2 {
  text-align: center;
  margin-bottom: 0;
  color: #1890ff;
}

.toggle-mode {
  text-align: center;
  margin-top: 16px;
}
</style>

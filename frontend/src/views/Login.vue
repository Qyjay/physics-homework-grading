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
  <div class="login-page">
    <!-- 装饰背景 -->
    <div class="bg-decoration">
      <div class="wave wave-1"></div>
      <div class="wave wave-2"></div>
      <div class="wave wave-3"></div>
      <div class="particle" style="--x: 10%; --y: 20%; --delay: 0s"></div>
      <div class="particle" style="--x: 85%; --y: 15%; --delay: 0.5s"></div>
      <div class="particle" style="--x: 70%; --y: 80%; --delay: 1s"></div>
      <div class="particle" style="--x: 20%; --y: 70%; --delay: 1.5s"></div>
      <div class="particle" style="--x: 50%; --y: 50%; --delay: 2s"></div>
    </div>

    <div class="login-container">
      <!-- 左侧品牌区域 -->
      <div class="brand-section animate-fade-in-up">
        <div class="brand-content">
          <div class="logo-mark">
            <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
              <circle cx="32" cy="32" r="30" stroke="currentColor" stroke-width="2" opacity="0.3"/>
              <circle cx="32" cy="32" r="20" stroke="currentColor" stroke-width="2" opacity="0.5"/>
              <circle cx="32" cy="32" r="10" fill="currentColor"/>
              <path d="M32 2 L32 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M32 50 L32 62" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M2 32 L14 32" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M50 32 L62 32" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h1 class="brand-title">高中物理作业<br/>智能批改系统</h1>
          <p class="brand-subtitle">AI 驱动的物理作业批改，让学习更高效</p>

          <div class="feature-list">
            <div class="feature-item stagger-1">
              <span class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M10 2L12.5 7.5L18 8L14 12L15 18L10 15L5 18L6 12L2 8L7.5 7.5L10 2Z" fill="currentColor"/>
                </svg>
              </span>
              <span>智能识别学生手写答案</span>
            </div>
            <div class="feature-item stagger-2">
              <span class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10C17 13.866 13.866 17 10 17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M10 7V10L13 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              <span>即时反馈与详细分析</span>
            </div>
            <div class="feature-item stagger-3">
              <span class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M10 2L12.5 7.5L18 8L14 12L15 18L10 15L5 18L6 12L2 8L7.5 7.5L10 2Z" fill="currentColor"/>
                </svg>
              </span>
              <span>个性化学习建议</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧登录表单区域 -->
      <div class="form-section">
        <div class="form-card animate-scale-in">
          <div class="form-header">
            <h2>{{ isLogin ? '欢迎回来' : '创建账号' }}</h2>
            <p>{{ isLogin ? '登录以继续使用智能批改系统' : '注册账号开始智能批改之旅' }}</p>
          </div>

          <a-form :model="form" layout="vertical" @finish="handleSubmit" class="login-form">
            <a-form-item
              label="用户名"
              name="username"
              :rules="[{ required: true, message: '请输入用户名' }]"
            >
              <a-input
                v-model:value="form.username"
                placeholder="请输入用户名"
                size="large"
                class="custom-input"
              >
                <template #prefix>
                  <UserOutlined class="input-icon" />
                </template>
              </a-input>
            </a-form-item>

            <a-form-item
              label="密码"
              name="password"
              :rules="[{ required: true, message: '请输入密码' }]"
            >
              <a-input-password
                v-model:value="form.password"
                placeholder="请输入密码"
                size="large"
                class="custom-input"
              >
                <template #prefix>
                  <LockOutlined class="input-icon" />
                </template>
              </a-input-password>
            </a-form-item>

            <template v-if="!isLogin">
              <a-form-item
                label="邮箱"
                name="email"
                :rules="[{ required: true, message: '请输入邮箱' }]"
                class="animate-fade-in-up"
              >
                <a-input
                  v-model:value="form.email"
                  placeholder="请输入邮箱"
                  size="large"
                  class="custom-input"
                >
                  <template #prefix>
                    <MailOutlined class="input-icon" />
                  </template>
                </a-input>
              </a-form-item>

              <a-form-item label="角色" name="role" class="animate-fade-in-up stagger-1">
                <a-radio-group v-model:value="form.role" class="role-group">
                  <a-radio-button value="teacher">
                    <span class="role-label">教师</span>
                  </a-radio-button>
                  <a-radio-button value="student">
                    <span class="role-label">学生</span>
                  </a-radio-button>
                </a-radio-group>
              </a-form-item>
            </template>

            <a-form-item class="submit-item">
              <a-button
                type="primary"
                html-type="submit"
                size="large"
                block
                :loading="loading"
                class="submit-btn"
              >
                {{ isLogin ? '登录' : '注册' }}
              </a-button>
            </a-form-item>

            <div class="toggle-mode animate-fade-in">
              <span class="toggle-text">{{ isLogin ? '还没有账号？' : '已有账号？' }}</span>
              <a @click="toggleMode" class="toggle-link">{{ isLogin ? '去注册' : '去登录' }}</a>
            </div>
          </a-form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
}

/* 装饰背景 */
.bg-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.wave {
  position: absolute;
  border-radius: 50%;
  opacity: 0.08;
}

.wave-1 {
  width: 600px;
  height: 600px;
  top: -200px;
  right: -100px;
  background: radial-gradient(circle, var(--primary) 0%, transparent 70%);
  animation: pulse 8s ease-in-out infinite;
}

.wave-2 {
  width: 400px;
  height: 400px;
  bottom: -100px;
  left: -100px;
  background: radial-gradient(circle, var(--physics-blue) 0%, transparent 70%);
  animation: pulse 6s ease-in-out infinite 1s;
}

.wave-3 {
  width: 300px;
  height: 300px;
  top: 50%;
  left: 30%;
  background: radial-gradient(circle, var(--success) 0%, transparent 70%);
  animation: pulse 10s ease-in-out infinite 2s;
}

.particle {
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--primary);
  left: var(--x);
  top: var(--y);
  opacity: 0.4;
  animation: float 6s ease-in-out infinite;
  animation-delay: var(--delay);
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.08; }
  50% { transform: scale(1.1); opacity: 0.12; }
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

/* 登录容器 */
.login-container {
  display: flex;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: var(--space-6);
  gap: var(--space-16);
  position: relative;
  z-index: 1;
}

/* 左侧品牌区域 */
.brand-section {
  flex: 1;
  display: flex;
  align-items: center;
  padding: var(--space-8) 0;
}

.brand-content {
  max-width: 380px;
}

.logo-mark {
  color: var(--primary);
  margin-bottom: var(--space-6);
  animation: float 4s ease-in-out infinite;
}

.brand-title {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1.2;
  color: var(--text-primary);
  margin-bottom: var(--space-4);
  letter-spacing: -0.02em;
}

.brand-subtitle {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin-bottom: var(--space-8);
  max-width: 100%;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.feature-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  color: var(--text-secondary);
  font-size: 0.9375rem;
}

.feature-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: rgba(79, 70, 229, 0.1);
  border-radius: var(--radius-md);
  color: var(--primary);
}

/* 右侧表单区域 */
.form-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-card {
  width: 100%;
  max-width: 400px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: var(--space-8);
  box-shadow: var(--shadow-lg);
}

.form-header {
  text-align: center;
  margin-bottom: var(--space-8);
}

.form-header h2 {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.form-header p {
  font-size: 0.9375rem;
  color: var(--text-secondary);
  max-width: 100%;
}

/* 表单样式 */
.login-form :deep(.ant-form-item-label > label) {
  font-weight: 500;
  color: var(--text-primary);
}

.custom-input {
  border-radius: var(--radius-md);
  height: 48px;
}

.custom-input :deep(.ant-input) {
  height: 100%;
  display: flex;
  align-items: center;
}

.input-icon {
  color: var(--text-tertiary);
}

.submit-item {
  margin-top: var(--space-6);
  margin-bottom: 0;
}

.submit-btn {
  height: 48px;
  font-size: 1rem;
  font-weight: 500;
  border-radius: var(--radius-md);
  background: var(--primary);
  border-color: var(--primary);
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
  transition: all var(--duration-fast) var(--ease-out-quart);
}

.submit-btn:hover {
  background: var(--primary-dark);
  border-color: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
}

/* 角色选择 */
.role-group {
  display: flex;
  width: 100%;
  gap: var(--space-3);
}

.role-group :deep(.ant-radio-button-wrapper) {
  flex: 1;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  border-color: var(--border);
}

.role-group :deep(.ant-radio-button-wrapper:first-child) {
  border-radius: var(--radius-md);
}

.role-group :deep(.ant-radio-button-wrapper:last-child) {
  border-radius: var(--radius-md);
}

.role-group :deep(.ant-radio-button-wrapper-checked) {
  background: rgba(79, 70, 229, 0.1);
  border-color: var(--primary);
}

.role-group :deep(.ant-radio-button-wrapper-checked .role-label) {
  color: var(--primary);
  font-weight: 500;
}

.role-label {
  font-size: 0.9375rem;
}

/* 切换模式 */
.toggle-mode {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  margin-top: var(--space-6);
}

.toggle-text {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.toggle-link {
  color: var(--primary);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: color var(--duration-fast);
}

.toggle-link:hover {
  color: var(--primary-dark);
}

/* 动画 */
.animate-fade-in-up {
  animation: fadeInUp var(--duration-slow) var(--ease-out-quart) forwards;
  opacity: 0;
}

.animate-scale-in {
  animation: scaleIn var(--duration-slow) var(--ease-spring) forwards;
  opacity: 0;
}

.animate-fade-in {
  animation: fadeIn var(--duration-normal) var(--ease-out-quart) forwards;
  opacity: 0;
}

.stagger-1 { animation-delay: 100ms; }
.stagger-2 { animation-delay: 200ms; }
.stagger-3 { animation-delay: 300ms; }

/* 响应式 */
@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
    gap: var(--space-8);
  }

  .brand-section {
    padding: var(--space-6) 0;
  }

  .brand-title {
    font-size: 2rem;
  }

  .feature-list {
    display: none;
  }

  .form-card {
    padding: var(--space-6);
  }
}
</style>

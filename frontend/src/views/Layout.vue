<script setup lang="ts">
import { computed } from 'vue'
import { RouterView, useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { message } from 'ant-design-vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const menuItems = [
  {
    key: '/',
    label: '首页',
    icon: '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M3 9L9 3L15 9M5.5 7.5V15H12.5V7.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  },
  {
    key: '/upload',
    label: '上传作业',
    icon: '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M9 3V12M9 3L6 6M9 3L12 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 13V14.5C3 15.0523 3.44772 15.5 4 15.5H14C14.5523 15.5 15 15.0523 15 14.5V13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
  },
  {
    key: '/answers',
    label: '标准答案',
    icon: '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M4 5H14M4 9H10M4 13H7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><rect x="12" y="7" width="3" height="3" rx="0.5" stroke="currentColor" stroke-width="1.5"/></svg>',
  },
  {
    key: '/classes',
    label: '班级管理',
    icon: '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><rect x="2" y="5" width="14" height="10" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M6 5V4C6 2.89543 6.89543 2 8 2H10C11.1046 2 12 2.89543 12 4V5" stroke="currentColor" stroke-width="1.5"/><circle cx="9" cy="10" r="2" stroke="currentColor" stroke-width="1.5"/></svg>',
  },
  {
    key: '/history',
    label: '历史记录',
    icon: '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="1.5"/><path d="M9 5V9L12 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  },
]

const selectedKey = computed(() => route.path)

function handleLogout() {
  authStore.logout()
  message.success('已退出登录')
  router.push('/login')
}
</script>

<template>
  <a-layout class="app-layout">
    <!-- 顶部导航 -->
    <a-layout-header class="app-header">
      <div class="header-content">
        <!-- Logo -->
        <div class="logo">
          <div class="logo-icon">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="1.5" opacity="0.3"/>
              <circle cx="16" cy="16" r="9" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
              <circle cx="16" cy="16" r="4" fill="currentColor"/>
              <path d="M16 2V6M16 26V30M2 16H6M26 16H30" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.6"/>
            </svg>
          </div>
          <span class="logo-text">物理作业批改</span>
        </div>

        <!-- 主导航 -->
        <nav class="main-nav">
          <router-link
            v-for="item in menuItems"
            :key="item.key"
            :to="item.key"
            class="nav-item"
            :class="{ active: selectedKey === item.key }"
          >
            <span class="nav-icon" v-html="item.icon"></span>
            <span class="nav-label">{{ item.label }}</span>
          </router-link>
        </nav>

        <!-- 用户信息 -->
        <div class="user-section">
          <div class="user-info">
            <div class="user-avatar">
              {{ authStore.user?.username?.charAt(0).toUpperCase() || 'U' }}
            </div>
            <div class="user-details">
              <span class="user-name">{{ authStore.user?.username || '用户' }}</span>
              <span class="user-role">{{ authStore.user?.role === 'teacher' ? '教师' : '学生' }}</span>
            </div>
          </div>
          <a-button type="text" class="logout-btn" @click="handleLogout">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path d="M6 15H4C3.44772 15 3 14.5523 3 14V4C3 3.44772 3.44772 3 4 3H6M12 12L15 9L12 6M15 9H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a-button>
        </div>
      </div>
    </a-layout-header>

    <!-- 主内容区 -->
    <a-layout-content class="app-content">
      <div class="content-wrapper">
        <RouterView />
      </div>
    </a-layout-content>

    <!-- 页脚 -->
    <a-layout-footer class="app-footer">
      <div class="footer-content">
        <span class="footer-text">高中物理作业智能批改系统 · 2026</span>
      </div>
    </a-layout-footer>
  </a-layout>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 头部导航 */
.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  height: auto;
  line-height: 1.5;
  padding: 0;
  background: var(--bg-elevated);
  border-bottom: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--space-6);
  height: 64px;
  display: flex;
  align-items: center;
  gap: var(--space-8);
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-shrink: 0;
}

.logo-icon {
  color: var(--primary);
  display: flex;
  align-items: center;
}

.logo-text {
  font-size: 1.0625rem;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

/* 主导航 */
.main-nav {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.9375rem;
  font-weight: 500;
  transition: all var(--duration-fast) var(--ease-out-quart);
  position: relative;
}

.nav-item:hover {
  color: var(--text-primary);
  background: var(--bg-secondary);
}

.nav-item.active {
  color: var(--primary);
  background: rgba(79, 70, 229, 0.08);
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
}

.nav-label {
  white-space: nowrap;
}

/* 用户区域 */
.user-section {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-shrink: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
  line-height: 1.3;
}

.user-role {
  font-size: 0.75rem;
  color: var(--text-tertiary);
  line-height: 1.3;
}

.logout-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
  border-radius: var(--radius-md);
  transition: all var(--duration-fast);
}

.logout-btn:hover {
  color: var(--error);
  background: rgba(239, 68, 68, 0.08);
}

/* 主内容区 */
.app-content {
  flex: 1;
  background: var(--bg-primary);
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 64px - 52px);
}

/* 页脚 */
.app-footer {
  padding: var(--space-4) var(--space-6);
  background: var(--bg-secondary);
  border-top: 1px solid var(--border);
  text-align: center;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
}

.footer-text {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
}

/* 响应式 */
@media (max-width: 768px) {
  .header-content {
    padding: 0 var(--space-4);
    gap: var(--space-4);
  }

  .logo-text {
    display: none;
  }

  .nav-label {
    display: none;
  }

  .nav-item {
    padding: var(--space-3);
  }

  .user-details {
    display: none;
  }

  .content-wrapper {
    min-height: calc(100vh - 64px - 52px);
  }
}
</style>

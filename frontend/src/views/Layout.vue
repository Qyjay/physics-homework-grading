<script setup lang="ts">
import { RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { message } from 'ant-design-vue'

const router = useRouter()
const authStore = useAuthStore()

const menuItems = [
  { key: '/', label: '首页' },
  { key: '/upload', label: '上传作业' },
  { key: '/answers', label: '标准答案' },
  { key: '/classes', label: '班级管理' },
  { key: '/history', label: '历史记录' },
]

function handleLogout() {
  authStore.logout()
  message.success('已退出登录')
  router.push('/login')
}
</script>

<template>
  <a-layout class="layout">
    <a-layout-header class="header">
      <div class="logo">物理作业批改</div>
      <a-menu mode="horizontal" theme="dark" :selectedKeys="[$route.path]" class="nav-menu">
        <a-menu-item v-for="item in menuItems" :key="item.key">
          <router-link :to="item.key">{{ item.label }}</router-link>
        </a-menu-item>
      </a-menu>
      <div class="user-info">
        <span>{{ authStore.user?.username }}</span>
        <a-button type="link" @click="handleLogout">退出</a-button>
      </div>
    </a-layout-header>

    <a-layout-content class="content">
      <div class="container">
        <RouterView />
      </div>
    </a-layout-content>
  </a-layout>
</template>

<style scoped>
.layout {
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  padding: 0 24px;
}

.logo {
  color: white;
  font-size: 18px;
  font-weight: bold;
  margin-right: 24px;
}

.nav-menu {
  flex: 1;
}

.user-info {
  color: white;
  display: flex;
  align-items: center;
  gap: 12px;
}

.content {
  padding: 24px 0;
}
</style>

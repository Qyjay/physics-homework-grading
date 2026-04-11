# 前端 (Vue 3 + TypeScript)

高中物理作业智能批改系统 - 前端应用

## 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全的 JavaScript 超集
- **Vite** - 下一代前端构建工具
- **Pinia** - Vue 状态管理
- **Vue Router** - Vue 路由管理
- **Ant Design Vue** - UI 组件库
- **Axios** - HTTP 客户端

## 项目结构

```
frontend/
├── index.html              # HTML 入口
├── package.json            # NPM 依赖
├── vite.config.ts          # Vite 配置
├── tsconfig.json           # TypeScript 配置
├── src/
│   ├── main.ts            # 应用入口
│   ├── App.vue            # 根组件
│   ├── api/               # API 调用（待创建）
│   ├── assets/            # 静态资源
│   │   └── main.css       # 全局样式
│   ├── components/         # 通用组件（待创建）
│   ├── router/
│   │   └── index.ts       # 路由配置
│   ├── stores/             # Pinia 状态管理
│   │   └── auth.ts        # 认证状态
│   ├── types/             # TypeScript 类型（待创建）
│   ├── utils/             # 工具函数（待创建）
│   └── views/             # 页面组件
│       ├── Login.vue       # 登录页
│       ├── Layout.vue      # 布局组件
│       ├── Home.vue        # 首页
│       ├── Upload.vue      # 上传作业
│       ├── Result.vue      # 批改结果
│       ├── Answers.vue     # 标准答案管理
│       ├── Classes.vue     # 班级管理
│       └── History.vue     # 历史记录
└── public/                # 公共静态资源（待创建）
```

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 运行开发服务器

```bash
npm run dev
```

### 3. 构建生产版本

```bash
npm run build
```

## 页面说明

| 页面 | 路由 | 说明 |
|------|------|------|
| 登录 | /login | 用户登录/注册 |
| 首页 | / | 仪表盘概览 |
| 上传 | /upload | 上传作业图片 |
| 结果 | /result/:id | 查看批改结果 |
| 答案 | /answers | 管理标准答案 |
| 班级 | /classes | 班级管理 |
| 历史 | /history | 批改历史 |

## API 代理

开发环境通过 Vite 代理到后端服务：

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': 'http://localhost:8000',
    '/uploads': 'http://localhost:8000',
  }
}
```

## 开发规范

### 组件结构

```vue
<script setup lang="ts">
// 1. imports
// 2. props & emits
// 3. 响应式状态
// 4. 计算属性
// 5. 方法
// 6. 生命周期
</script>

<template>
  <!-- 模板 -->
</template>

<style scoped>
/* 样式 */
</style>
```

### 命名规范

- 组件文件：PascalCase（e.g., `UserCard.vue`）
- 组件名：PascalCase
- Props：camelCase
- 事件：kebab-case

## License

课程项目 - 仅供学习交流

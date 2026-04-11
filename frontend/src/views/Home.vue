<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getHistory } from '@/services/api'

const router = useRouter()

const stats = ref({
  totalGradings: 0,
  todayGradings: 0,
  averageScore: 0,
  passRate: 0,
})

const recentActivity = ref<any[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await getHistory({ page: 1, page_size: 5 })
    if (res.data?.items) {
      recentActivity.value = res.data.items
    }
    // Mock stats for demo
    stats.value = {
      totalGradings: 156,
      todayGradings: 12,
      averageScore: 7.8,
      passRate: 85,
    }
  } catch (error) {
    // Mock data on error
    stats.value = {
      totalGradings: 156,
      todayGradings: 12,
      averageScore: 7.8,
      passRate: 85,
    }
  } finally {
    loading.value = false
  }
})

function goToUpload() {
  router.push('/upload')
}

function goToAnswers() {
  router.push('/answers')
}

function goToHistory() {
  router.push('/history')
}

function viewResult(item: any) {
  router.push(`/result/${item.grading_id}`)
}
</script>

<template>
  <div class="home-page">
    <!-- 页面标题区 -->
    <header class="page-header animate-fade-in-up">
      <div class="header-content">
        <h1>仪表盘</h1>
        <p class="header-subtitle">欢迎使用高中物理作业智能批改系统</p>
      </div>
      <div class="header-actions">
        <a-button type="primary" size="large" class="action-btn primary" @click="goToUpload">
          <template #icon>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M10 3V13M10 3L6 7M10 3L14 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M3 14V16C3 16.5523 3.44772 17 4 17H16C16.5523 17 17 16.5523 17 16V14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </template>
          上传作业
        </a-button>
        <a-button size="large" class="action-btn secondary" @click="goToAnswers">
          <template #icon>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M4 4H16M4 8H16M4 12H10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </template>
          管理答案
        </a-button>
      </div>
    </header>

    <!-- 统计卡片区 -->
    <section class="stats-section">
      <div class="stats-grid">
        <div class="stat-card animate-fade-in-up stagger-1" :style="{ '--accent': 'var(--primary)' }">
          <div class="stat-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15M9 5C9 6.10457 9.89543 7 11 7H13C14.1046 7 15 6.10457 15 5M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M9 14L11 16L15 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="stat-content">
            <span class="stat-label">总批改数</span>
            <span class="stat-value">{{ stats.totalGradings }}</span>
          </div>
          <div class="stat-decoration"></div>
        </div>

        <div class="stat-card animate-fade-in-up stagger-2" :style="{ '--accent': 'var(--physics-blue)' }">
          <div class="stat-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 8V12L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <div class="stat-content">
            <span class="stat-label">今日批改</span>
            <span class="stat-value">{{ stats.todayGradings }}</span>
          </div>
          <div class="stat-decoration"></div>
        </div>

        <div class="stat-card animate-fade-in-up stagger-3" :style="{ '--accent': 'var(--success)' }">
          <div class="stat-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="stat-content">
            <span class="stat-label">平均分</span>
            <span class="stat-value">{{ stats.averageScore }}<span class="stat-unit">/10</span></span>
          </div>
          <div class="stat-decoration"></div>
        </div>

        <div class="stat-card animate-fade-in-up stagger-4" :style="{ '--accent': 'var(--warning)' }">
          <div class="stat-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M22 11.08V12C21.9988 14.1564 21.3005 16.2547 20.0093 17.9818C18.7182 19.709 16.9033 20.9725 14.8354 21.5839C12.7674 22.1953 10.5573 22.1219 8.53447 21.3746C6.51168 20.6273 4.78465 19.2461 3.61096 17.4371C2.43727 15.628 1.87979 13.4881 2.02168 11.3363C2.16356 9.18455 2.99721 7.13631 4.39828 5.49706C5.79935 3.85781 7.69279 2.71537 9.79619 2.24013C11.8996 1.7649 14.1003 1.98232 16.07 2.85999" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M22 4L12 14.01L9 11.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="stat-content">
            <span class="stat-label">通过率</span>
            <span class="stat-value">{{ stats.passRate }}<span class="stat-unit">%</span></span>
          </div>
          <div class="stat-decoration"></div>
        </div>
      </div>
    </section>

    <!-- 最近活动 & 快捷操作 -->
    <section class="main-content">
      <!-- 最近批改 -->
      <div class="recent-section animate-fade-in-up stagger-5">
        <div class="section-header">
          <h2>最近批改</h2>
          <a @click="goToHistory" class="view-all">
            查看全部
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M6 4L10 8L6 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
        </div>
        <div class="recent-list">
          <div
            v-for="(item, index) in recentActivity"
            :key="item.grading_id"
            class="recent-item"
            :style="{ animationDelay: `${(index + 6) * 50}ms` }"
            @click="viewResult(item)"
          >
            <div class="recent-icon" :class="item.total_score >= 6 ? 'success' : 'warning'">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path v-if="item.total_score >= 6" d="M10 2L12.5 7.5L18 8L14 12L15 18L10 15L5 18L6 12L2 8L7.5 7.5L10 2Z" fill="currentColor"/>
                <path v-else d="M10 18L10 10M10 6L10 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <div class="recent-info">
              <span class="recent-title">{{ item.question_title || '物理作业批改' }}</span>
              <span class="recent-meta">{{ item.student_name || '学生' }} · {{ item.created_at || '刚刚' }}</span>
            </div>
            <div class="recent-score" :class="item.total_score >= 6 ? 'success' : 'warning'">
              {{ item.total_score ?? 0 }}/{{ item.max_score ?? 10 }}
            </div>
          </div>

          <!-- Empty state -->
          <div v-if="!recentActivity.length && !loading" class="empty-state">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <circle cx="24" cy="24" r="20" stroke="currentColor" stroke-width="2" opacity="0.3"/>
              <path d="M24 14V26M24 32V34" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <p>暂无批改记录</p>
            <a-button type="primary" @click="goToUpload">开始批改第一份作业</a-button>
          </div>

          <!-- Loading skeleton -->
          <div v-if="loading" class="loading-skeleton">
            <div v-for="i in 3" :key="i" class="skeleton-item">
              <div class="skeleton skeleton-icon"></div>
              <div class="skeleton-text">
                <div class="skeleton skeleton-title"></div>
                <div class="skeleton skeleton-meta"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="quick-section animate-fade-in-up stagger-6">
        <div class="section-header">
          <h2>快捷操作</h2>
        </div>
        <div class="quick-grid">
          <button class="quick-card" @click="goToUpload">
            <div class="quick-icon" style="--icon-color: var(--primary)">
              <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                <path d="M14 4V20M14 4L10 8M14 4L18 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M4 22V24C4 24.5523 4.44772 25 5 25H23C23.5523 25 24 24.5523 24 24V22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <span class="quick-label">上传作业</span>
            <span class="quick-desc">拍照或选择文件上传</span>
          </button>

          <button class="quick-card" @click="goToAnswers">
            <div class="quick-icon" style="--icon-color: var(--physics-blue)">
              <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                <path d="M6 8H22M6 14H16M6 20H12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <rect x="18" y="12" width="6" height="6" rx="1" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <span class="quick-label">标准答案</span>
            <span class="quick-desc">管理题目与评分标准</span>
          </button>

          <button class="quick-card" @click="goToHistory">
            <div class="quick-icon" style="--icon-color: var(--success)">
              <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                <circle cx="14" cy="14" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M14 8V14L18 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <span class="quick-label">历史记录</span>
            <span class="quick-desc">查看所有批改历史</span>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  padding: var(--space-6);
  max-width: 1200px;
  margin: 0 auto;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-8);
  gap: var(--space-6);
}

.header-content h1 {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: var(--space-1);
}

.header-subtitle {
  color: var(--text-secondary);
  font-size: 0.9375rem;
  max-width: 100%;
}

.header-actions {
  display: flex;
  gap: var(--space-3);
}

.action-btn {
  height: 44px;
  padding: 0 var(--space-6);
  border-radius: var(--radius-md);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: var(--space-2);
  transition: all var(--duration-fast) var(--ease-out-quart);
}

.action-btn.primary {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25);
}

.action-btn.primary:hover {
  background: var(--primary-dark);
  border-color: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.35);
}

.action-btn.secondary {
  background: var(--bg-elevated);
  border-color: var(--border);
  color: var(--text-primary);
}

.action-btn.secondary:hover {
  border-color: var(--border-strong);
  background: var(--bg-secondary);
}

/* 统计卡片 */
.stats-section {
  margin-bottom: var(--space-8);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
}

.stat-card {
  position: relative;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  display: flex;
  align-items: flex-start;
  gap: var(--space-4);
  overflow: hidden;
  transition: all var(--duration-fast) var(--ease-out-quart);
}

.stat-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: color-mix(in oklch, var(--accent) 12%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  flex-shrink: 0;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.stat-unit {
  font-size: 1rem;
  font-weight: 400;
  color: var(--text-tertiary);
  margin-left: 2px;
}

.stat-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 80px;
  height: 80px;
  background: radial-gradient(circle at top right, color-mix(in oklch, var(--accent) 8%, transparent), transparent 70%);
  pointer-events: none;
}

/* 主内容区 */
.main-content {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: var(--space-6);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.section-header h2 {
  font-size: 1.125rem;
  font-weight: 600;
}

.view-all {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  color: var(--primary);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: color var(--duration-fast);
}

.view-all:hover {
  color: var(--primary-dark);
}

/* 最近批改 */
.recent-section {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.recent-item {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background var(--duration-fast);
}

.recent-item:hover {
  background: var(--bg-secondary);
}

.recent-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.recent-icon.success {
  background: rgba(34, 197, 94, 0.1);
  color: var(--success);
}

.recent-icon.warning {
  background: rgba(249, 115, 22, 0.1);
  color: var(--warning);
}

.recent-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.recent-title {
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.recent-meta {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
}

.recent-score {
  font-size: 0.9375rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  flex-shrink: 0;
}

.recent-score.success {
  color: var(--success);
}

.recent-score.warning {
  color: var(--warning);
}

/* Empty state */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-8) var(--space-4);
  color: var(--text-tertiary);
  text-align: center;
}

.empty-state p {
  margin: var(--space-4) 0;
  color: var(--text-secondary);
}

/* Loading skeleton */
.loading-skeleton {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.skeleton-item {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-2);
}

.skeleton-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
}

.skeleton-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.skeleton-title {
  height: 16px;
  width: 60%;
}

.skeleton-meta {
  height: 12px;
  width: 40%;
}

/* 快捷操作 */
.quick-section {
  display: flex;
  flex-direction: column;
}

.quick-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.quick-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-4);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out-quart);
  text-align: left;
}

.quick-card:hover {
  border-color: var(--icon-color, var(--primary));
  transform: translateX(4px);
  box-shadow: var(--shadow-sm);
}

.quick-icon {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-md);
  background: color-mix(in oklch, var(--icon-color) 12%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--icon-color);
  margin-bottom: var(--space-2);
}

.quick-label {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 1rem;
}

.quick-desc {
  font-size: 0.875rem;
  color: var(--text-tertiary);
  line-height: 1.5;
}

/* 动画 */
.animate-fade-in-up {
  animation: fadeInUp var(--duration-slow) var(--ease-out-quart) forwards;
  opacity: 0;
}

.stagger-1 { animation-delay: 50ms; }
.stagger-2 { animation-delay: 100ms; }
.stagger-3 { animation-delay: 150ms; }
.stagger-4 { animation-delay: 200ms; }
.stagger-5 { animation-delay: 250ms; }
.stagger-6 { animation-delay: 300ms; }

/* 响应式 */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .main-content {
    grid-template-columns: 1fr;
  }

  .quick-section {
    order: -1;
  }

  .quick-grid {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .quick-card {
    flex: 1;
    min-width: 200px;
  }
}

@media (max-width: 640px) {
  .home-page {
    padding: var(--space-4);
  }

  .page-header {
    flex-direction: column;
    gap: var(--space-4);
  }

  .header-actions {
    width: 100%;
  }

  .action-btn {
    flex: 1;
    justify-content: center;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .quick-grid {
    flex-direction: column;
  }

  .quick-card {
    min-width: 100%;
  }
}
</style>

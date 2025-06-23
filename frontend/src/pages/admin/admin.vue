<template>
  <div class="admin-page">
    <div class="admin-container">
      <div class="admin-header">
        <h1 class="page-title">Admin Dashboard</h1>
        <p class="page-subtitle">Manage your ChatApp instance</p>
      </div>

      <div class="admin-content">
        <div class="stats-grid">
          <div class="stat-card" :class="{ loading: isLoading }">
            <div class="stat-icon">👥</div>
            <div class="stat-info">
              <h3 class="stat-number">{{ formatNumber(stats.users?.total || 0) }}</h3>
              <p class="stat-label">Total Users</p>
              <span class="stat-change" v-if="stats.users?.new_today">
                +{{ stats.users.new_today }} today
              </span>
            </div>
          </div>
          <div class="stat-card" :class="{ loading: isLoading }">
            <div class="stat-icon">💬</div>
            <div class="stat-info">
              <h3 class="stat-number">{{ formatNumber(stats.messages?.today || 0) }}</h3>
              <p class="stat-label">Messages Today</p>
              <span class="stat-change" v-if="stats.messages?.total">
                {{ formatNumber(stats.messages.total) }} total
              </span>
            </div>
          </div>
          <div class="stat-card" :class="{ loading: isLoading }">
            <div class="stat-icon">🟢</div>
            <div class="stat-info">
              <h3 class="stat-number">{{ formatNumber(stats.users?.online || 0) }}</h3>
              <p class="stat-label">Online Users</p>
              <span class="stat-change" v-if="stats.users?.active_24h">
                {{ stats.users.active_24h }} active 24h
              </span>
            </div>
          </div>
          <div class="stat-card" :class="{ loading: isLoading }">
            <div class="stat-icon">📊</div>
            <div class="stat-info">
              <h3 class="stat-number">{{ formatNumber(stats.rooms?.active || 0) }}</h3>
              <p class="stat-label">Active Rooms</p>
              <span class="stat-change" v-if="stats.rooms?.total">
                {{ stats.rooms.total }} total
              </span>
            </div>
          </div>
        </div>

        <div class="admin-sections">
          <div class="admin-section">
            <h2 class="section-title">Quick Actions</h2>
            <div class="action-grid">
              <button class="action-btn" @click="manageUsers">
                <div class="action-icon">👤</div>
                <span>Manage Users</span>
              </button>
              <button class="action-btn" @click="moderateMessages">
                <div class="action-icon">🛡️</div>
                <span>Moderate Messages</span>
              </button>
              <button class="action-btn" @click="viewAnalytics">
                <div class="action-icon">📈</div>
                <span>View Analytics</span>
              </button>
              <button class="action-btn" @click="refreshData" :disabled="isLoading">
                <div class="action-icon">{{ isLoading ? '⏳' : '🔄' }}</div>
                <span>{{ isLoading ? 'Refreshing...' : 'Refresh Data' }}</span>
              </button>
            </div>
          </div>

          <div class="admin-section">
            <h2 class="section-title">Recent Activity</h2>
            <div class="activity-list">
              <div
                v-for="user in stats.recent_activity.new_users"
                :key="user.id"
                class="activity-item"
              >
                <div class="activity-icon">👤</div>
                <div class="activity-content">
                  <p class="activity-text">New user registered: {{ user.username }}</p>
                  <span class="activity-time">{{ getTimeAgo(user.created_at) }}</span>
                </div>
              </div>

              <div v-if="stats.recent_activity.new_users.length === 0" class="activity-item">
                <div class="activity-icon">📊</div>
                <div class="activity-content">
                  <p class="activity-text">No recent activity</p>
                  <span class="activity-time">{{ formatTime(lastUpdated) }}</span>
                </div>
              </div>
            </div>

            <!-- System Health Status -->
            <div class="health-status" :class="healthStatus">
              <h3>System Health:
                <span class="health-indicator">
                  {{ healthStatus === 'healthy' ? '🟢 Healthy' :
                     healthStatus === 'warning' ? '🟡 Warning' : '🔴 Unhealthy' }}
                </span>
              </h3>
              <div class="health-details">
                <div class="health-item">
                  <span>Database:</span>
                  <span :class="systemHealth.database.status">{{ systemHealth.database.status }}</span>
                </div>
                <div class="health-item">
                  <span>WebSocket:</span>
                  <span>{{ systemHealth.websocket.active_connections }} connections</span>
                </div>
                <div class="health-item">
                  <span>Memory:</span>
                  <span>{{ systemHealth.system.memory_usage_percent }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useToast } from '../../composables/useToast'
import apiService from '../../services/api'

export default {
  name: 'Admin',
  setup() {
    const { showSuccess, showError, showInfo } = useToast()

    // Reactive data
    const isLoading = ref(false)
    const stats = reactive({
      users: {
        total: 0,
        new_today: 0,
        new_week: 0,
        online: 0,
        active_24h: 0,
        status_distribution: {},
        role_distribution: {}
      },
      messages: {
        total: 0,
        today: 0,
        week: 0,
        hourly_activity: {}
      },
      rooms: {
        total: 0,
        active: 0,
        total_members: 0
      },
      recent_activity: {
        new_users: []
      }
    })

    const systemHealth = reactive({
      database: { status: 'unknown', connected: false },
      websocket: { active_connections: 0, status: 'unknown' },
      system: { memory_usage_percent: 0, status: 'unknown' }
    })

    const lastUpdated = ref(null)

    // Methods
    const loadDashboardStats = async () => {
      try {
        isLoading.value = true

        try {
          const response = await apiService.getAdminDashboardStats()

          if (response.success) {
            // Update each property individually to ensure reactivity
            stats.users = response.stats.users
            stats.messages = response.stats.messages
            stats.rooms = response.stats.rooms
            stats.recent_activity = response.stats.recent_activity

            lastUpdated.value = new Date(response.timestamp)
            showSuccess('Dashboard data updated successfully')
          } else {
            loadMockData()
            showInfo('Using demo data (API response not successful)')
          }
        } catch (apiError) {
          console.error('API Error:', apiError)
          // Use mock data when backend is not available
          loadMockData()
          showInfo('Using demo data (backend not available)')
        }
      } catch (error) {
        console.error('Failed to load dashboard stats:', error)
        showError('Failed to load dashboard data')
        loadMockData()
      } finally {
        isLoading.value = false
      }
    }

    const loadSystemHealth = async () => {
      try {
        const response = await apiService.getSystemHealth()
        if (response.success) {
          Object.assign(systemHealth, response.health)
        }
      } catch (error) {
        console.log('System health check failed, using defaults')
        // Use default values when backend is not available
      }
    }

    const loadMockData = () => {
      // Mock data for demonstration
      Object.assign(stats, {
        users: {
          total: 1247,
          new_today: 23,
          new_week: 156,
          online: 89,
          active_24h: 234,
          status_distribution: { online: 89, away: 45, busy: 12, offline: 1101 },
          role_distribution: { user: 1245, admin: 2 }
        },
        messages: {
          total: 45678,
          today: 1234,
          week: 8765,
          hourly_activity: { 0: 12, 1: 8, 2: 5, 3: 3, 4: 2, 5: 4, 6: 15, 7: 45, 8: 89, 9: 123, 10: 156, 11: 178, 12: 234, 13: 198, 14: 167, 15: 145, 16: 134, 17: 123, 18: 98, 19: 76, 20: 54, 21: 43, 22: 32, 23: 21 }
        },
        rooms: {
          total: 45,
          active: 12,
          total_members: 567
        },
        recent_activity: {
          new_users: [
            { id: '1', username: 'john_doe', display_name: 'John Doe', created_at: new Date().toISOString() },
            { id: '2', username: 'jane_smith', display_name: 'Jane Smith', created_at: new Date(Date.now() - 300000).toISOString() }
          ]
        }
      })
      lastUpdated.value = new Date()
    }

    const refreshData = async () => {
      await Promise.all([
        loadDashboardStats(),
        loadSystemHealth()
      ])
    }

    const formatNumber = (num) => {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toString()
    }

    const formatTime = (date) => {
      if (!date) return 'Never'
      return new Date(date).toLocaleString()
    }

    const getTimeAgo = (date) => {
      if (!date) return 'Unknown'
      const now = new Date()
      const diff = now - new Date(date)
      const minutes = Math.floor(diff / 60000)
      const hours = Math.floor(diff / 3600000)
      const days = Math.floor(diff / 86400000)

      if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`
      if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`
      if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`
      return 'Just now'
    }

    // Action handlers
    const manageUsers = () => {
      showInfo('User management interface coming soon!')
    }

    const moderateMessages = () => {
      showInfo('Message moderation interface coming soon!')
    }

    const viewAnalytics = () => {
      showInfo('Analytics dashboard coming soon!')
    }

    const systemSettings = () => {
      showInfo('System settings interface coming soon!')
    }

    // Computed properties
    const healthStatus = computed(() => {
      const dbHealthy = systemHealth.database.status === 'healthy'
      const wsHealthy = systemHealth.websocket.status === 'healthy'
      const sysHealthy = systemHealth.system.status === 'healthy'

      if (dbHealthy && wsHealthy && sysHealthy) return 'healthy'
      if (!dbHealthy || systemHealth.system.status === 'unhealthy') return 'unhealthy'
      return 'warning'
    })

    // Lifecycle
    onMounted(() => {
      refreshData()

      // Auto-refresh every 30 seconds
      const interval = setInterval(refreshData, 30000)

      // Cleanup on unmount
      return () => clearInterval(interval)
    })

    return {
      // Data
      isLoading,
      stats,
      systemHealth,
      lastUpdated,

      // Computed
      healthStatus,

      // Methods
      refreshData,
      formatNumber,
      formatTime,
      getTimeAgo,
      manageUsers,
      moderateMessages,
      viewAnalytics,
      systemSettings
    }
  }
}
</script>

<style scoped>
.admin-page {
  min-height: 80vh;
  padding: 2rem;
  background: #f9fafb;
}

.admin-container {
  max-width: 1200px;
  margin: 0 auto;
}

.admin-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
}

.admin-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 2rem;
  background: #eff6ff;
  padding: 0.75rem;
  border-radius: 0.75rem;
}

.stat-number {
  font-size: 1.875rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.stat-change {
  font-size: 0.75rem;
  color: #059669;
  margin-top: 0.25rem;
  display: block;
}

.stat-card.loading {
  opacity: 0.6;
  pointer-events: none;
}

.stat-card.loading .stat-number {
  background: linear-gradient(90deg, #f3f4f6 25%, #e5e7eb 50%, #f3f4f6 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
  color: transparent;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.admin-sections {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.admin-section {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.action-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1.5rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.action-btn:hover {
  background: #f3f4f6;
  border-color: #3b82f6;
  transform: translateY(-2px);
}

.action-icon {
  font-size: 1.5rem;
}

.action-btn span {
  font-weight: 500;
  color: #374151;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.activity-icon {
  font-size: 1.25rem;
  background: #eff6ff;
  padding: 0.5rem;
  border-radius: 0.5rem;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-text {
  color: #374151;
  margin-bottom: 0.25rem;
}

.activity-time {
  color: #9ca3af;
  font-size: 0.875rem;
}

/* Health Status Styles */
.health-status {
  margin-top: 2rem;
  padding: 1rem;
  border-radius: 0.5rem;
  border: 2px solid;
}

.health-status.healthy {
  background: #f0fdf4;
  border-color: #22c55e;
}

.health-status.warning {
  background: #fffbeb;
  border-color: #f59e0b;
}

.health-status.unhealthy {
  background: #fef2f2;
  border-color: #ef4444;
}

.health-indicator {
  font-weight: 600;
}

.health-details {
  margin-top: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.health-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
}

.health-item span:first-child {
  color: #6b7280;
}

.health-item span:last-child {
  font-weight: 500;
}

.health-item .healthy {
  color: #22c55e;
}

.health-item .warning {
  color: #f59e0b;
}

.health-item .unhealthy {
  color: #ef4444;
}

/* Disabled button styles */
.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.action-btn:disabled:hover {
  background: #f9fafb;
  border-color: #e5e7eb;
}

@media (max-width: 768px) {
  .admin-page {
    padding: 1rem;
  }

  .admin-sections {
    grid-template-columns: 1fr;
  }

  .action-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
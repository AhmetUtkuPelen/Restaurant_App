<template>
  <div class="admin-page">
    <div class="admin-container">
      <div class="admin-header">
        <h1 class="page-title">Admin Dashboard</h1>
        <p class="page-subtitle">Manage your ChatApp instance</p>
      </div>

      <div class="admin-content">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-info">
              <h3 class="stat-number">1,234</h3>
              <p class="stat-label">Total Users</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">💬</div>
            <div class="stat-info">
              <h3 class="stat-number">5,678</h3>
              <p class="stat-label">Messages Today</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🟢</div>
            <div class="stat-info">
              <h3 class="stat-number">89</h3>
              <p class="stat-label">Online Users</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-info">
              <h3 class="stat-number">12</h3>
              <p class="stat-label">Active Rooms</p>
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
              <button class="action-btn" @click="systemSettings">
                <div class="action-icon">⚙️</div>
                <span>System Settings</span>
              </button>
            </div>
          </div>

          <div class="admin-section">
            <h2 class="section-title">Recent Activity</h2>
            <div class="activity-list">
              <div class="activity-item">
                <div class="activity-icon">👤</div>
                <div class="activity-content">
                  <p class="activity-text">New user registered: john_doe</p>
                  <span class="activity-time">2 minutes ago</span>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon">🚫</div>
                <div class="activity-content">
                  <p class="activity-text">Message flagged for review</p>
                  <span class="activity-time">5 minutes ago</span>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon">💬</div>
                <div class="activity-content">
                  <p class="activity-text">New chat room created: "Project Alpha"</p>
                  <span class="activity-time">10 minutes ago</span>
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
export default {
  name: 'Admin',
  setup() {
    const manageUsers = () => {
      alert('User management interface coming soon!')
    }

    const moderateMessages = () => {
      alert('Message moderation interface coming soon!')
    }

    const viewAnalytics = () => {
      alert('Analytics dashboard coming soon!')
    }

    const systemSettings = () => {
      alert('System settings interface coming soon!')
    }

    return {
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
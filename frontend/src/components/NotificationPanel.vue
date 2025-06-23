<template>
  <div class="notification-panel">
    <!-- Notification Bell -->
    <div class="notification-trigger" @click="togglePanel">
      <div class="notification-bell">
        🔔
        <span v-if="unreadCount > 0" class="notification-badge">
          {{ unreadCount > 99 ? '99+' : unreadCount }}
        </span>
      </div>
    </div>

    <!-- Notification Panel -->
    <div v-if="showPanel" class="notification-dropdown">
      <div class="notification-header">
        <h4>Notifications</h4>
        <div class="notification-actions">
          <button
            v-if="unreadCount > 0"
            @click="markAllAsRead"
            class="mark-all-read-btn"
            title="Mark all as read"
          >
            ✓
          </button>
          <button @click="showPanel = false" class="close-btn">×</button>
        </div>
      </div>

      <!-- Notification Filters -->
      <div class="notification-filters">
        <button
          @click="filterType = 'all'"
          :class="{ active: filterType === 'all' }"
          class="filter-btn"
        >
          All ({{ notifications.length }})
        </button>
        <button
          @click="filterType = 'unread'"
          :class="{ active: filterType === 'unread' }"
          class="filter-btn"
        >
          Unread ({{ unreadCount }})
        </button>
      </div>

      <!-- Notification List -->
      <div class="notification-list">
        <div v-if="loading" class="loading-state">
          <p>Loading notifications...</p>
        </div>
        
        <div v-else-if="filteredNotifications.length === 0" class="empty-state">
          <div class="empty-icon">🔔</div>
          <p v-if="filterType === 'unread'">No unread notifications</p>
          <p v-else>No notifications yet</p>
        </div>

        <div
          v-for="notification in filteredNotifications"
          :key="notification.id"
          class="notification-item"
          :class="{
            unread: !notification.is_read,
            [notification.notification_type]: true
          }"
          @click="handleNotificationClick(notification)"
        >
          <div class="notification-icon">
            {{ getNotificationIcon(notification.notification_type) }}
          </div>
          
          <div class="notification-content">
            <div class="notification-title">{{ notification.title }}</div>
            <div class="notification-message">{{ notification.message }}</div>
            <div class="notification-time">{{ formatTime(notification.created_at) }}</div>
          </div>

          <div class="notification-actions">
            <button
              v-if="!notification.is_read"
              @click.stop="markAsRead(notification.id)"
              class="mark-read-btn"
              title="Mark as read"
            >
              ✓
            </button>
            <button
              @click.stop="deleteNotification(notification.id)"
              class="delete-btn"
              title="Delete"
            >
              ×
            </button>
          </div>
        </div>
      </div>

      <!-- Load More -->
      <div v-if="hasMore" class="load-more">
        <button @click="loadMore" class="load-more-btn" :disabled="loading">
          Load More
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  userId: {
    type: String,
    required: true
  }
})

const emit = defineEmits([
  'notification-click',
  'message-notification',
  'call-notification',
  'room-notification'
])

// Reactive data
const showPanel = ref(false)
const notifications = ref([])
const unreadCount = ref(0)
const filterType = ref('all')
const loading = ref(false)
const hasMore = ref(false)
const currentPage = ref(0)
const pageSize = 20

// Computed properties
const filteredNotifications = computed(() => {
  if (filterType.value === 'unread') {
    return notifications.value.filter(n => !n.is_read)
  }
  return notifications.value
})

// Methods
const togglePanel = () => {
  showPanel.value = !showPanel.value
  if (showPanel.value) {
    loadNotifications()
  }
}

const loadNotifications = async (append = false) => {
  try {
    loading.value = true
    const page = append ? currentPage.value + 1 : 0
    const unreadOnly = filterType.value === 'unread'
    
    const response = await fetch(
      `http://localhost:8000/notifications/user/${props.userId}?unread_only=${unreadOnly}&limit=${pageSize}&offset=${page * pageSize}`
    )

    if (response.ok) {
      const data = await response.json()
      
      if (append) {
        notifications.value = [...notifications.value, ...data.notifications]
        currentPage.value = page
      } else {
        notifications.value = data.notifications || []
        currentPage.value = 0
      }
      
      hasMore.value = data.notifications.length === pageSize
      
      // Load unread count
      await loadUnreadCount()
    }
  } catch (error) {
    console.error('Failed to load notifications:', error)
  } finally {
    loading.value = false
  }
}

const loadUnreadCount = async () => {
  try {
    const response = await fetch(`http://localhost:8000/notifications/user/${props.userId}/unread-count`)
    if (response.ok) {
      const data = await response.json()
      unreadCount.value = data.unread_count || 0
    }
  } catch (error) {
    console.error('Failed to load unread count:', error)
  }
}

const markAsRead = async (notificationId) => {
  try {
    const response = await fetch(`http://localhost:8000/notifications/${notificationId}/read`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_id: props.userId })
    })

    if (response.ok) {
      // Update local state
      const notification = notifications.value.find(n => n.id === notificationId)
      if (notification) {
        notification.is_read = true
        unreadCount.value = Math.max(0, unreadCount.value - 1)
      }
    }
  } catch (error) {
    console.error('Failed to mark notification as read:', error)
  }
}

const markAllAsRead = async () => {
  try {
    const response = await fetch(`http://localhost:8000/notifications/user/${props.userId}/read-all`, {
      method: 'PUT'
    })

    if (response.ok) {
      // Update local state
      notifications.value.forEach(n => n.is_read = true)
      unreadCount.value = 0
    }
  } catch (error) {
    console.error('Failed to mark all notifications as read:', error)
  }
}

const deleteNotification = async (notificationId) => {
  try {
    const response = await fetch(`http://localhost:8000/notifications/${notificationId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_id: props.userId })
    })

    if (response.ok) {
      // Remove from local state
      const index = notifications.value.findIndex(n => n.id === notificationId)
      if (index > -1) {
        const notification = notifications.value[index]
        if (!notification.is_read) {
          unreadCount.value = Math.max(0, unreadCount.value - 1)
        }
        notifications.value.splice(index, 1)
      }
    }
  } catch (error) {
    console.error('Failed to delete notification:', error)
  }
}

const handleNotificationClick = (notification) => {
  // Mark as read if unread
  if (!notification.is_read) {
    markAsRead(notification.id)
  }

  // Emit specific events based on notification type
  emit('notification-click', notification)
  
  switch (notification.notification_type) {
    case 'message':
      emit('message-notification', notification)
      break
    case 'call':
      emit('call-notification', notification)
      break
    case 'room_invite':
      emit('room-notification', notification)
      break
    case 'mention':
      emit('message-notification', notification)
      break
  }

  // Close panel
  showPanel.value = false
}

const loadMore = () => {
  loadNotifications(true)
}

const getNotificationIcon = (type) => {
  const icons = {
    message: '💬',
    mention: '📢',
    call: '📞',
    room_invite: '🏠',
    reaction: '😊',
    system: '⚙️',
    default: '🔔'
  }
  return icons[type] || icons.default
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now - date
  const diffMinutes = Math.floor(diffMs / (1000 * 60))
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

  if (diffMinutes < 1) {
    return 'Just now'
  } else if (diffMinutes < 60) {
    return `${diffMinutes}m ago`
  } else if (diffHours < 24) {
    return `${diffHours}h ago`
  } else if (diffDays < 7) {
    return `${diffDays}d ago`
  } else {
    return date.toLocaleDateString()
  }
}

// Handle real-time notifications
const handleRealtimeNotification = (notification) => {
  // Add to beginning of list
  notifications.value.unshift(notification)
  
  // Update unread count
  if (!notification.is_read) {
    unreadCount.value++
  }
  
  // Show browser notification if permission granted
  if (Notification.permission === 'granted') {
    new Notification(notification.title, {
      body: notification.message,
      icon: '/favicon.ico',
      tag: notification.id
    })
  }
}

// Click outside to close
const handleClickOutside = (event) => {
  if (!event.target.closest('.notification-panel')) {
    showPanel.value = false
  }
}

// Lifecycle
onMounted(() => {
  loadUnreadCount()
  document.addEventListener('click', handleClickOutside)
  
  // Request notification permission
  if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission()
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Expose method for parent component to add real-time notifications
defineExpose({
  addNotification: handleRealtimeNotification,
  loadNotifications,
  loadUnreadCount
})
</script>

<style scoped>
.notification-panel {
  position: relative;
}

.notification-trigger {
  cursor: pointer;
}

.notification-bell {
  position: relative;
  font-size: 20px;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.notification-bell:hover {
  background: #f8f9fa;
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #dc3545;
  color: white;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
  line-height: 1.2;
}

.notification-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 350px;
  max-height: 500px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e0e0e0;
  background: #f8f9fa;
}

.notification-header h4 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.notification-actions {
  display: flex;
  gap: 8px;
}

.mark-all-read-btn, .close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  transition: background-color 0.2s;
}

.mark-all-read-btn:hover, .close-btn:hover {
  background: #e9ecef;
}

.notification-filters {
  display: flex;
  border-bottom: 1px solid #e0e0e0;
}

.filter-btn {
  flex: 1;
  padding: 8px 12px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 13px;
  color: #666;
  transition: all 0.2s;
}

.filter-btn:hover {
  background: #f8f9fa;
}

.filter-btn.active {
  background: #007bff;
  color: white;
}

.notification-list {
  max-height: 350px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background: #f8f9fa;
}

.notification-item.unread {
  background: #f0f8ff;
  border-left: 3px solid #007bff;
}

.notification-icon {
  font-size: 18px;
  margin-right: 12px;
  margin-top: 2px;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-weight: 600;
  color: #333;
  font-size: 14px;
  margin-bottom: 2px;
}

.notification-message {
  color: #666;
  font-size: 13px;
  line-height: 1.4;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.notification-time {
  font-size: 11px;
  color: #888;
}

.notification-actions {
  display: flex;
  gap: 4px;
  margin-left: 8px;
  opacity: 0;
  transition: opacity 0.2s;
}

.notification-item:hover .notification-actions {
  opacity: 1;
}

.mark-read-btn, .delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  font-size: 12px;
  transition: background-color 0.2s;
}

.mark-read-btn:hover {
  background: #d4edda;
  color: #155724;
}

.delete-btn:hover {
  background: #f8d7da;
  color: #721c24;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.empty-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.load-more {
  padding: 12px 16px;
  border-top: 1px solid #e0e0e0;
  text-align: center;
}

.load-more-btn {
  background: none;
  border: 1px solid #007bff;
  color: #007bff;
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.load-more-btn:hover:not(:disabled) {
  background: #007bff;
  color: white;
}

.load-more-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Notification type specific styles */
.notification-item.message {
  border-left-color: #28a745;
}

.notification-item.call {
  border-left-color: #ffc107;
}

.notification-item.room_invite {
  border-left-color: #17a2b8;
}

.notification-item.mention {
  border-left-color: #dc3545;
}

.notification-item.reaction {
  border-left-color: #fd7e14;
}
</style>

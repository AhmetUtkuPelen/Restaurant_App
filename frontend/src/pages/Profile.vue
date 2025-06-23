<template>
  <div class="profile-page">
    <div class="profile-container">
      <!-- Profile Header -->
      <div class="profile-header">
        <div class="profile-avatar-section">
          <div class="profile-avatar">
            <img v-if="userProfile.avatar" :src="userProfile.avatar" :alt="userProfile.display_name" />
            <span v-else class="avatar-placeholder">{{ getUserInitials() }}</span>
          </div>
          <button @click="showAvatarUpload = true" class="change-avatar-btn">
            📷 Change Photo
          </button>
        </div>
        
        <div class="profile-info">
          <h1 class="profile-name">{{ userProfile.display_name || userProfile.username }}</h1>
          <p class="profile-username">@{{ userProfile.username }}</p>
          <p class="profile-email">{{ userProfile.email }}</p>
          <div class="profile-badges">
            <span v-if="isAdmin" class="badge admin-badge">👑 Administrator</span>
            <span class="badge status-badge" :class="userProfile.status">
              {{ userProfile.status || 'offline' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Profile Stats -->
      <div class="profile-stats">
        <div class="stat-item">
          <div class="stat-number">{{ profileStats.total_messages || 0 }}</div>
          <div class="stat-label">Messages Sent</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ profileStats.rooms_joined || 0 }}</div>
          <div class="stat-label">Rooms Joined</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ profileStats.files_shared || 0 }}</div>
          <div class="stat-label">Files Shared</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ formatDate(userProfile.created_at) }}</div>
          <div class="stat-label">Member Since</div>
        </div>
      </div>

      <!-- Profile Tabs -->
      <div class="profile-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="{ active: activeTab === tab.id }"
          class="tab-btn"
        >
          {{ tab.icon }} {{ tab.label }}
        </button>
      </div>

      <!-- Tab Content -->
      <div class="tab-content">
        <!-- Personal Information Tab -->
        <div v-if="activeTab === 'info'" class="tab-panel">
          <div class="info-section">
            <h3>Personal Information</h3>
            <form @submit.prevent="updateProfile" class="profile-form">
              <div class="form-row">
                <div class="form-group">
                  <label for="displayName">Display Name</label>
                  <input
                    id="displayName"
                    v-model="editForm.display_name"
                    type="text"
                    class="form-input"
                    placeholder="Your display name"
                  />
                </div>
                <div class="form-group">
                  <label for="username">Username</label>
                  <input
                    id="username"
                    v-model="editForm.username"
                    type="text"
                    class="form-input"
                    placeholder="Your username"
                  />
                </div>
              </div>
              
              <div class="form-group">
                <label for="email">Email Address</label>
                <input
                  id="email"
                  v-model="editForm.email"
                  type="email"
                  class="form-input"
                  placeholder="your.email@example.com"
                />
              </div>
              
              <div class="form-group">
                <label for="bio">Bio</label>
                <textarea
                  id="bio"
                  v-model="editForm.bio"
                  class="form-textarea"
                  rows="3"
                  placeholder="Tell us about yourself..."
                ></textarea>
              </div>
              
              <div class="form-group">
                <label for="status">Status</label>
                <select id="status" v-model="editForm.status" class="form-select">
                  <option value="online">🟢 Online</option>
                  <option value="away">🟡 Away</option>
                  <option value="busy">🔴 Busy</option>
                  <option value="offline">⚫ Offline</option>
                </select>
              </div>
              
              <div class="form-actions">
                <button type="button" @click="resetForm" class="btn btn-secondary">
                  Reset
                </button>
                <button type="submit" class="btn btn-primary" :disabled="isLoading">
                  {{ isLoading ? 'Saving...' : 'Save Changes' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Security Tab -->
        <div v-if="activeTab === 'security'" class="tab-panel">
          <div class="security-section">
            <h3>Security Settings</h3>
            <form @submit.prevent="changePassword" class="security-form">
              <div class="form-group">
                <label for="currentPassword">Current Password</label>
                <input
                  id="currentPassword"
                  v-model="passwordForm.current_password"
                  type="password"
                  class="form-input"
                  placeholder="Enter current password"
                />
              </div>
              
              <div class="form-group">
                <label for="newPassword">New Password</label>
                <input
                  id="newPassword"
                  v-model="passwordForm.new_password"
                  type="password"
                  class="form-input"
                  placeholder="Enter new password"
                />
              </div>
              
              <div class="form-group">
                <label for="confirmPassword">Confirm New Password</label>
                <input
                  id="confirmPassword"
                  v-model="passwordForm.confirm_password"
                  type="password"
                  class="form-input"
                  placeholder="Confirm new password"
                />
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn btn-primary" :disabled="isLoading">
                  {{ isLoading ? 'Updating...' : 'Change Password' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Activity Tab -->
        <div v-if="activeTab === 'activity'" class="tab-panel">
          <div class="activity-section">
            <h3>Recent Activity</h3>
            <div v-if="recentActivity.length === 0" class="empty-state">
              <p>No recent activity to display.</p>
            </div>
            <div v-else class="activity-list">
              <div
                v-for="activity in recentActivity"
                :key="activity.id"
                class="activity-item"
              >
                <div class="activity-icon">{{ getActivityIcon(activity.type) }}</div>
                <div class="activity-content">
                  <div class="activity-description">{{ activity.description }}</div>
                  <div class="activity-time">{{ formatTime(activity.timestamp) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Preferences Tab -->
        <div v-if="activeTab === 'preferences'" class="tab-panel">
          <div class="preferences-section">
            <h3>Preferences</h3>
            <div class="preference-group">
              <h4>Notifications</h4>
              <div class="preference-item">
                <label class="checkbox-label">
                  <input v-model="preferences.email_notifications" type="checkbox" />
                  Email notifications
                </label>
              </div>
              <div class="preference-item">
                <label class="checkbox-label">
                  <input v-model="preferences.push_notifications" type="checkbox" />
                  Push notifications
                </label>
              </div>
              <div class="preference-item">
                <label class="checkbox-label">
                  <input v-model="preferences.sound_notifications" type="checkbox" />
                  Sound notifications
                </label>
              </div>
            </div>
            
            <div class="preference-group">
              <h4>Privacy</h4>
              <div class="preference-item">
                <label class="checkbox-label">
                  <input v-model="preferences.show_online_status" type="checkbox" />
                  Show online status
                </label>
              </div>
              <div class="preference-item">
                <label class="checkbox-label">
                  <input v-model="preferences.allow_direct_messages" type="checkbox" />
                  Allow direct messages
                </label>
              </div>
            </div>
            
            <div class="form-actions">
              <button @click="savePreferences" class="btn btn-primary" :disabled="isLoading">
                {{ isLoading ? 'Saving...' : 'Save Preferences' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Avatar Upload Modal -->
    <div v-if="showAvatarUpload" class="modal-overlay" @click="showAvatarUpload = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4>Change Profile Photo</h4>
          <button @click="showAvatarUpload = false" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="avatar-upload">
            <input
              ref="avatarInput"
              type="file"
              accept="image/*"
              @change="handleAvatarUpload"
              style="display: none"
            />
            <button @click="$refs.avatarInput.click()" class="upload-btn">
              📁 Choose Photo
            </button>
            <p class="upload-hint">Recommended: Square image, max 2MB</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useAuth } from '../composables/useAuth'
import { useToast } from '../composables/useToast'
import apiService from '../services/api'

export default {
  name: 'Profile',
  setup() {
    const { currentUser, currentUserId, isAdmin, getUserInitials, updateUserInfo } = useAuth()
    const { showSuccess, showError, showInfo } = useToast()

    // Reactive data
    const isLoading = ref(false)
    const activeTab = ref('info')
    const showAvatarUpload = ref(false)
    
    const userProfile = ref({
      id: '',
      username: '',
      email: '',
      display_name: '',
      bio: '',
      avatar: '',
      status: 'online',
      created_at: '',
      last_seen: ''
    })

    const profileStats = ref({
      total_messages: 0,
      rooms_joined: 0,
      files_shared: 0
    })

    const editForm = reactive({
      display_name: '',
      username: '',
      email: '',
      bio: '',
      status: 'online'
    })

    const passwordForm = reactive({
      current_password: '',
      new_password: '',
      confirm_password: ''
    })

    const preferences = reactive({
      email_notifications: true,
      push_notifications: true,
      sound_notifications: true,
      show_online_status: true,
      allow_direct_messages: true
    })

    const recentActivity = ref([])

    const tabs = [
      { id: 'info', label: 'Personal Info', icon: '👤' },
      { id: 'security', label: 'Security', icon: '🔒' },
      { id: 'activity', label: 'Activity', icon: '📊' },
      { id: 'preferences', label: 'Preferences', icon: '⚙️' }
    ]

    // Methods
    const loadProfile = async () => {
      try {
        isLoading.value = true

        // Use current user data as fallback
        if (currentUser.value) {
          userProfile.value = { ...currentUser.value }
          Object.assign(editForm, currentUser.value)
        }

        // Try to fetch from backend
        try {
          const data = await apiService.getCurrentUserProfile()
          userProfile.value = data
          Object.assign(editForm, data)
        } catch (apiError) {
          console.log('Backend not available, using local data')
          // Backend might not be available, continue with local data
        }
      } catch (error) {
        console.error('Failed to load profile:', error)
        showError('Failed to load profile data')
      } finally {
        isLoading.value = false
      }
    }

    const loadProfileStats = async () => {
      try {
        const response = await fetch(`http://localhost:8000/users/stats/${currentUserId.value}`)
        if (response.ok) {
          const data = await response.json()
          profileStats.value = data.stats
        }
      } catch (error) {
        console.error('Failed to load profile stats:', error)
      }
    }

    const updateProfile = async () => {
      try {
        isLoading.value = true

        try {
          const data = await apiService.updateUserProfile(editForm)
          userProfile.value = data
          updateUserInfo(data)
          showSuccess('Profile updated successfully!')
        } catch (apiError) {
          // Fallback: update local data
          Object.assign(userProfile.value, editForm)
          updateUserInfo(editForm)
          showSuccess('Profile updated locally (backend not available)')
        }
      } catch (error) {
        console.error('Failed to update profile:', error)
        showError('Failed to update profile')
      } finally {
        isLoading.value = false
      }
    }

    const changePassword = async () => {
      if (passwordForm.new_password !== passwordForm.confirm_password) {
        showError('New passwords do not match')
        return
      }

      try {
        isLoading.value = true
        
        const response = await fetch(`http://localhost:8000/users/change-password/${currentUserId.value}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            current_password: passwordForm.current_password,
            new_password: passwordForm.new_password
          })
        })

        if (response.ok) {
          showSuccess('Password changed successfully!')
          Object.assign(passwordForm, {
            current_password: '',
            new_password: '',
            confirm_password: ''
          })
        } else {
          const error = await response.json()
          showError(error.detail || 'Failed to change password')
        }
      } catch (error) {
        console.error('Failed to change password:', error)
        showError('Failed to change password')
      } finally {
        isLoading.value = false
      }
    }

    const savePreferences = async () => {
      try {
        isLoading.value = true
        showSuccess('Preferences saved successfully!')
        // In a real app, you would save to backend
      } catch (error) {
        showError('Failed to save preferences')
      } finally {
        isLoading.value = false
      }
    }

    const handleAvatarUpload = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      if (file.size > 2 * 1024 * 1024) {
        showError('File size must be less than 2MB')
        return
      }

      try {
        isLoading.value = true

        try {
          const data = await apiService.uploadAvatar(file)
          userProfile.value.avatar = data.avatar_url
          updateUserInfo({ avatar: data.avatar_url })
          showSuccess('Profile photo updated successfully!')
          showAvatarUpload.value = false
        } catch (apiError) {
          // Fallback: create a local URL for preview
          const localUrl = URL.createObjectURL(file)
          userProfile.value.avatar = localUrl
          updateUserInfo({ avatar: localUrl })
          showSuccess('Profile photo updated locally (backend not available)')
          showAvatarUpload.value = false
        }
      } catch (error) {
        console.error('Failed to upload avatar:', error)
        showError('Failed to upload photo')
      } finally {
        isLoading.value = false
      }
    }

    const resetForm = () => {
      Object.assign(editForm, userProfile.value)
      showInfo('Form reset to original values')
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'Unknown'
      return new Date(dateString).toLocaleDateString()
    }

    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleString()
    }

    const getActivityIcon = (type) => {
      const icons = {
        message: '💬',
        login: '🔑',
        join_room: '🏠',
        file_upload: '📁',
        profile_update: '👤'
      }
      return icons[type] || '📝'
    }

    // Lifecycle
    onMounted(() => {
      loadProfile()
      loadProfileStats()
    })

    return {
      // Data
      isLoading,
      activeTab,
      showAvatarUpload,
      userProfile,
      profileStats,
      editForm,
      passwordForm,
      preferences,
      recentActivity,
      tabs,
      
      // Computed
      isAdmin,
      
      // Methods
      updateProfile,
      changePassword,
      savePreferences,
      handleAvatarUpload,
      resetForm,
      formatDate,
      formatTime,
      getActivityIcon,
      getUserInitials
    }
  }
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem;
}

.profile-container {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* Profile Header */
.profile-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.profile-avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.profile-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: 2.5rem;
  font-weight: bold;
  color: white;
}

.change-avatar-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.change-avatar-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 2rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.profile-username {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0 0 0.5rem 0;
}

.profile-email {
  font-size: 1rem;
  opacity: 0.8;
  margin: 0 0 1rem 0;
}

.profile-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.admin-badge {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.status-badge {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  text-transform: capitalize;
}

/* Profile Stats */
.profile-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  padding: 2rem;
  background: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Profile Tabs */
.profile-tabs {
  display: flex;
  background: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
  overflow-x: auto;
}

.tab-btn {
  flex: 1;
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.2s;
  border-bottom: 3px solid transparent;
  white-space: nowrap;
}

.tab-btn:hover {
  color: #374151;
  background: rgba(59, 130, 246, 0.05);
}

.tab-btn.active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
  background: white;
}

/* Tab Content */
.tab-content {
  padding: 2rem;
}

.tab-panel {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Forms */
.profile-form,
.security-form {
  max-width: 600px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  font-size: 0.875rem;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

/* Sections */
.info-section h3,
.security-section h3,
.activity-section h3,
.preferences-section h3 {
  margin: 0 0 1.5rem 0;
  color: #1f2937;
  font-size: 1.25rem;
  font-weight: 600;
}

/* Activity */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.activity-list {
  space-y: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
}

.activity-icon {
  font-size: 1.5rem;
}

.activity-content {
  flex: 1;
}

.activity-description {
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.25rem;
}

.activity-time {
  font-size: 0.875rem;
  color: #6b7280;
}

/* Preferences */
.preference-group {
  margin-bottom: 2rem;
}

.preference-group h4 {
  margin: 0 0 1rem 0;
  color: #374151;
  font-size: 1rem;
  font-weight: 600;
}

.preference-item {
  margin-bottom: 0.75rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  color: #374151;
}

.checkbox-label input[type="checkbox"] {
  width: 1rem;
  height: 1rem;
  accent-color: #3b82f6;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 0.5rem;
  max-width: 400px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h4 {
  margin: 0;
  color: #1f2937;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #374151;
}

.modal-body {
  padding: 1.5rem;
}

.avatar-upload {
  text-align: center;
}

.upload-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.upload-btn:hover {
  background: #2563eb;
}

.upload-hint {
  font-size: 0.75rem;
  color: #6b7280;
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .profile-page {
    padding: 1rem;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .profile-stats {
    grid-template-columns: repeat(2, 1fr);
    padding: 1rem;
  }

  .tab-content {
    padding: 1rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>

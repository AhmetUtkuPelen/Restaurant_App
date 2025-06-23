<template>
  <div class="room-list">
    <div class="room-list-header">
      <h3>Chat Rooms</h3>
      <button @click="showCreateRoom = true" class="create-room-btn">
        ➕ Create Room
      </button>
    </div>

    <!-- Room Creation Modal -->
    <div v-if="showCreateRoom" class="modal-overlay" @click="showCreateRoom = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4>Create New Room</h4>
          <button @click="showCreateRoom = false" class="close-btn">×</button>
        </div>
        <form @submit.prevent="createRoom" class="room-form">
          <div class="form-group">
            <label for="roomName">Room Name</label>
            <input
              id="roomName"
              v-model="newRoom.name"
              type="text"
              placeholder="Enter room name"
              required
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="roomDescription">Description</label>
            <textarea
              id="roomDescription"
              v-model="newRoom.description"
              placeholder="Enter room description (optional)"
              class="form-textarea"
              rows="3"
            ></textarea>
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input
                v-model="newRoom.isPrivate"
                type="checkbox"
                class="form-checkbox"
              />
              Private Room
            </label>
          </div>
          <div class="form-actions">
            <button type="button" @click="showCreateRoom = false" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="!newRoom.name.trim()">
              Create Room
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Room Search -->
    <div class="room-search">
      <input
        v-model="searchQuery"
        placeholder="Search rooms..."
        class="search-input"
      />
    </div>

    <!-- Room Tabs -->
    <div class="room-tabs">
      <button
        @click="activeTab = 'joined'"
        :class="{ active: activeTab === 'joined' }"
        class="tab-btn"
      >
        My Rooms ({{ userRooms.length }})
      </button>
      <button
        @click="activeTab = 'public'"
        :class="{ active: activeTab === 'public' }"
        class="tab-btn"
      >
        Public Rooms
      </button>
    </div>

    <!-- Room Lists -->
    <div class="room-content">
      <!-- User's Rooms -->
      <div v-if="activeTab === 'joined'" class="room-section">
        <div v-if="filteredUserRooms.length === 0" class="empty-state">
          <p>You haven't joined any rooms yet.</p>
          <button @click="activeTab = 'public'" class="btn btn-primary">
            Browse Public Rooms
          </button>
        </div>
        <div
          v-for="room in filteredUserRooms"
          :key="room.id"
          class="room-item"
          :class="{ active: room.id === currentRoomId }"
          @click="selectRoom(room)"
        >
          <div class="room-info">
            <div class="room-header">
              <span class="room-name">{{ room.name }}</span>
              <span class="room-privacy">{{ room.is_private ? '🔒' : '🌐' }}</span>
            </div>
            <p class="room-description">{{ room.description || 'No description' }}</p>
            <div class="room-meta">
              <span class="member-count">👥 {{ room.member_count }} members</span>
              <span class="user-role" v-if="room.user_role === 'admin'">👑 Admin</span>
              <span class="muted-indicator" v-if="room.is_muted">🔇 Muted</span>
            </div>
            <div v-if="room.latest_message" class="latest-message">
              <span class="message-preview">{{ room.latest_message.content }}</span>
              <span class="message-time">{{ formatTime(room.latest_message.created_at) }}</span>
            </div>
          </div>
          <div class="room-actions">
            <button
              v-if="room.user_role === 'admin'"
              @click.stop="editRoom(room)"
              class="action-btn"
              title="Edit Room"
            >
              ⚙️
            </button>
            <button
              @click.stop="leaveRoom(room.id)"
              class="action-btn leave-btn"
              title="Leave Room"
            >
              🚪
            </button>
          </div>
        </div>
      </div>

      <!-- Public Rooms -->
      <div v-if="activeTab === 'public'" class="room-section">
        <div v-if="loading" class="loading-state">
          <p>Loading rooms...</p>
        </div>
        <div v-else-if="filteredPublicRooms.length === 0" class="empty-state">
          <p>No public rooms found.</p>
        </div>
        <div
          v-for="room in filteredPublicRooms"
          :key="room.id"
          class="room-item public-room"
        >
          <div class="room-info">
            <div class="room-header">
              <span class="room-name">{{ room.name }}</span>
              <span class="room-privacy">🌐</span>
            </div>
            <p class="room-description">{{ room.description || 'No description' }}</p>
            <div class="room-meta">
              <span class="member-count">👥 {{ room.member_count }} members</span>
              <span class="creator">Created by {{ room.creator_name }}</span>
            </div>
          </div>
          <div class="room-actions">
            <button
              v-if="!isUserInRoom(room.id)"
              @click="joinRoom(room.id)"
              class="btn btn-primary btn-sm"
            >
              Join
            </button>
            <span v-else class="joined-indicator">✓ Joined</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  currentRoomId: {
    type: String,
    default: null
  },
  userId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['room-selected', 'room-created', 'room-joined', 'room-left'])

// Reactive data
const userRooms = ref([])
const publicRooms = ref([])
const searchQuery = ref('')
const activeTab = ref('joined')
const showCreateRoom = ref(false)
const loading = ref(false)

const newRoom = ref({
  name: '',
  description: '',
  isPrivate: false
})

// Computed properties
const filteredUserRooms = computed(() => {
  if (!searchQuery.value) return userRooms.value
  
  return userRooms.value.filter(room =>
    room.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    room.description.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const filteredPublicRooms = computed(() => {
  if (!searchQuery.value) return publicRooms.value
  
  return publicRooms.value.filter(room =>
    room.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    room.description.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// Methods
const loadUserRooms = async () => {
  try {
    const response = await fetch(`http://localhost:8000/rooms/user/${props.userId}`)
    if (response.ok) {
      const data = await response.json()
      userRooms.value = data.rooms || []
    }
  } catch (error) {
    console.error('Failed to load user rooms:', error)
  }
}

const loadPublicRooms = async () => {
  try {
    loading.value = true
    const response = await fetch('http://localhost:8000/rooms/public')
    if (response.ok) {
      const data = await response.json()
      publicRooms.value = data.public_rooms || []
    }
  } catch (error) {
    console.error('Failed to load public rooms:', error)
  } finally {
    loading.value = false
  }
}

const createRoom = async () => {
  try {
    const response = await fetch('http://localhost:8000/rooms/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: newRoom.value.name,
        description: newRoom.value.description,
        is_private: newRoom.value.isPrivate
      })
    })

    if (response.ok) {
      const data = await response.json()
      
      // Reset form
      newRoom.value = { name: '', description: '', isPrivate: false }
      showCreateRoom.value = false
      
      // Reload rooms
      await loadUserRooms()
      if (!newRoom.value.isPrivate) {
        await loadPublicRooms()
      }
      
      emit('room-created', data.room)
    } else {
      const error = await response.json()
      alert(`Failed to create room: ${error.detail}`)
    }
  } catch (error) {
    console.error('Failed to create room:', error)
    alert('Failed to create room. Please try again.')
  }
}

const joinRoom = async (roomId) => {
  try {
    const response = await fetch(`http://localhost:8000/rooms/${roomId}/join`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_id: props.userId })
    })

    if (response.ok) {
      // Reload user rooms
      await loadUserRooms()
      emit('room-joined', roomId)
    } else {
      const error = await response.json()
      alert(`Failed to join room: ${error.detail}`)
    }
  } catch (error) {
    console.error('Failed to join room:', error)
    alert('Failed to join room. Please try again.')
  }
}

const leaveRoom = async (roomId) => {
  if (!confirm('Are you sure you want to leave this room?')) return

  try {
    const response = await fetch(`http://localhost:8000/rooms/${roomId}/leave`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_id: props.userId })
    })

    if (response.ok) {
      // Remove from user rooms
      userRooms.value = userRooms.value.filter(room => room.id !== roomId)
      emit('room-left', roomId)
    } else {
      const error = await response.json()
      alert(`Failed to leave room: ${error.detail}`)
    }
  } catch (error) {
    console.error('Failed to leave room:', error)
    alert('Failed to leave room. Please try again.')
  }
}

const selectRoom = (room) => {
  emit('room-selected', room)
}

const editRoom = (room) => {
  // TODO: Implement room editing
  console.log('Edit room:', room)
}

const isUserInRoom = (roomId) => {
  return userRooms.value.some(room => room.id === roomId)
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Lifecycle
onMounted(() => {
  loadUserRooms()
  loadPublicRooms()
})

// Watch for tab changes to reload data
const handleTabChange = () => {
  if (activeTab.value === 'public') {
    loadPublicRooms()
  }
}
</script>

<style scoped>
.room-list {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: white;
  border-right: 1px solid #e0e0e0;
}

.room-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
  background: #f8f9fa;
}

.room-list-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.create-room-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.create-room-btn:hover {
  background: #0056b3;
}

.room-search {
  padding: 12px 16px;
  border-bottom: 1px solid #e0e0e0;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.room-tabs {
  display: flex;
  border-bottom: 1px solid #e0e0e0;
}

.tab-btn {
  flex: 1;
  padding: 12px 16px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.2s;
}

.tab-btn:hover {
  background: #f8f9fa;
}

.tab-btn.active {
  background: #007bff;
  color: white;
}

.room-content {
  flex: 1;
  overflow-y: auto;
}

.room-section {
  padding: 8px;
}

.room-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 12px;
  margin-bottom: 8px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.room-item:hover {
  background: #f8f9fa;
  border-color: #007bff;
}

.room-item.active {
  background: #e3f2fd;
  border-color: #007bff;
}

.room-info {
  flex: 1;
  min-width: 0;
}

.room-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.room-name {
  font-weight: 600;
  color: #333;
  font-size: 16px;
}

.room-privacy {
  font-size: 14px;
}

.room-description {
  margin: 4px 0;
  color: #666;
  font-size: 14px;
  line-height: 1.4;
}

.room-meta {
  display: flex;
  gap: 12px;
  margin: 8px 0;
  font-size: 12px;
  color: #888;
}

.latest-message {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #eee;
  font-size: 12px;
}

.message-preview {
  color: #666;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.message-time {
  color: #888;
  margin-left: 8px;
}

.room-actions {
  display: flex;
  gap: 4px;
  margin-left: 8px;
}

.action-btn {
  background: none;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.action-btn:hover {
  background: #e9ecef;
}

.leave-btn:hover {
  background: #f8d7da;
  color: #721c24;
}

.joined-indicator {
  color: #28a745;
  font-size: 14px;
  font-weight: 600;
}

.empty-state, .loading-state {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

/* Modal Styles */
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
  border-radius: 8px;
  padding: 0;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h4 {
  margin: 0;
  font-size: 18px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.close-btn:hover {
  background: #f8f9fa;
}

.room-form {
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  font-weight: 600;
  color: #333;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.form-checkbox {
  width: auto;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn-primary:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}
</style>

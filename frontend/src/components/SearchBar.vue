<template>
  <div class="search-bar">
    <div class="search-input-container">
      <input
        v-model="searchQuery"
        @input="handleSearch"
        @focus="showResults = true"
        @keydown.escape="clearSearch"
        @keydown.enter="performSearch"
        placeholder="Search messages, users, rooms..."
        class="search-input"
        ref="searchInput"
      />
      <button
        v-if="searchQuery"
        @click="clearSearch"
        class="clear-btn"
      >
        ×
      </button>
      <button @click="performSearch" class="search-btn">
        🔍
      </button>
    </div>

    <!-- Search Results Dropdown -->
    <div v-if="showResults && (suggestions.length > 0 || searchQuery)" class="search-results">
      <!-- Search Suggestions -->
      <div v-if="suggestions.length > 0 && !searchQuery" class="suggestions-section">
        <h4>Recent Searches</h4>
        <div
          v-for="suggestion in suggestions"
          :key="suggestion"
          @click="selectSuggestion(suggestion)"
          class="suggestion-item"
        >
          <span class="suggestion-icon">🔍</span>
          <span class="suggestion-text">{{ suggestion }}</span>
        </div>
      </div>

      <!-- Live Search Results -->
      <div v-if="searchQuery && searchResults" class="live-results">
        <!-- Messages -->
        <div v-if="searchResults.messages && searchResults.messages.length > 0" class="result-section">
          <h4>Messages ({{ searchResults.messages.length }})</h4>
          <div
            v-for="message in searchResults.messages.slice(0, 5)"
            :key="message.id"
            @click="selectMessage(message)"
            class="result-item message-result"
          >
            <div class="result-icon">💬</div>
            <div class="result-content">
              <div class="result-title">{{ message.sender?.display_name || 'Unknown' }}</div>
              <div class="result-description" v-html="message.highlighted_content || message.content"></div>
              <div class="result-meta">
                <span v-if="message.room">in {{ message.room.name }}</span>
                <span>{{ formatTime(message.created_at) }}</span>
              </div>
            </div>
          </div>
          <div v-if="searchResults.messages.length > 5" class="show-more">
            <button @click="showAllMessages" class="show-more-btn">
              Show all {{ searchResults.messages.length }} messages
            </button>
          </div>
        </div>

        <!-- Users -->
        <div v-if="searchResults.users && searchResults.users.length > 0" class="result-section">
          <h4>Users ({{ searchResults.users.length }})</h4>
          <div
            v-for="user in searchResults.users.slice(0, 3)"
            :key="user.id"
            @click="selectUser(user)"
            class="result-item user-result"
          >
            <div class="result-icon">👤</div>
            <div class="result-content">
              <div class="result-title">{{ user.display_name || user.username }}</div>
              <div class="result-description">@{{ user.username }}</div>
              <div class="result-meta">
                <span class="user-status" :class="user.status">{{ user.status || 'offline' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Rooms -->
        <div v-if="searchResults.rooms && searchResults.rooms.length > 0" class="result-section">
          <h4>Rooms ({{ searchResults.rooms.length }})</h4>
          <div
            v-for="room in searchResults.rooms.slice(0, 3)"
            :key="room.id"
            @click="selectRoom(room)"
            class="result-item room-result"
          >
            <div class="result-icon">{{ room.is_private ? '🔒' : '🌐' }}</div>
            <div class="result-content">
              <div class="result-title">{{ room.name }}</div>
              <div class="result-description">{{ room.description || 'No description' }}</div>
              <div class="result-meta">
                <span>{{ room.member_count }} members</span>
                <span v-if="room.is_member">• Joined</span>
              </div>
            </div>
          </div>
        </div>

        <!-- No Results -->
        <div v-if="searchQuery && !hasResults" class="no-results">
          <div class="no-results-icon">🔍</div>
          <div class="no-results-text">No results found for "{{ searchQuery }}"</div>
          <div class="no-results-suggestions">
            <p>Try:</p>
            <ul>
              <li>Checking your spelling</li>
              <li>Using different keywords</li>
              <li>Searching for users or rooms instead</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Advanced Search Link -->
      <div class="advanced-search">
        <button @click="openAdvancedSearch" class="advanced-search-btn">
          ⚙️ Advanced Search
        </button>
      </div>
    </div>

    <!-- Advanced Search Modal -->
    <div v-if="showAdvancedSearch" class="modal-overlay" @click="showAdvancedSearch = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4>Advanced Search</h4>
          <button @click="showAdvancedSearch = false" class="close-btn">×</button>
        </div>
        <form @submit.prevent="performAdvancedSearch" class="advanced-form">
          <div class="form-group">
            <label>Search Query</label>
            <input v-model="advancedQuery.query" type="text" class="form-input" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>From User</label>
              <select v-model="advancedQuery.senderId" class="form-select">
                <option value="">Any user</option>
                <option v-for="user in knownUsers" :key="user.id" :value="user.id">
                  {{ user.display_name || user.username }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>In Room</label>
              <select v-model="advancedQuery.roomId" class="form-select">
                <option value="">Any room</option>
                <option v-for="room in knownRooms" :key="room.id" :value="room.id">
                  {{ room.name }}
                </option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>From Date</label>
              <input v-model="advancedQuery.dateFrom" type="date" class="form-input" />
            </div>
            <div class="form-group">
              <label>To Date</label>
              <input v-model="advancedQuery.dateTo" type="date" class="form-input" />
            </div>
          </div>
          <div class="form-group">
            <label>Message Type</label>
            <select v-model="advancedQuery.messageType" class="form-select">
              <option value="">Any type</option>
              <option value="TEXT">Text only</option>
              <option value="IMAGE">With images</option>
              <option value="FILE">With files</option>
            </select>
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input v-model="advancedQuery.hasAttachments" type="checkbox" />
              Only messages with attachments
            </label>
          </div>
          <div class="form-actions">
            <button type="button" @click="showAdvancedSearch = false" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary">
              Search
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import Fuse from 'fuse.js'

const props = defineProps({
  userId: {
    type: String,
    required: true
  }
})

const emit = defineEmits([
  'search-results',
  'message-selected',
  'user-selected',
  'room-selected',
  'advanced-search'
])

// Reactive data
const searchQuery = ref('')
const showResults = ref(false)
const searchResults = ref(null)
const suggestions = ref([])
const showAdvancedSearch = ref(false)
const knownUsers = ref([])
const knownRooms = ref([])
const searchTimeout = ref(null)

const advancedQuery = ref({
  query: '',
  senderId: '',
  roomId: '',
  dateFrom: '',
  dateTo: '',
  messageType: '',
  hasAttachments: false
})

// Computed properties
const hasResults = computed(() => {
  if (!searchResults.value) return false
  return (
    (searchResults.value.messages && searchResults.value.messages.length > 0) ||
    (searchResults.value.users && searchResults.value.users.length > 0) ||
    (searchResults.value.rooms && searchResults.value.rooms.length > 0)
  )
})

// Methods
const handleSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }

  if (!searchQuery.value.trim()) {
    searchResults.value = null
    return
  }

  // Debounce search
  searchTimeout.value = setTimeout(() => {
    performLiveSearch()
  }, 300)
}

const performLiveSearch = async () => {
  if (!searchQuery.value.trim()) return

  try {
    const response = await fetch(
      `http://localhost:8000/search/global?query=${encodeURIComponent(searchQuery.value)}&user_id=${props.userId}&limit=10`
    )

    if (response.ok) {
      const data = await response.json()
      searchResults.value = data.results
      emit('search-results', data.results)
    }
  } catch (error) {
    console.error('Search failed:', error)
  }
}

const performSearch = () => {
  if (!searchQuery.value.trim()) return

  // Add to search history
  addToSearchHistory(searchQuery.value)
  
  // Perform full search
  performLiveSearch()
  showResults.value = false
}

const performAdvancedSearch = async () => {
  try {
    const params = new URLSearchParams()
    
    if (advancedQuery.value.query) params.append('query', advancedQuery.value.query)
    if (advancedQuery.value.senderId) params.append('sender_id', advancedQuery.value.senderId)
    if (advancedQuery.value.roomId) params.append('room_id', advancedQuery.value.roomId)
    if (advancedQuery.value.dateFrom) params.append('date_from', advancedQuery.value.dateFrom)
    if (advancedQuery.value.dateTo) params.append('date_to', advancedQuery.value.dateTo)
    if (advancedQuery.value.messageType) params.append('message_type', advancedQuery.value.messageType)
    if (advancedQuery.value.hasAttachments) params.append('has_attachments', 'true')
    
    params.append('user_id', props.userId)

    const response = await fetch(`http://localhost:8000/search/messages?${params}`)

    if (response.ok) {
      const data = await response.json()
      emit('advanced-search', data)
      showAdvancedSearch.value = false
    }
  } catch (error) {
    console.error('Advanced search failed:', error)
  }
}

const clearSearch = () => {
  searchQuery.value = ''
  searchResults.value = null
  showResults.value = false
}

const selectSuggestion = (suggestion) => {
  searchQuery.value = suggestion
  performSearch()
}

const selectMessage = (message) => {
  emit('message-selected', message)
  showResults.value = false
}

const selectUser = (user) => {
  emit('user-selected', user)
  showResults.value = false
}

const selectRoom = (room) => {
  emit('room-selected', room)
  showResults.value = false
}

const showAllMessages = () => {
  // Emit event to show all messages in a dedicated view
  emit('search-results', searchResults.value)
  showResults.value = false
}

const openAdvancedSearch = () => {
  advancedQuery.value.query = searchQuery.value
  showAdvancedSearch.value = true
  showResults.value = false
}

const addToSearchHistory = (query) => {
  const history = JSON.parse(localStorage.getItem('searchHistory') || '[]')
  
  // Remove if already exists
  const index = history.indexOf(query)
  if (index > -1) {
    history.splice(index, 1)
  }
  
  // Add to beginning
  history.unshift(query)
  
  // Keep only last 10 searches
  const trimmed = history.slice(0, 10)
  
  localStorage.setItem('searchHistory', JSON.stringify(trimmed))
  suggestions.value = trimmed
}

const loadSearchHistory = () => {
  const history = JSON.parse(localStorage.getItem('searchHistory') || '[]')
  suggestions.value = history
}

const loadKnownData = async () => {
  try {
    // Load users
    const usersResponse = await fetch(`http://localhost:8000/search/users?query=&limit=100`)
    if (usersResponse.ok) {
      const usersData = await usersResponse.json()
      knownUsers.value = usersData.results || []
    }

    // Load rooms
    const roomsResponse = await fetch(`http://localhost:8000/search/rooms?query=&user_id=${props.userId}&limit=100`)
    if (roomsResponse.ok) {
      const roomsData = await roomsResponse.json()
      knownRooms.value = roomsData.results || []
    }
  } catch (error) {
    console.error('Failed to load known data:', error)
  }
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now - date
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

  if (diffDays === 0) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } else if (diffDays === 1) {
    return 'Yesterday'
  } else if (diffDays < 7) {
    return `${diffDays} days ago`
  } else {
    return date.toLocaleDateString()
  }
}

// Click outside to close
const handleClickOutside = (event) => {
  if (!event.target.closest('.search-bar')) {
    showResults.value = false
  }
}

// Lifecycle
onMounted(() => {
  loadSearchHistory()
  loadKnownData()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
})
</script>

<style scoped>
.search-bar {
  position: relative;
  width: 100%;
  max-width: 500px;
}

.search-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 10px 40px 10px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: #007bff;
}

.clear-btn, .search-btn {
  position: absolute;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.clear-btn {
  right: 35px;
  font-size: 18px;
  color: #666;
}

.search-btn {
  right: 5px;
  font-size: 16px;
  color: #007bff;
}

.clear-btn:hover, .search-btn:hover {
  background: #f8f9fa;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  max-height: 400px;
  overflow-y: auto;
  z-index: 1000;
  margin-top: 4px;
}

.suggestions-section, .live-results {
  padding: 8px 0;
}

.result-section {
  border-bottom: 1px solid #f0f0f0;
  padding: 8px 0;
}

.result-section:last-child {
  border-bottom: none;
}

.result-section h4 {
  margin: 0 0 8px 0;
  padding: 0 16px;
  font-size: 12px;
  color: #666;
  text-transform: uppercase;
  font-weight: 600;
}

.suggestion-item, .result-item {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.suggestion-item:hover, .result-item:hover {
  background: #f8f9fa;
}

.suggestion-icon, .result-icon {
  margin-right: 12px;
  font-size: 16px;
  width: 20px;
  text-align: center;
}

.suggestion-text {
  color: #666;
  font-size: 14px;
}

.result-content {
  flex: 1;
  min-width: 0;
}

.result-title {
  font-weight: 600;
  color: #333;
  font-size: 14px;
  margin-bottom: 2px;
}

.result-description {
  color: #666;
  font-size: 13px;
  line-height: 1.4;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.result-meta {
  display: flex;
  gap: 8px;
  font-size: 11px;
  color: #888;
}

.user-status {
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 10px;
  text-transform: uppercase;
  font-weight: 600;
}

.user-status.online {
  background: #d4edda;
  color: #155724;
}

.user-status.offline {
  background: #f8d7da;
  color: #721c24;
}

.show-more {
  padding: 8px 16px;
  text-align: center;
}

.show-more-btn {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  font-size: 13px;
  text-decoration: underline;
}

.no-results {
  padding: 24px 16px;
  text-align: center;
  color: #666;
}

.no-results-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.no-results-text {
  font-size: 16px;
  margin-bottom: 16px;
}

.no-results-suggestions {
  text-align: left;
  max-width: 200px;
  margin: 0 auto;
}

.no-results-suggestions ul {
  margin: 8px 0;
  padding-left: 20px;
}

.no-results-suggestions li {
  font-size: 13px;
  margin-bottom: 4px;
}

.advanced-search {
  border-top: 1px solid #f0f0f0;
  padding: 8px 16px;
}

.advanced-search-btn {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  font-size: 13px;
  text-decoration: underline;
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
  width: 90%;
  max-width: 600px;
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

.advanced-form {
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.form-input, .form-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-label input {
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

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

/* Highlight search terms */
:deep(mark) {
  background: #fff3cd;
  padding: 1px 2px;
  border-radius: 2px;
}
</style>

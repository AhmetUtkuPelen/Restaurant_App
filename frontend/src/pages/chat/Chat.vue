<template>
  <div class="chat-page">
    <div class="chat-container">
      <!-- Chat Header -->
      <div class="chat-header">
        <div class="chat-info">
          <h1 class="chat-title">💬 ChatApp</h1>
          <div class="online-status">
            <span class="status-indicator" :class="{ online: isConnected }"></span>
            <span class="status-text">{{ isConnected ? 'Connected' : 'Disconnected' }}</span>
          </div>
        </div>
        <div class="chat-actions">
          <button class="btn btn-secondary" @click="clearChat">
            🗑️ Clear Chat
          </button>
          <button class="btn btn-primary" @click="toggleUserList">
            👥 Users ({{ onlineUsers.length }})
          </button>
        </div>
      </div>

      <div class="chat-layout">
        <!-- Users Sidebar -->
        <div class="users-sidebar" :class="{ hidden: !showUserList }">
          <div class="users-header">
            <h3>Online Users</h3>
            <button class="close-btn" @click="toggleUserList">×</button>
          </div>
          <div class="users-list">
            <div
              v-for="user in onlineUsers"
              :key="user.id"
              class="user-item"
              :class="{ current: user.id === currentUser.id }"
            >
              <div class="user-avatar">{{ user.display_name?.charAt(0) || user.username.charAt(0) }}</div>
              <div class="user-info">
                <span class="user-name">{{ user.display_name || user.username }}</span>
                <span class="user-status">{{ user.id === currentUser.id ? '(You)' : 'Online' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Chat Area -->
        <div class="chat-main">
          <!-- Messages Area -->
          <div class="messages-container" ref="messagesContainer">
            <div class="messages-list">
              <div
                v-for="message in messages"
                :key="message.id"
                class="message-wrapper"
                :class="{ 'own-message': message.sender_id === currentUser.id }"
              >
                <div class="message-bubble">
                  <div class="message-header">
                    <span class="sender-name">{{ getSenderName(message.sender_id) }}</span>
                    <span class="message-time">{{ formatTime(message.created_at) }}</span>
                    <div class="message-actions" v-if="message.sender_id === currentUser.id">
                      <button @click="editMessage(message)" class="action-btn">✏️</button>
                      <button @click="deleteMessage(message.id)" class="action-btn">🗑️</button>
                    </div>
                  </div>

                  <!-- Message Content -->
                  <div class="message-content">
                    <div v-if="editingMessageId === message.id" class="edit-form">
                      <textarea
                        v-model="editContent"
                        class="edit-textarea"
                        @keydown.enter.prevent="saveEdit"
                        @keydown.esc="cancelEdit"
                      ></textarea>
                      <div class="edit-actions">
                        <button @click="saveEdit" class="btn btn-sm btn-primary">Save</button>
                        <button @click="cancelEdit" class="btn btn-sm btn-secondary">Cancel</button>
                      </div>
                    </div>
                    <div v-else>
                      <p class="message-text">{{ message.content }}</p>
                      <div v-if="message.is_edited" class="edited-indicator">(edited)</div>
                    </div>
                  </div>

                  <!-- File Attachments -->
                  <div v-if="message.attachments && message.attachments.length" class="message-attachments">
                    <div
                      v-for="attachment in message.attachments"
                      :key="attachment.id"
                      class="attachment-item"
                    >
                      <div v-if="attachment.attachment_type === 'IMAGE'" class="image-attachment">
                        <img
                          :src="attachment.thumbnail_url || attachment.url"
                          :alt="attachment.original_filename"
                          @click="openImageModal(attachment)"
                          class="attachment-image"
                        />
                      </div>
                      <div v-else class="file-attachment">
                        <div class="file-icon">📄</div>
                        <div class="file-info">
                          <span class="file-name">{{ attachment.original_filename }}</span>
                          <span class="file-size">{{ formatFileSize(attachment.file_size) }}</span>
                        </div>
                        <a :href="attachment.url" download class="download-btn">⬇️</a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Message Input Area -->
          <div class="message-input-area">
            <div class="input-container">
              <div class="file-upload-section">
                <input
                  type="file"
                  ref="fileInput"
                  @change="handleFileSelect"
                  multiple
                  accept="image/*,.pdf,.doc,.docx,.txt"
                  style="display: none"
                />
                <button @click="$refs.fileInput.click()" class="file-btn" title="Attach File">
                  📎
                </button>
              </div>

              <div class="text-input-section">
                <textarea
                  v-model="newMessage"
                  @keydown.enter.prevent="sendMessage"
                  @keydown.shift.enter="newMessage += '\n'"
                  placeholder="Type your message... (Enter to send, Shift+Enter for new line)"
                  class="message-input"
                  rows="1"
                  ref="messageInput"
                ></textarea>
              </div>

              <div class="send-section">
                <button
                  @click="sendMessage"
                  :disabled="!newMessage.trim() && selectedFiles.length === 0"
                  class="send-btn"
                >
                  🚀
                </button>
              </div>
            </div>

            <!-- File Preview Area -->
            <div v-if="selectedFiles.length" class="file-preview-area">
              <div class="file-preview-header">
                <span>Selected Files ({{ selectedFiles.length }})</span>
                <button @click="clearSelectedFiles" class="clear-files-btn">Clear All</button>
              </div>
              <div class="file-preview-list">
                <div
                  v-for="(file, index) in selectedFiles"
                  :key="index"
                  class="file-preview-item"
                >
                  <div class="file-preview-info">
                    <span class="file-preview-name">{{ file.name }}</span>
                    <span class="file-preview-size">{{ formatFileSize(file.size) }}</span>
                  </div>
                  <button @click="removeFile(index)" class="remove-file-btn">×</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Image Modal -->
    <div v-if="showImageModal" class="image-modal" @click="closeImageModal">
      <div class="image-modal-content" @click.stop>
        <button class="modal-close-btn" @click="closeImageModal">×</button>
        <img :src="selectedImage.url" :alt="selectedImage.original_filename" class="modal-image" />
        <div class="image-modal-info">
          <p>{{ selectedImage.original_filename }}</p>
          <a :href="selectedImage.url" download class="download-link">Download</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useToast } from '../../composables/useToast'
import { useAuth } from '../../composables/useAuth'

export default {
  name: 'Chat',
  setup() {
    // Toast notifications
    const { showSuccess, showError, showInfo } = useToast()

    // Authentication
    const { currentUser, currentUserId, isAuthenticated } = useAuth()

    // Reactive data
    const messages = ref([])
    const newMessage = ref('')
    const isConnected = ref(false)
    const showUserList = ref(false)
    const onlineUsers = ref([])
    const selectedFiles = ref([])
    const editingMessageId = ref(null)
    const editContent = ref('')
    const showImageModal = ref(false)
    const selectedImage = ref(null)

    // Refs
    const messagesContainer = ref(null)
    const messageInput = ref(null)
    const fileInput = ref(null)

    // WebSocket connection
    let websocket = null

    // Redirect to login if not authenticated
    if (!isAuthenticated.value || !currentUser.value) {
      window.location.href = '/login'
      return
    }

    // WebSocket functions
    const connectWebSocket = () => {
      try {
        websocket = new WebSocket(`ws://localhost:8000/ws/${currentUser.value.id}`)

        websocket.onopen = () => {
          isConnected.value = true
          console.log('Connected to chat server')
          showSuccess('Connected to chat server', 'Connection Established')

          // Add current user to online users if not already there
          if (!onlineUsers.value.find(u => u.id === currentUser.value.id)) {
            onlineUsers.value.push({ ...currentUser.value })
          }
        }

        websocket.onmessage = (event) => {
          const data = JSON.parse(event.data)

          if (data.type === 'user_joined') {
            // Add user to online list
            if (!onlineUsers.value.find(u => u.id === data.user_id)) {
              onlineUsers.value.push({
                id: data.user_id,
                username: data.username || data.user_id,
                display_name: data.display_name || data.username || data.user_id
              })
            }
          } else if (data.type === 'user_left') {
            // Remove user from online list
            onlineUsers.value = onlineUsers.value.filter(u => u.id !== data.user_id)
          } else {
            // Regular message
            const message = {
              id: data.id || Date.now().toString(),
              sender_id: data.user_id || data.sender_id,
              content: data.message || data.content,
              created_at: data.timestamp || new Date().toISOString(),
              is_edited: false,
              attachments: data.attachments || []
            }

            messages.value.push(message)
            scrollToBottom()
          }
        }

        websocket.onclose = () => {
          isConnected.value = false
          console.log('Disconnected from chat server')
          showInfo('Disconnected from chat server. Attempting to reconnect...', 'Connection Lost')

          // Remove current user from online users
          onlineUsers.value = onlineUsers.value.filter(u => u.id !== currentUser.value.id)

          // Attempt to reconnect after 3 seconds
          setTimeout(connectWebSocket, 3000)
        }

        websocket.onerror = (error) => {
          console.error('WebSocket error:', error)
          isConnected.value = false
          showError('Connection error occurred. Please check your internet connection.', 'Connection Error')
        }

      } catch (error) {
        console.error('Failed to connect to WebSocket:', error)
        isConnected.value = false
      }
    }

    // Message functions
    const sendMessage = async () => {
      if (!newMessage.value.trim() && selectedFiles.value.length === 0) return

      try {
        let attachments = []

        // Upload files if any
        if (selectedFiles.value.length > 0) {
          for (const file of selectedFiles.value) {
            const formData = new FormData()
            formData.append('file', file)

            const response = await fetch('http://localhost:8000/files/upload', {
              method: 'POST',
              body: formData
            })

            if (response.ok) {
              const attachment = await response.json()
              attachments.push(attachment)
            }
          }
        }

        const messageData = {
          message: newMessage.value.trim(),
          timestamp: new Date().toISOString(),
          attachments: attachments
        }

        if (websocket && websocket.readyState === WebSocket.OPEN) {
          websocket.send(JSON.stringify(messageData))

          if (attachments.length > 0) {
            showSuccess(`Message sent with ${attachments.length} file(s)`)
          }
        } else {
          showError('Unable to send message. Connection lost.', 'Connection Error')
        }

        // Clear input
        newMessage.value = ''
        selectedFiles.value = []

        // Auto-resize textarea
        if (messageInput.value) {
          messageInput.value.style.height = 'auto'
        }

      } catch (error) {
        console.error('Failed to send message:', error)
        showError('Failed to send message. Please try again.', 'Send Error')
      }
    }

    const editMessage = (message) => {
      editingMessageId.value = message.id
      editContent.value = message.content
    }

    const saveEdit = async () => {
      if (!editContent.value.trim()) return

      try {
        // Find and update the message locally
        const messageIndex = messages.value.findIndex(m => m.id === editingMessageId.value)
        if (messageIndex !== -1) {
          messages.value[messageIndex].content = editContent.value
          messages.value[messageIndex].is_edited = true
        }

        // Cancel edit mode
        cancelEdit()

        showSuccess('Message updated successfully')

        // In a real app, you would send this to the server
        // await updateMessage(editingMessageId.value, editContent.value)

      } catch (error) {
        console.error('Failed to edit message:', error)
        showError('Failed to edit message. Please try again.', 'Edit Error')
      }
    }

    const cancelEdit = () => {
      editingMessageId.value = null
      editContent.value = ''
    }

    const deleteMessage = async (messageId) => {
      if (!confirm('Are you sure you want to delete this message?')) return

      try {
        // Remove message locally
        messages.value = messages.value.filter(m => m.id !== messageId)

        showInfo('Message deleted successfully')

        // In a real app, you would send this to the server
        // await deleteMessageFromServer(messageId)

      } catch (error) {
        console.error('Failed to delete message:', error)
        showError('Failed to delete message. Please try again.', 'Delete Error')
      }
    }

    // File handling functions
    const handleFileSelect = (event) => {
      const files = Array.from(event.target.files)
      selectedFiles.value = [...selectedFiles.value, ...files]

      // Clear the input so the same file can be selected again
      event.target.value = ''
    }

    const removeFile = (index) => {
      selectedFiles.value.splice(index, 1)
    }

    const clearSelectedFiles = () => {
      selectedFiles.value = []
    }

    // Image modal functions
    const openImageModal = (attachment) => {
      selectedImage.value = attachment
      showImageModal.value = true
    }

    const closeImageModal = () => {
      showImageModal.value = false
      selectedImage.value = null
    }

    // Utility functions
    const getSenderName = (senderId) => {
      if (senderId === currentUser.value.id) return 'You'
      const user = onlineUsers.value.find(u => u.id === senderId)
      return user ? (user.display_name || user.username) : 'Unknown User'
    }

    const formatTime = (timestamp) => {
      const date = new Date(timestamp)
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
    }

    const clearChat = () => {
      if (confirm('Are you sure you want to clear all messages?')) {
        messages.value = []
      }
    }

    const toggleUserList = () => {
      showUserList.value = !showUserList.value
    }

    // Lifecycle hooks
    onMounted(() => {
      connectWebSocket()
      scrollToBottom()
    })

    onUnmounted(() => {
      if (websocket) {
        websocket.close()
      }
    })

    return {
      // Data
      messages,
      newMessage,
      isConnected,
      showUserList,
      onlineUsers,
      selectedFiles,
      editingMessageId,
      editContent,
      showImageModal,
      selectedImage,
      currentUser,
      currentUserId,

      // Refs
      messagesContainer,
      messageInput,
      fileInput,

      // Functions
      sendMessage,
      editMessage,
      saveEdit,
      cancelEdit,
      deleteMessage,
      handleFileSelect,
      removeFile,
      clearSelectedFiles,
      openImageModal,
      closeImageModal,
      getSenderName,
      formatTime,
      formatFileSize,
      scrollToBottom,
      clearChat,
      toggleUserList
    }
  }
}
</script>

<style scoped>
.chat-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f9fafb;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* Chat Header */
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom: 1px solid #e5e7eb;
}

.chat-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.chat-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.online-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
  transition: background 0.3s;
}

.status-indicator.online {
  background: #10b981;
}

.chat-actions {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
}

.btn-primary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-primary:hover {
  background: rgba(255, 255, 255, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Chat Layout */
.chat-layout {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* Users Sidebar */
.users-sidebar {
  width: 280px;
  background: #f8fafc;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
}

.users-sidebar.hidden {
  transform: translateX(-100%);
  position: absolute;
  z-index: 10;
}

.users-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
  background: white;
}

.users-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #374151;
}

.users-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-bottom: 0.25rem;
  transition: background 0.2s;
}

.user-item:hover {
  background: rgba(59, 130, 246, 0.1);
}

.user-item.current {
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  text-transform: uppercase;
}

.user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 500;
  color: #1f2937;
  font-size: 0.875rem;
}

.user-status {
  font-size: 0.75rem;
  color: #6b7280;
}

/* Main Chat Area */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: #ffffff;
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.message-wrapper.own-message {
  align-items: flex-end;
}

.message-bubble {
  max-width: 70%;
  background: #f3f4f6;
  border-radius: 1rem;
  padding: 0.75rem 1rem;
  position: relative;
  word-wrap: break-word;
}

.own-message .message-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.75rem;
}

.sender-name {
  font-weight: 600;
  color: #374151;
}

.own-message .sender-name {
  color: rgba(255, 255, 255, 0.9);
}

.message-time {
  color: #9ca3af;
}

.own-message .message-time {
  color: rgba(255, 255, 255, 0.7);
}

.message-actions {
  display: flex;
  gap: 0.25rem;
  margin-left: auto;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.action-btn:hover {
  opacity: 1;
  background: rgba(0, 0, 0, 0.1);
}

.message-content {
  width: 100%;
}

.message-text {
  margin: 0;
  line-height: 1.5;
  color: #1f2937;
  white-space: pre-wrap;
}

.own-message .message-text {
  color: white;
}

.edited-indicator {
  font-size: 0.75rem;
  color: #9ca3af;
  font-style: italic;
  margin-top: 0.25rem;
}

.own-message .edited-indicator {
  color: rgba(255, 255, 255, 0.7);
}

/* Edit Form */
.edit-form {
  width: 100%;
}

.edit-textarea {
  width: 100%;
  min-height: 60px;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  resize: vertical;
  font-family: inherit;
  font-size: 0.875rem;
}

.edit-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.btn-sm {
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
}

/* Message Attachments */
.message-attachments {
  margin-top: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.attachment-item {
  border-radius: 0.5rem;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.image-attachment {
  cursor: pointer;
}

.attachment-image {
  max-width: 200px;
  max-height: 200px;
  border-radius: 0.5rem;
  transition: transform 0.2s;
}

.attachment-image:hover {
  transform: scale(1.02);
}

.file-attachment {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 0.5rem;
}

.file-icon {
  font-size: 1.5rem;
}

.file-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.file-name {
  font-weight: 500;
  color: #1f2937;
  font-size: 0.875rem;
}

.file-size {
  font-size: 0.75rem;
  color: #6b7280;
}

.download-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem;
  border-radius: 0.25rem;
  cursor: pointer;
  text-decoration: none;
  font-size: 1rem;
  transition: background 0.2s;
}

.download-btn:hover {
  background: #2563eb;
}

/* Message Input Area */
.message-input-area {
  border-top: 1px solid #e5e7eb;
  background: white;
  padding: 1rem;
}

.input-container {
  display: flex;
  align-items: flex-end;
  gap: 0.75rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 1rem;
  padding: 0.75rem;
}

.file-upload-section {
  display: flex;
  align-items: center;
}

.file-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s;
}

.file-btn:hover {
  background: #2563eb;
}

.text-input-section {
  flex: 1;
}

.message-input {
  width: 100%;
  min-height: 40px;
  max-height: 120px;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  resize: none;
  font-family: inherit;
  font-size: 0.875rem;
  line-height: 1.5;
  background: white;
  outline: none;
}

.message-input::placeholder {
  color: #9ca3af;
}

.send-section {
  display: flex;
  align-items: center;
}

.send-btn {
  background: #10b981;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  background: #059669;
  transform: scale(1.05);
}

.send-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
  transform: none;
}

/* File Preview Area */
.file-preview-area {
  margin-top: 1rem;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
}

.file-preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.clear-files-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.25rem 0.75rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.75rem;
  transition: background 0.2s;
}

.clear-files-btn:hover {
  background: #dc2626;
}

.file-preview-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.file-preview-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

.file-preview-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.file-preview-name {
  font-weight: 500;
  color: #1f2937;
  font-size: 0.875rem;
}

.file-preview-size {
  font-size: 0.75rem;
  color: #6b7280;
}

.remove-file-btn {
  background: #ef4444;
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.remove-file-btn:hover {
  background: #dc2626;
}

/* Image Modal */
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.image-modal-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
}

.modal-close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1001;
  transition: background 0.2s;
}

.modal-close-btn:hover {
  background: rgba(0, 0, 0, 0.7);
}

.modal-image {
  max-width: 100%;
  max-height: 70vh;
  display: block;
}

.image-modal-info {
  padding: 1rem;
  background: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.image-modal-info p {
  margin: 0;
  font-weight: 500;
  color: #1f2937;
}

.download-link {
  background: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  text-decoration: none;
  font-size: 0.875rem;
  transition: background 0.2s;
}

.download-link:hover {
  background: #2563eb;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .chat-page {
    height: 100vh;
  }

  .chat-container {
    border-radius: 0;
    height: 100vh;
  }

  .chat-header {
    padding: 1rem;
  }

  .chat-title {
    font-size: 1.25rem;
  }

  .users-sidebar {
    position: absolute;
    z-index: 10;
    height: 100%;
    width: 100%;
    max-width: 280px;
  }

  .users-sidebar.hidden {
    transform: translateX(-100%);
  }

  .message-bubble {
    max-width: 85%;
  }

  .input-container {
    flex-direction: column;
    gap: 0.5rem;
    align-items: stretch;
  }

  .file-upload-section,
  .send-section {
    align-self: flex-end;
  }

  .image-modal-content {
    max-width: 95%;
    max-height: 95%;
  }
}

@media (max-width: 480px) {
  .chat-header {
    flex-direction: column;
    gap: 0.5rem;
    align-items: stretch;
  }

  .chat-actions {
    justify-content: center;
  }

  .message-bubble {
    max-width: 90%;
  }
}
</style>
<template>
  <div class="message-component">
    <div class="message-item" :class="{ 'own-message': isOwnMessage }">
      <div class="message-avatar" v-if="!isOwnMessage">
        {{ senderInitial }}
      </div>

      <div class="message-content">
        <div class="message-header">
          <span class="sender-name">{{ senderName }}</span>
          <span class="message-timestamp">{{ formattedTime }}</span>
          <div class="message-actions" v-if="isOwnMessage">
            <button @click="$emit('edit', message)" class="action-btn edit-btn" title="Edit">
              ✏️
            </button>
            <button @click="$emit('delete', message.id)" class="action-btn delete-btn" title="Delete">
              🗑️
            </button>
          </div>
        </div>

        <div class="message-body">
          <!-- Text Content -->
          <div v-if="message.content" class="message-text">
            {{ message.content }}
          </div>

          <!-- Edited Indicator -->
          <div v-if="message.is_edited" class="edited-indicator">
            (edited)
          </div>

          <!-- Attachments -->
          <div v-if="message.attachments && message.attachments.length" class="attachments">
            <div
              v-for="attachment in message.attachments"
              :key="attachment.id"
              class="attachment"
            >
              <!-- Image Attachment -->
              <div v-if="attachment.attachment_type === 'IMAGE'" class="image-attachment">
                <img
                  :src="attachment.thumbnail_url || attachment.url"
                  :alt="attachment.original_filename"
                  @click="$emit('openImage', attachment)"
                  class="attachment-image"
                  loading="lazy"
                />
                <div class="image-overlay">
                  <span class="image-filename">{{ attachment.original_filename }}</span>
                </div>
              </div>

              <!-- File Attachment -->
              <div v-else class="file-attachment">
                <div class="file-icon">
                  {{ getFileIcon(attachment.mime_type) }}
                </div>
                <div class="file-details">
                  <div class="file-name">{{ attachment.original_filename }}</div>
                  <div class="file-meta">
                    <span class="file-size">{{ formatFileSize(attachment.file_size) }}</span>
                    <span class="file-type">{{ getFileType(attachment.mime_type) }}</span>
                  </div>
                </div>
                <a
                  :href="attachment.url"
                  download
                  class="download-button"
                  title="Download file"
                >
                  ⬇️
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- Message Status -->
        <div class="message-status" v-if="isOwnMessage">
          <span class="status-indicator" :class="message.status?.toLowerCase()">
            {{ getStatusIcon(message.status) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'Message',
  props: {
    message: {
      type: Object,
      required: true
    },
    currentUserId: {
      type: String,
      required: true
    },
    senderName: {
      type: String,
      default: 'Unknown User'
    }
  },
  emits: ['edit', 'delete', 'openImage'],
  setup(props) {
    const isOwnMessage = computed(() => {
      return props.message.sender_id === props.currentUserId
    })

    const senderInitial = computed(() => {
      return props.senderName.charAt(0).toUpperCase()
    })

    const formattedTime = computed(() => {
      const date = new Date(props.message.created_at)
      return date.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      })
    })

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    const getFileIcon = (mimeType) => {
      if (mimeType.startsWith('image/')) return '🖼️'
      if (mimeType.startsWith('video/')) return '🎥'
      if (mimeType.startsWith('audio/')) return '🎵'
      if (mimeType.includes('pdf')) return '📄'
      if (mimeType.includes('word') || mimeType.includes('document')) return '📝'
      if (mimeType.includes('excel') || mimeType.includes('spreadsheet')) return '📊'
      if (mimeType.includes('powerpoint') || mimeType.includes('presentation')) return '📽️'
      if (mimeType.includes('zip') || mimeType.includes('rar')) return '🗜️'
      return '📁'
    }

    const getFileType = (mimeType) => {
      const typeMap = {
        'application/pdf': 'PDF',
        'application/msword': 'DOC',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'DOCX',
        'text/plain': 'TXT',
        'image/jpeg': 'JPEG',
        'image/png': 'PNG',
        'image/gif': 'GIF',
        'image/webp': 'WEBP'
      }
      return typeMap[mimeType] || mimeType.split('/')[1]?.toUpperCase() || 'FILE'
    }

    const getStatusIcon = (status) => {
      switch (status?.toLowerCase()) {
        case 'sent': return '✓'
        case 'delivered': return '✓✓'
        case 'read': return '✓✓'
        default: return '⏳'
      }
    }

    return {
      isOwnMessage,
      senderInitial,
      formattedTime,
      formatFileSize,
      getFileIcon,
      getFileType,
      getStatusIcon
    }
  }
}
</script>

<style scoped>
.message-component {
  margin-bottom: 1rem;
}

.message-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  max-width: 80%;
}

.message-item.own-message {
  flex-direction: row-reverse;
  margin-left: auto;
  max-width: 80%;
}

.message-avatar {
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
  flex-shrink: 0;
}

.message-content {
  flex: 1;
  background: #f3f4f6;
  border-radius: 1rem;
  padding: 0.75rem 1rem;
  position: relative;
  word-wrap: break-word;
}

.own-message .message-content {
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

.message-timestamp {
  color: #9ca3af;
}

.own-message .message-timestamp {
  color: rgba(255, 255, 255, 0.7);
}

.message-actions {
  display: flex;
  gap: 0.25rem;
  margin-left: auto;
  opacity: 0;
  transition: opacity 0.2s;
}

.message-item:hover .message-actions {
  opacity: 1;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  transition: all 0.2s;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.message-body {
  line-height: 1.5;
}

.message-text {
  color: #1f2937;
  white-space: pre-wrap;
  margin-bottom: 0.5rem;
}

.own-message .message-text {
  color: white;
}

.edited-indicator {
  font-size: 0.75rem;
  color: #9ca3af;
  font-style: italic;
}

.own-message .edited-indicator {
  color: rgba(255, 255, 255, 0.7);
}

/* Attachments */
.attachments {
  margin-top: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.attachment {
  border-radius: 0.5rem;
  overflow: hidden;
}

.image-attachment {
  position: relative;
  cursor: pointer;
  border-radius: 0.5rem;
  overflow: hidden;
  max-width: 300px;
}

.attachment-image {
  width: 100%;
  height: auto;
  max-height: 200px;
  object-fit: cover;
  transition: transform 0.2s;
}

.attachment-image:hover {
  transform: scale(1.02);
}

.image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  color: white;
  padding: 0.5rem;
  font-size: 0.75rem;
  opacity: 0;
  transition: opacity 0.2s;
}

.image-attachment:hover .image-overlay {
  opacity: 1;
}

.file-attachment {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(255, 255, 255, 0.9);
  padding: 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.own-message .file-attachment {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.2);
}

.file-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.file-details {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-weight: 500;
  color: #1f2937;
  font-size: 0.875rem;
  truncate: true;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.own-message .file-name {
  color: white;
}

.file-meta {
  display: flex;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.own-message .file-meta {
  color: rgba(255, 255, 255, 0.8);
}

.download-button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem;
  border-radius: 0.25rem;
  cursor: pointer;
  text-decoration: none;
  font-size: 1rem;
  transition: all 0.2s;
  flex-shrink: 0;
}

.download-button:hover {
  background: #2563eb;
  transform: scale(1.1);
}

.message-status {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.25rem;
}

.status-indicator {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
}

.status-indicator.read {
  color: #10b981;
}

.status-indicator.delivered {
  color: #3b82f6;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .message-item {
    max-width: 90%;
  }

  .message-item.own-message {
    max-width: 90%;
  }

  .file-attachment {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .file-details {
    width: 100%;
  }

  .download-button {
    align-self: flex-end;
  }
}
</style>
// API service for making HTTP requests to the backend
const API_BASE_URL = 'http://localhost:8000'

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  // Helper method to get auth headers
  getAuthHeaders() {
    const token = localStorage.getItem('authToken')
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  }

  // Helper method to handle API responses
  async handleResponse(response) {
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'An error occurred' }))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }
    return response.json()
  }

  // User Profile APIs
  async getUserProfile(userId) {
    try {
      const response = await fetch(`${this.baseURL}/users/${userId}`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to get user profile:', error)
      throw error
    }
  }

  async getCurrentUserProfile() {
    try {
      const response = await fetch(`${this.baseURL}/users/me`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to get current user profile:', error)
      throw error
    }
  }

  async updateUserProfile(userData) {
    try {
      const response = await fetch(`${this.baseURL}/users/me`, {
        method: 'PUT',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(userData)
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to update user profile:', error)
      throw error
    }
  }

  async uploadAvatar(file) {
    try {
      const formData = new FormData()
      formData.append('avatar', file)

      const token = localStorage.getItem('authToken')
      const headers = {}
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }

      const response = await fetch(`${this.baseURL}/users/me/avatar`, {
        method: 'POST',
        headers,
        body: formData
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to upload avatar:', error)
      throw error
    }
  }

  async changePassword(passwordData) {
    try {
      const response = await fetch(`${this.baseURL}/users/me/password`, {
        method: 'PUT',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(passwordData)
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to change password:', error)
      throw error
    }
  }

  async updateUserStatus(status) {
    try {
      const response = await fetch(`${this.baseURL}/users/me/status`, {
        method: 'PATCH',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ status })
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to update user status:', error)
      throw error
    }
  }

  // User Authentication APIs
  async login(credentials) {
    try {
      const response = await fetch(`${this.baseURL}/users/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to login:', error)
      throw error
    }
  }

  async register(userData) {
    try {
      const response = await fetch(`${this.baseURL}/users/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to register:', error)
      throw error
    }
  }

  // Message APIs
  async getMessages(chatId, limit = 50, offset = 0) {
    try {
      const response = await fetch(`${this.baseURL}/messages?chat_id=${chatId}&limit=${limit}&offset=${offset}`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to get messages:', error)
      throw error
    }
  }

  async sendMessage(messageData) {
    try {
      const response = await fetch(`${this.baseURL}/messages`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(messageData)
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to send message:', error)
      throw error
    }
  }

  async updateMessage(messageId, updateData) {
    try {
      const response = await fetch(`${this.baseURL}/messages/${messageId}`, {
        method: 'PUT',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(updateData)
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to update message:', error)
      throw error
    }
  }

  async deleteMessage(messageId) {
    try {
      const response = await fetch(`${this.baseURL}/messages/${messageId}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to delete message:', error)
      throw error
    }
  }

  // File Upload APIs
  async uploadFile(file, type = 'attachment') {
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('type', type)

      const token = localStorage.getItem('authToken')
      const headers = {}
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }

      const response = await fetch(`${this.baseURL}/files/upload`, {
        method: 'POST',
        headers,
        body: formData
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to upload file:', error)
      throw error
    }
  }

  // Search APIs
  async searchUsers(query, limit = 20) {
    try {
      const response = await fetch(`${this.baseURL}/search/users?query=${encodeURIComponent(query)}&limit=${limit}`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to search users:', error)
      throw error
    }
  }

  async searchMessages(query, filters = {}) {
    try {
      const params = new URLSearchParams({
        query,
        ...filters
      })
      
      const response = await fetch(`${this.baseURL}/search/messages?${params}`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to search messages:', error)
      throw error
    }
  }

  // Room/Chat APIs
  async getRooms() {
    try {
      const response = await fetch(`${this.baseURL}/rooms`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to get rooms:', error)
      throw error
    }
  }

  async createRoom(roomData) {
    try {
      const response = await fetch(`${this.baseURL}/rooms`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(roomData)
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to create room:', error)
      throw error
    }
  }

  async joinRoom(roomId) {
    try {
      const response = await fetch(`${this.baseURL}/rooms/${roomId}/join`, {
        method: 'POST',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to join room:', error)
      throw error
    }
  }

  async leaveRoom(roomId) {
    try {
      const response = await fetch(`${this.baseURL}/rooms/${roomId}/leave`, {
        method: 'POST',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to leave room:', error)
      throw error
    }
  }

  // Reaction APIs
  async addReaction(messageId, emoji) {
    try {
      const response = await fetch(`${this.baseURL}/reactions`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ message_id: messageId, emoji })
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to add reaction:', error)
      throw error
    }
  }

  async removeReaction(messageId, emoji) {
    try {
      const response = await fetch(`${this.baseURL}/reactions/${messageId}/${emoji}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to remove reaction:', error)
      throw error
    }
  }

  // Admin APIs
  async getAdminDashboardStats() {
    try {
      const response = await fetch(`${this.baseURL}/admin/dashboard/stats`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to get admin dashboard stats:', error)
      throw error
    }
  }

  async getAdminUsers(params = {}) {
    try {
      const queryParams = new URLSearchParams(params)
      const response = await fetch(`${this.baseURL}/admin/users?${queryParams}`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to get admin users:', error)
      throw error
    }
  }

  async getRecentMessages(limit = 50) {
    try {
      const response = await fetch(`${this.baseURL}/admin/messages/recent?limit=${limit}`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to get recent messages:', error)
      throw error
    }
  }

  async getSystemHealth() {
    try {
      const response = await fetch(`${this.baseURL}/admin/system/health`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to get system health:', error)
      throw error
    }
  }

  async banUser(userId) {
    try {
      const response = await fetch(`${this.baseURL}/admin/users/${userId}/ban`, {
        method: 'POST',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to ban user:', error)
      throw error
    }
  }

  async unbanUser(userId) {
    try {
      const response = await fetch(`${this.baseURL}/admin/users/${userId}/unban`, {
        method: 'POST',
        headers: this.getAuthHeaders()
      })
      return await this.handleResponse(response)
    } catch (error) {
      console.error('Failed to unban user:', error)
      throw error
    }
  }
}

// Create and export a singleton instance
const apiService = new ApiService()
export default apiService

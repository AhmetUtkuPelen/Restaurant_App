import { ApiResponse, User, Message, ChatRoom, AdminStats, LoginResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    // Get token from localStorage
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Auth endpoints
  async register(userData: { username: string; email: string; password: string; display_name?: string }) {
    return this.request<LoginResponse>('/users/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(credentials: { username_or_email: string; password: string }) {
    return this.request<LoginResponse>('/users/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async getCurrentUser() {
    return this.request<User>('/users/me');
  }

  async updateUser(userId: string, userData: { display_name?: string; bio?: string; avatar_url?: string }) {
    return this.request<User>(`/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  async updatePassword(userId: string, passwordData: { current_password: string; new_password: string }) {
    return this.request<ApiResponse>(`/users/${userId}/password`, {
      method: 'PUT',
      body: JSON.stringify(passwordData),
    });
  }

  // User endpoints
  async getUsers(limit: number = 50) {
    return this.request<{ users: User[] }>(`/users?limit=${limit}`);
  }

  async searchUsers(query: string) {
    return this.request<{ users: User[] }>(`/users/search?q=${encodeURIComponent(query)}`);
  }

  async updateUserStatus(status: 'ONLINE' | 'OFFLINE' | 'AWAY' | 'BUSY') {
    return this.request<ApiResponse>('/users/status', {
      method: 'PUT',
      body: JSON.stringify({ status }),
    });
  }

  // Message endpoints
  async getMessages(chatId?: string, recipientId?: string, limit: number = 50) {
    const params = new URLSearchParams();
    if (chatId) params.append('chat_id', chatId);
    if (recipientId) params.append('recipient_id', recipientId);
    params.append('limit', limit.toString());
    
    return this.request<{ messages: Message[] }>(`/messages?${params.toString()}`);
  }

  async sendMessage(messageData: { content: string; chat_id?: string; recipient_id?: string; message_type?: string }) {
    return this.request<Message>('/messages', {
      method: 'POST',
      body: JSON.stringify(messageData),
    });
  }

  async updateMessage(messageId: string, content: string) {
    return this.request<Message>(`/messages/${messageId}`, {
      method: 'PUT',
      body: JSON.stringify({ content }),
    });
  }

  async deleteMessage(messageId: string) {
    return this.request<ApiResponse>(`/messages/${messageId}`, {
      method: 'DELETE',
    });
  }

  // Room endpoints
  async getRooms() {
    return this.request<{ rooms: ChatRoom[] }>('/rooms');
  }

  async getPublicRooms() {
    return this.request<{ public_rooms: ChatRoom[] }>('/rooms/public');
  }

  async createRoom(roomData: { name: string; description?: string; is_private?: boolean }) {
    return this.request<{ room: ChatRoom }>('/rooms', {
      method: 'POST',
      body: JSON.stringify(roomData),
    });
  }

  async joinRoom(roomId: string, userId: string) {
    return this.request<ApiResponse>(`/rooms/${roomId}/join`, {
      method: 'POST',
      body: JSON.stringify({ user_id: userId }),
    });
  }

  async leaveRoom(roomId: string, userId: string) {
    return this.request<ApiResponse>(`/rooms/${roomId}/leave`, {
      method: 'POST',
      body: JSON.stringify({ user_id: userId }),
    });
  }

  // Reaction endpoints
  async addReaction(messageId: string, emoji: string, emojiName?: string) {
    return this.request<ApiResponse>('/reactions', {
      method: 'POST',
      body: JSON.stringify({ message_id: messageId, emoji, emoji_name: emojiName }),
    });
  }

  async removeReaction(reactionId: string) {
    return this.request<ApiResponse>(`/reactions/${reactionId}`, {
      method: 'DELETE',
    });
  }

  // File upload endpoints
  async uploadFile(file: File, onProgress?: (progress: number) => void) {
    const formData = new FormData();
    formData.append('file', file);

    return new Promise<{ file_url: string; filename: string; file_size: number }>((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      
      if (onProgress) {
        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable) {
            const progress = (e.loaded / e.total) * 100;
            onProgress(progress);
          }
        });
      }

      xhr.addEventListener('load', () => {
        if (xhr.status === 200) {
          resolve(JSON.parse(xhr.responseText));
        } else {
          reject(new Error(`Upload failed: ${xhr.statusText}`));
        }
      });

      xhr.addEventListener('error', () => {
        reject(new Error('Upload failed'));
      });

      const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
      if (token) {
        xhr.setRequestHeader('Authorization', `Bearer ${token}`);
      }

      xhr.open('POST', `${this.baseURL}/files/upload`);
      xhr.send(formData);
    });
  }

  // Admin endpoints
  async getAdminStats() {
    return this.request<AdminStats>('/admin/stats');
  }

  async getAllUsers() {
    return this.request<{ users: User[] }>('/admin/users');
  }

  async deleteUser(userId: string) {
    return this.request<ApiResponse>(`/admin/users/${userId}`, {
      method: 'DELETE',
    });
  }

  async getAllRooms() {
    return this.request<{ rooms: ChatRoom[] }>('/admin/rooms');
  }

  async deleteRoom(roomId: string) {
    return this.request<ApiResponse>(`/admin/rooms/${roomId}`, {
      method: 'DELETE',
    });
  }
}

export const api = new ApiClient(API_BASE_URL);

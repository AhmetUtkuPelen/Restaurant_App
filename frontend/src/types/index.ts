// User types
export interface User {
  id: string;
  username: string;
  email: string;
  display_name?: string;
  avatar_url?: string;
  bio?: string;
  status: 'ONLINE' | 'OFFLINE' | 'AWAY' | 'BUSY';
  role: 'USER' | 'ADMIN' | 'MODERATOR';
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  last_seen?: string;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  display_name?: string;
}

export interface UserLogin {
  username_or_email: string;
  password: string;
}

export interface UserUpdate {
  display_name?: string;
  bio?: string;
  avatar_url?: string;
}

// Message types
export interface Message {
  id: string;
  sender_id: string;
  chat_id?: string;
  recipient_id?: string;
  content: string;
  message_type: 'TEXT' | 'IMAGE' | 'FILE' | 'AUDIO' | 'VIDEO';
  reply_to_message_id?: string;
  status: 'SENT' | 'DELIVERED' | 'READ';
  is_edited: boolean;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
  attachments?: Attachment[];
  reactions?: Reaction[];
  sender?: User;
}

export interface MessageCreate {
  content: string;
  chat_id?: string;
  recipient_id?: string;
  message_type?: 'TEXT' | 'IMAGE' | 'FILE' | 'AUDIO' | 'VIDEO';
  reply_to_message_id?: string;
  attachments?: Attachment[];
}

export interface Attachment {
  id: string;
  filename: string;
  file_url: string;
  file_size: number;
  file_type: string;
  thumbnail_url?: string;
}

export interface Reaction {
  id: string;
  message_id: string;
  user_id: string;
  emoji: string;
  emoji_name?: string;
  created_at: string;
}

// Chat Room types
export interface ChatRoom {
  id: string;
  name: string;
  description?: string;
  is_private: boolean;
  created_by: string;
  created_at: string;
  updated_at: string;
  members: string[];
  admins: string[];
  member_count?: number;
  last_message?: Message;
}

export interface ChatRoomCreate {
  name: string;
  description?: string;
  is_private?: boolean;
}

// WebSocket types
export interface WebSocketMessage {
  type: 'message' | 'user_joined' | 'user_left' | 'typing' | 'stop_typing' | 'reaction' | 'room_created' | 'user_joined_room';
  data: any;
  timestamp: string;
}

// API Response types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  has_next: boolean;
  has_prev: boolean;
}

// Auth types
export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface LoginResponse {
  user: User;
  token: string;
  message: string;
}

// Chat state types
export interface ChatState {
  messages: Message[];
  rooms: ChatRoom[];
  currentRoom: ChatRoom | null;
  onlineUsers: User[];
  typingUsers: string[];
  isConnected: boolean;
}

// Admin types
export interface AdminStats {
  total_users: number;
  online_users: number;
  total_messages: number;
  messages_today: number;
  total_rooms: number;
  active_rooms: number;
}

// Form types
export interface FormErrors {
  [key: string]: string;
}

// File upload types
export interface FileUploadProgress {
  file: File;
  progress: number;
  status: 'uploading' | 'completed' | 'error';
  url?: string;
  error?: string;
}

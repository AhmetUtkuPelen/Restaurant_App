import { io, Socket } from 'socket.io-client';
import { Message, User, WebSocketMessage } from '@/types';

class WebSocketManager {
  private socket: Socket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private isConnecting = false;

  // Event listeners
  private messageListeners: ((message: Message) => void)[] = [];
  private userJoinedListeners: ((user: User) => void)[] = [];
  private userLeftListeners: ((userId: string) => void)[] = [];
  private typingListeners: ((userId: string, isTyping: boolean) => void)[] = [];
  private connectionListeners: ((isConnected: boolean) => void)[] = [];
  private reactionListeners: ((data: any) => void)[] = [];

  connect(userId: string, userInfo: User): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.socket?.connected) {
        resolve();
        return;
      }

      if (this.isConnecting) {
        return;
      }

      this.isConnecting = true;
      const token = localStorage.getItem('token');
      
      if (!token) {
        this.isConnecting = false;
        reject(new Error('No authentication token found'));
        return;
      }

      const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
      
      this.socket = io(wsUrl, {
        auth: {
          token,
          user_id: userId,
          user_info: userInfo,
        },
        transports: ['websocket'],
        upgrade: false,
      });

      this.socket.on('connect', () => {
        console.log('WebSocket connected');
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.notifyConnectionListeners(true);
        resolve();
      });

      this.socket.on('disconnect', (reason) => {
        console.log('WebSocket disconnected:', reason);
        this.notifyConnectionListeners(false);
        
        if (reason === 'io server disconnect') {
          // Server disconnected, try to reconnect
          this.handleReconnect(userId, userInfo);
        }
      });

      this.socket.on('connect_error', (error) => {
        console.error('WebSocket connection error:', error);
        this.isConnecting = false;
        this.notifyConnectionListeners(false);
        
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.handleReconnect(userId, userInfo);
        } else {
          reject(error);
        }
      });

      // Message events
      this.socket.on('message', (data: Message) => {
        this.notifyMessageListeners(data);
      });

      this.socket.on('user_joined', (data: User) => {
        this.notifyUserJoinedListeners(data);
      });

      this.socket.on('user_left', (data: { user_id: string }) => {
        this.notifyUserLeftListeners(data.user_id);
      });

      this.socket.on('typing', (data: { user_id: string }) => {
        this.notifyTypingListeners(data.user_id, true);
      });

      this.socket.on('stop_typing', (data: { user_id: string }) => {
        this.notifyTypingListeners(data.user_id, false);
      });

      this.socket.on('reaction', (data: any) => {
        this.notifyReactionListeners(data);
      });

      // Set connection timeout
      setTimeout(() => {
        if (this.isConnecting) {
          this.isConnecting = false;
          reject(new Error('Connection timeout'));
        }
      }, 10000);
    });
  }

  private handleReconnect(userId: string, userInfo: User) {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
    
    console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);
    
    setTimeout(() => {
      this.connect(userId, userInfo).catch((error) => {
        console.error('Reconnection failed:', error);
      });
    }, delay);
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
    this.isConnecting = false;
    this.reconnectAttempts = 0;
    this.notifyConnectionListeners(false);
  }

  sendMessage(message: string, chatId?: string, recipientId?: string) {
    if (!this.socket?.connected) {
      throw new Error('WebSocket not connected');
    }

    this.socket.emit('message', {
      message,
      chat_id: chatId,
      recipient_id: recipientId,
      timestamp: new Date().toISOString(),
    });
  }

  sendTyping(isTyping: boolean, chatId?: string, recipientId?: string) {
    if (!this.socket?.connected) return;

    this.socket.emit(isTyping ? 'typing' : 'stop_typing', {
      chat_id: chatId,
      recipient_id: recipientId,
    });
  }

  joinRoom(roomId: string) {
    if (!this.socket?.connected) return;
    this.socket.emit('join_room', { room_id: roomId });
  }

  leaveRoom(roomId: string) {
    if (!this.socket?.connected) return;
    this.socket.emit('leave_room', { room_id: roomId });
  }

  // Event listener management
  onMessage(callback: (message: Message) => void) {
    this.messageListeners.push(callback);
    return () => {
      this.messageListeners = this.messageListeners.filter(cb => cb !== callback);
    };
  }

  onUserJoined(callback: (user: User) => void) {
    this.userJoinedListeners.push(callback);
    return () => {
      this.userJoinedListeners = this.userJoinedListeners.filter(cb => cb !== callback);
    };
  }

  onUserLeft(callback: (userId: string) => void) {
    this.userLeftListeners.push(callback);
    return () => {
      this.userLeftListeners = this.userLeftListeners.filter(cb => cb !== callback);
    };
  }

  onTyping(callback: (userId: string, isTyping: boolean) => void) {
    this.typingListeners.push(callback);
    return () => {
      this.typingListeners = this.typingListeners.filter(cb => cb !== callback);
    };
  }

  onConnection(callback: (isConnected: boolean) => void) {
    this.connectionListeners.push(callback);
    return () => {
      this.connectionListeners = this.connectionListeners.filter(cb => cb !== callback);
    };
  }

  onReaction(callback: (data: any) => void) {
    this.reactionListeners.push(callback);
    return () => {
      this.reactionListeners = this.reactionListeners.filter(cb => cb !== callback);
    };
  }

  // Notification methods
  private notifyMessageListeners(message: Message) {
    this.messageListeners.forEach(callback => callback(message));
  }

  private notifyUserJoinedListeners(user: User) {
    this.userJoinedListeners.forEach(callback => callback(user));
  }

  private notifyUserLeftListeners(userId: string) {
    this.userLeftListeners.forEach(callback => callback(userId));
  }

  private notifyTypingListeners(userId: string, isTyping: boolean) {
    this.typingListeners.forEach(callback => callback(userId, isTyping));
  }

  private notifyConnectionListeners(isConnected: boolean) {
    this.connectionListeners.forEach(callback => callback(isConnected));
  }

  private notifyReactionListeners(data: any) {
    this.reactionListeners.forEach(callback => callback(data));
  }

  get isConnected(): boolean {
    return this.socket?.connected || false;
  }
}

export const wsManager = new WebSocketManager();

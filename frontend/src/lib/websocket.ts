import { Message, User, WebSocketMessage } from '@/types';

class WebSocketManager {
  private socket: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private isConnecting = false;
  private userId: string | null = null;

  // Event listeners
  private messageListeners: ((message: Message) => void)[] = [];
  private userJoinedListeners: ((user: User) => void)[] = [];
  private userLeftListeners: ((userId: string) => void)[] = [];
  private typingListeners: ((userId: string, isTyping: boolean) => void)[] = [];
  private connectionListeners: ((isConnected: boolean) => void)[] = [];
  private reactionListeners: ((data: any) => void)[] = [];

  connect(userId: string, userInfo: User): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.socket?.readyState === WebSocket.OPEN) {
        resolve();
        return;
      }

      if (this.isConnecting) {
        return;
      }

      this.isConnecting = true;
      this.userId = userId;

      const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
      const wsEndpoint = `${wsUrl}/ws/${userId}`;

      try {
        this.socket = new WebSocket(wsEndpoint);
      } catch (error) {
        this.isConnecting = false;
        reject(error);
        return;
      }

      this.socket.onopen = () => {
        console.log('WebSocket connected');
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.notifyConnectionListeners(true);
        resolve();
      };

      this.socket.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason);
        this.notifyConnectionListeners(false);

        // Try to reconnect unless it was a clean close
        if (event.code !== 1000) {
          this.handleReconnect(userId, userInfo);
        }
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket connection error:', error);
        this.isConnecting = false;
        this.notifyConnectionListeners(false);

        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.handleReconnect(userId, userInfo);
        } else {
          reject(error);
        }
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          // Handle different message types based on the data structure
          if (data.type === 'message' || data.content) {
            this.notifyMessageListeners(data);
          } else if (data.type === 'user_joined') {
            this.notifyUserJoinedListeners(data.user);
          } else if (data.type === 'user_left') {
            this.notifyUserLeftListeners(data.user_id);
          } else if (data.type === 'typing') {
            this.notifyTypingListeners(data.user_id, true);
          } else if (data.type === 'stop_typing') {
            this.notifyTypingListeners(data.user_id, false);
          } else if (data.type === 'reaction') {
            this.notifyReactionListeners(data);
          } else {
            // Default to treating as message
            this.notifyMessageListeners(data);
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

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
      this.socket.close(1000, 'Client disconnect');
      this.socket = null;
    }
    this.isConnecting = false;
    this.reconnectAttempts = 0;
    this.notifyConnectionListeners(false);
  }

  sendMessage(message: string, chatId?: string, recipientId?: string) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket not connected');
    }

    const messageData = {
      message,
      chat_id: chatId,
      recipient_id: recipientId,
      timestamp: new Date().toISOString(),
    };

    this.socket.send(JSON.stringify(messageData));
  }

  sendTyping(isTyping: boolean, chatId?: string, recipientId?: string) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;

    const typingData = {
      type: isTyping ? 'typing' : 'stop_typing',
      chat_id: chatId,
      recipient_id: recipientId,
    };

    this.socket.send(JSON.stringify(typingData));
  }

  joinRoom(roomId: string) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;

    const joinData = {
      type: 'join_room',
      room_id: roomId
    };

    this.socket.send(JSON.stringify(joinData));
  }

  leaveRoom(roomId: string) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;

    const leaveData = {
      type: 'leave_room',
      room_id: roomId
    };

    this.socket.send(JSON.stringify(leaveData));
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

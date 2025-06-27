'use client';

import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react';
import { Message, User, ChatRoom, ChatState } from '@/types';
import { useAuth } from './AuthContext';
import { wsManager } from '@/lib/websocket';
import { api } from '@/lib/api';

interface ChatContextType extends ChatState {
  sendMessage: (content: string, chatId?: string, recipientId?: string) => void;
  loadMessages: (chatId?: string, recipientId?: string) => Promise<void>;
  loadRooms: () => Promise<void>;
  joinRoom: (roomId: string) => Promise<void>;
  leaveRoom: (roomId: string) => Promise<void>;
  setCurrentRoom: (room: ChatRoom | null) => void;
  startTyping: (chatId?: string, recipientId?: string) => void;
  stopTyping: (chatId?: string, recipientId?: string) => void;
  addReaction: (messageId: string, emoji: string) => Promise<void>;
  editMessage: (messageId: string, content: string) => Promise<void>;
  deleteMessage: (messageId: string) => Promise<void>;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

type ChatAction =
  | { type: 'SET_MESSAGES'; payload: Message[] }
  | { type: 'ADD_MESSAGE'; payload: Message }
  | { type: 'UPDATE_MESSAGE'; payload: { id: string; updates: Partial<Message> } }
  | { type: 'DELETE_MESSAGE'; payload: string }
  | { type: 'SET_ROOMS'; payload: ChatRoom[] }
  | { type: 'ADD_ROOM'; payload: ChatRoom }
  | { type: 'SET_CURRENT_ROOM'; payload: ChatRoom | null }
  | { type: 'SET_ONLINE_USERS'; payload: User[] }
  | { type: 'ADD_ONLINE_USER'; payload: User }
  | { type: 'REMOVE_ONLINE_USER'; payload: string }
  | { type: 'SET_TYPING_USERS'; payload: string[] }
  | { type: 'ADD_TYPING_USER'; payload: string }
  | { type: 'REMOVE_TYPING_USER'; payload: string }
  | { type: 'SET_CONNECTION_STATUS'; payload: boolean };

const chatReducer = (state: ChatState, action: ChatAction): ChatState => {
  switch (action.type) {
    case 'SET_MESSAGES':
      return { ...state, messages: action.payload };
    case 'ADD_MESSAGE':
      return { 
        ...state, 
        messages: [...state.messages, action.payload].sort((a, b) => 
          new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
        )
      };
    case 'UPDATE_MESSAGE':
      return {
        ...state,
        messages: state.messages.map(msg =>
          msg.id === action.payload.id ? { ...msg, ...action.payload.updates } : msg
        ),
      };
    case 'DELETE_MESSAGE':
      return {
        ...state,
        messages: state.messages.filter(msg => msg.id !== action.payload),
      };
    case 'SET_ROOMS':
      return { ...state, rooms: action.payload };
    case 'ADD_ROOM':
      return { ...state, rooms: [...state.rooms, action.payload] };
    case 'SET_CURRENT_ROOM':
      return { ...state, currentRoom: action.payload };
    case 'SET_ONLINE_USERS':
      return { ...state, onlineUsers: action.payload };
    case 'ADD_ONLINE_USER':
      return {
        ...state,
        onlineUsers: state.onlineUsers.find(u => u.id === action.payload.id)
          ? state.onlineUsers
          : [...state.onlineUsers, action.payload],
      };
    case 'REMOVE_ONLINE_USER':
      return {
        ...state,
        onlineUsers: state.onlineUsers.filter(u => u.id !== action.payload),
      };
    case 'SET_TYPING_USERS':
      return { ...state, typingUsers: action.payload };
    case 'ADD_TYPING_USER':
      return {
        ...state,
        typingUsers: state.typingUsers.includes(action.payload)
          ? state.typingUsers
          : [...state.typingUsers, action.payload],
      };
    case 'REMOVE_TYPING_USER':
      return {
        ...state,
        typingUsers: state.typingUsers.filter(id => id !== action.payload),
      };
    case 'SET_CONNECTION_STATUS':
      return { ...state, isConnected: action.payload };
    default:
      return state;
  }
};

const initialState: ChatState = {
  messages: [],
  rooms: [],
  currentRoom: null,
  onlineUsers: [],
  typingUsers: [],
  isConnected: false,
};

interface ChatProviderProps {
  children: ReactNode;
}

export function ChatProvider({ children }: ChatProviderProps) {
  const [state, dispatch] = useReducer(chatReducer, initialState);
  const { user, isAuthenticated } = useAuth();

  // Initialize WebSocket connection when user is authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      const initializeWebSocket = async () => {
        try {
          await wsManager.connect(user.id, user);
          
          // Set up event listeners
          const unsubscribeMessage = wsManager.onMessage((message) => {
            dispatch({ type: 'ADD_MESSAGE', payload: message });
          });

          const unsubscribeUserJoined = wsManager.onUserJoined((joinedUser) => {
            dispatch({ type: 'ADD_ONLINE_USER', payload: joinedUser });
          });

          const unsubscribeUserLeft = wsManager.onUserLeft((userId) => {
            dispatch({ type: 'REMOVE_ONLINE_USER', payload: userId });
          });

          const unsubscribeTyping = wsManager.onTyping((userId, isTyping) => {
            if (isTyping) {
              dispatch({ type: 'ADD_TYPING_USER', payload: userId });
            } else {
              dispatch({ type: 'REMOVE_TYPING_USER', payload: userId });
            }
          });

          const unsubscribeConnection = wsManager.onConnection((isConnected) => {
            dispatch({ type: 'SET_CONNECTION_STATUS', payload: isConnected });
          });

          // Cleanup function
          return () => {
            unsubscribeMessage();
            unsubscribeUserJoined();
            unsubscribeUserLeft();
            unsubscribeTyping();
            unsubscribeConnection();
          };
        } catch (error) {
          console.error('Failed to initialize WebSocket:', error);
        }
      };

      initializeWebSocket();
    }

    return () => {
      if (wsManager.isConnected) {
        wsManager.disconnect();
      }
    };
  }, [isAuthenticated, user]);

  const sendMessage = (content: string, chatId?: string, recipientId?: string) => {
    if (!wsManager.isConnected) {
      throw new Error('Not connected to chat server');
    }
    wsManager.sendMessage(content, chatId, recipientId);
  };

  const loadMessages = async (chatId?: string, recipientId?: string) => {
    try {
      const response = await api.getMessages(chatId, recipientId);
      dispatch({ type: 'SET_MESSAGES', payload: response.messages });
    } catch (error) {
      console.error('Failed to load messages:', error);
    }
  };

  const loadRooms = async () => {
    try {
      const response = await api.getRooms();
      dispatch({ type: 'SET_ROOMS', payload: response.rooms });
    } catch (error) {
      console.error('Failed to load rooms:', error);
    }
  };

  const joinRoom = async (roomId: string) => {
    if (!user) return;
    
    try {
      await api.joinRoom(roomId, user.id);
      wsManager.joinRoom(roomId);
      
      // Find and set the current room
      const room = state.rooms.find(r => r.id === roomId);
      if (room) {
        dispatch({ type: 'SET_CURRENT_ROOM', payload: room });
      }
    } catch (error) {
      console.error('Failed to join room:', error);
      throw error;
    }
  };

  const leaveRoom = async (roomId: string) => {
    if (!user) return;
    
    try {
      await api.leaveRoom(roomId, user.id);
      wsManager.leaveRoom(roomId);
      
      if (state.currentRoom?.id === roomId) {
        dispatch({ type: 'SET_CURRENT_ROOM', payload: null });
      }
    } catch (error) {
      console.error('Failed to leave room:', error);
      throw error;
    }
  };

  const setCurrentRoom = (room: ChatRoom | null) => {
    dispatch({ type: 'SET_CURRENT_ROOM', payload: room });
  };

  const startTyping = (chatId?: string, recipientId?: string) => {
    wsManager.sendTyping(true, chatId, recipientId);
  };

  const stopTyping = (chatId?: string, recipientId?: string) => {
    wsManager.sendTyping(false, chatId, recipientId);
  };

  const addReaction = async (messageId: string, emoji: string) => {
    try {
      await api.addReaction(messageId, emoji);
    } catch (error) {
      console.error('Failed to add reaction:', error);
      throw error;
    }
  };

  const editMessage = async (messageId: string, content: string) => {
    try {
      const updatedMessage = await api.updateMessage(messageId, content);
      dispatch({ 
        type: 'UPDATE_MESSAGE', 
        payload: { id: messageId, updates: { content, is_edited: true } }
      });
    } catch (error) {
      console.error('Failed to edit message:', error);
      throw error;
    }
  };

  const deleteMessage = async (messageId: string) => {
    try {
      await api.deleteMessage(messageId);
      dispatch({ type: 'DELETE_MESSAGE', payload: messageId });
    } catch (error) {
      console.error('Failed to delete message:', error);
      throw error;
    }
  };

  const value: ChatContextType = {
    ...state,
    sendMessage,
    loadMessages,
    loadRooms,
    joinRoom,
    leaveRoom,
    setCurrentRoom,
    startTyping,
    stopTyping,
    addReaction,
    editMessage,
    deleteMessage,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}

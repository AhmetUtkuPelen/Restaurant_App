'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useChat } from '@/contexts/ChatContext';
import Header from '@/components/layout/Header';
import { Send, Smile, Paperclip, Users, Settings, Wifi, WifiOff } from 'lucide-react';
import { formatDate, scrollToBottom } from '@/lib/utils';

export default function ChatPage() {
  const [message, setMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messageInputRef = useRef<HTMLInputElement>(null);
  const typingTimeoutRef = useRef<NodeJS.Timeout>();

  const { user } = useAuth();
  const {
    messages,
    onlineUsers,
    typingUsers,
    isConnected,
    sendMessage,
    loadMessages,
    startTyping,
    stopTyping,
  } = useChat();

  // Load messages on component mount
  useEffect(() => {
    loadMessages();
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom(messagesEndRef.current);
  }, [messages]);

  // Handle typing indicators
  const handleTyping = () => {
    if (!isTyping) {
      setIsTyping(true);
      startTyping();
    }

    // Clear existing timeout
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }

    // Set new timeout to stop typing
    typingTimeoutRef.current = setTimeout(() => {
      setIsTyping(false);
      stopTyping();
    }, 1000);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!message.trim() || !isConnected) return;

    try {
      sendMessage(message.trim());
      setMessage('');
      
      // Stop typing indicator
      if (isTyping) {
        setIsTyping(false);
        stopTyping();
        if (typingTimeoutRef.current) {
          clearTimeout(typingTimeoutRef.current);
        }
      }
      
      // Focus back to input
      messageInputRef.current?.focus();
    } catch (error) {
      console.error('Failed to send message:', error);
      // You could show a toast notification here
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const getTypingText = () => {
    if (!typingUsers || !onlineUsers) return '';

    const typingUsernames = typingUsers
      .filter(userId => userId !== user?.id)
      .map(userId => {
        const typingUser = onlineUsers.find(u => u.id === userId);
        return typingUser?.display_name || typingUser?.username || 'Someone';
      });

    if (typingUsernames.length === 0) return '';
    if (typingUsernames.length === 1) return `${typingUsernames[0]} is typing...`;
    if (typingUsernames.length === 2) return `${typingUsernames[0]} and ${typingUsernames[1]} are typing...`;
    return `${typingUsernames[0]} and ${typingUsernames.length - 1} others are typing...`;
  };

  return (
    <div className="min-h-screen flex flex-col bg-base-100">
      <Header />
      
      <div className="flex-1 flex">
        {/* Sidebar */}
        <div className="w-80 bg-base-200 border-r border-base-300 flex flex-col">
          {/* Connection Status */}
          <div className={`p-4 border-b border-base-300 ${isConnected ? 'bg-success/10' : 'bg-error/10'}`}>
            <div className="flex items-center gap-2">
              {isConnected ? (
                <>
                  <Wifi size={16} className="text-success" />
                  <span className="text-sm text-success">Connected</span>
                </>
              ) : (
                <>
                  <WifiOff size={16} className="text-error" />
                  <span className="text-sm text-error">Disconnected</span>
                </>
              )}
            </div>
          </div>

          {/* Online Users */}
          <div className="p-4 border-b border-base-300">
            <div className="flex items-center gap-2 mb-3">
              <Users size={16} />
              <span className="font-semibold">Online Users ({onlineUsers?.length || 0})</span>
            </div>
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {onlineUsers?.map((onlineUser) => (
                <div key={onlineUser.id} className="flex items-center gap-2">
                  <div className="avatar placeholder">
                    <div className="bg-neutral text-neutral-content rounded-full w-8">
                      <span className="text-xs">
                        {(onlineUser.display_name || onlineUser.username).charAt(0).toUpperCase()}
                      </span>
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate">
                      {onlineUser.display_name || onlineUser.username}
                      {onlineUser.id === user?.id && ' (You)'}
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 bg-success rounded-full"></div>
                      <span className="text-xs text-base-content/70">Online</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Room Settings */}
          <div className="p-4">
            <button className="btn btn-outline btn-sm w-full">
              <Settings size={16} />
              Room Settings
            </button>
          </div>
        </div>

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Chat Header */}
          <div className="p-4 border-b border-base-300 bg-base-200">
            <h1 className="text-xl font-bold">Global Chat</h1>
            <p className="text-sm text-base-content/70">
              Welcome to the main chat room. Be respectful and have fun!
            </p>
          </div>

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {!messages || messages.length === 0 ? (
              <div className="text-center text-base-content/50 py-8">
                <p>No messages yet. Start the conversation!</p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div key={msg.id || `message-${index}`} className={`chat ${msg.sender_id === user?.id ? 'chat-end' : 'chat-start'}`}>
                  <div className="chat-image avatar">
                    <div className="w-10 rounded-full bg-neutral text-neutral-content flex items-center justify-center">
                      <span className="text-sm">
                        {(msg.sender?.display_name || msg.sender?.username || 'U').charAt(0).toUpperCase()}
                      </span>
                    </div>
                  </div>
                  <div className="chat-header">
                    {msg.sender?.display_name || msg.sender?.username || 'Unknown User'}
                    <time className="text-xs opacity-50 ml-2">
                      {formatDate(msg.created_at)}
                    </time>
                    {msg.is_edited && (
                      <span className="text-xs opacity-50 ml-2">(edited)</span>
                    )}
                  </div>
                  <div className={`chat-bubble ${msg.sender_id === user?.id ? 'chat-bubble-primary' : ''}`}>
                    {msg.content}
                  </div>
                  {msg.reactions && msg.reactions.length > 0 && (
                    <div className="chat-footer">
                      <div className="flex gap-1 mt-1">
                        {msg.reactions.map((reaction, index) => (
                          <span key={index} className="text-xs bg-base-200 px-2 py-1 rounded">
                            {reaction.emoji} {reaction.count}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))
            )}
            
            {/* Typing Indicator */}
            {getTypingText() && (
              <div className="chat chat-start">
                <div className="chat-bubble chat-bubble-accent opacity-70">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <span className="text-xs ml-2">{getTypingText()}</span>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Message Input */}
          <div className="p-4 border-t border-base-300 bg-base-200">
            <form onSubmit={handleSubmit} className="flex gap-2">
              <button
                type="button"
                className="btn btn-ghost btn-circle"
                disabled={!isConnected}
              >
                <Paperclip size={20} />
              </button>
              
              <div className="flex-1 relative">
                <input
                  ref={messageInputRef}
                  type="text"
                  value={message}
                  onChange={(e) => {
                    setMessage(e.target.value);
                    handleTyping();
                  }}
                  onKeyPress={handleKeyPress}
                  placeholder={isConnected ? "Type a message..." : "Connecting..."}
                  className="input input-bordered w-full pr-12"
                  disabled={!isConnected}
                  maxLength={1000}
                />
                <button
                  type="button"
                  className="btn btn-ghost btn-circle absolute right-1 top-1/2 transform -translate-y-1/2"
                  disabled={!isConnected}
                >
                  <Smile size={20} />
                </button>
              </div>
              
              <button
                type="submit"
                className="btn btn-primary"
                disabled={!message.trim() || !isConnected}
              >
                <Send size={20} />
              </button>
            </form>
            
            <div className="text-xs text-base-content/50 mt-2">
              Press Enter to send, Shift+Enter for new line
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

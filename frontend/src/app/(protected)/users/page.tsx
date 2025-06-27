'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import Header from '@/components/layout/Header';
import { Search, MessageCircle, UserPlus, Users, Filter, Grid, List } from 'lucide-react';
import { User } from '@/types';
import { api } from '@/lib/api';
import { debounce } from '@/lib/utils';

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [filterRole, setFilterRole] = useState<'all' | 'user' | 'admin'>('all');

  const { user: currentUser } = useAuth();

  // Debounced search function
  const debouncedSearch = debounce((term: string) => {
    const filtered = users.filter(user =>
      (user.username.toLowerCase().includes(term.toLowerCase()) ||
       user.display_name?.toLowerCase().includes(term.toLowerCase()) ||
       user.email.toLowerCase().includes(term.toLowerCase())) &&
      (filterRole === 'all' || user.role === filterRole)
    );
    setFilteredUsers(filtered);
  }, 300);

  // Load users on component mount
  useEffect(() => {
    const loadUsers = async () => {
      try {
        setIsLoading(true);
        const response = await api.getUsers();
        setUsers(response.users);
        setFilteredUsers(response.users);
      } catch (error) {
        console.error('Failed to load users:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadUsers();
  }, []);

  // Handle search and filter changes
  useEffect(() => {
    debouncedSearch(searchTerm);
  }, [searchTerm, users, filterRole]);

  const handleStartChat = async (userId: string) => {
    try {
      // This would typically create a private chat or navigate to existing one
      console.log('Starting chat with user:', userId);
      // You could implement navigation to a private chat here
    } catch (error) {
      console.error('Failed to start chat:', error);
    }
  };

  const getUserStatusColor = (user: User) => {
    // This would typically check if user is online
    // For now, we'll use a simple random status
    return Math.random() > 0.5 ? 'bg-success' : 'bg-base-300';
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex flex-col bg-base-100">
        <Header />
        <div className="flex-1 flex items-center justify-center">
          <span className="loading loading-spinner loading-lg"></span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-base-100">
      <Header />
      
      <div className="flex-1 container mx-auto px-4 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Users Directory</h1>
          <p className="text-base-content/70">
            Find and connect with other users in the community
          </p>
        </div>

        {/* Search and Filters */}
        <div className="card bg-base-200 shadow-lg mb-6">
          <div className="card-body">
            <div className="flex flex-col lg:flex-row gap-4">
              {/* Search Input */}
              <div className="flex-1 relative">
                <input
                  type="text"
                  placeholder="Search users by name, username, or email..."
                  className="input input-bordered w-full pl-10"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-base-content/50" size={18} />
              </div>

              {/* Role Filter */}
              <div className="flex items-center gap-2">
                <Filter size={18} />
                <select
                  className="select select-bordered"
                  value={filterRole}
                  onChange={(e) => setFilterRole(e.target.value as 'all' | 'user' | 'admin')}
                >
                  <option value="all">All Roles</option>
                  <option value="user">Users</option>
                  <option value="admin">Admins</option>
                </select>
              </div>

              {/* View Mode Toggle */}
              <div className="join">
                <button
                  className={`btn join-item ${viewMode === 'grid' ? 'btn-active' : ''}`}
                  onClick={() => setViewMode('grid')}
                >
                  <Grid size={18} />
                </button>
                <button
                  className={`btn join-item ${viewMode === 'list' ? 'btn-active' : ''}`}
                  onClick={() => setViewMode('list')}
                >
                  <List size={18} />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Results Count */}
        <div className="mb-4">
          <p className="text-sm text-base-content/70">
            Showing {filteredUsers.length} of {users.length} users
          </p>
        </div>

        {/* Users Grid/List */}
        {filteredUsers.length === 0 ? (
          <div className="text-center py-12">
            <Users size={48} className="mx-auto text-base-content/30 mb-4" />
            <h3 className="text-lg font-semibold mb-2">No users found</h3>
            <p className="text-base-content/70">
              {searchTerm ? 'Try adjusting your search terms' : 'No users match the current filters'}
            </p>
          </div>
        ) : (
          <div className={viewMode === 'grid' 
            ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'
            : 'space-y-4'
          }>
            {filteredUsers.map((user) => (
              <div key={user.id} className={`card bg-base-100 shadow-lg hover:shadow-xl transition-shadow ${
                viewMode === 'list' ? 'card-side' : ''
              }`}>
                <div className="card-body">
                  <div className="flex items-start gap-4">
                    {/* Avatar */}
                    <div className="avatar placeholder">
                      <div className="bg-neutral text-neutral-content rounded-full w-12">
                        <span className="text-lg">
                          {(user.display_name || user.username).charAt(0).toUpperCase()}
                        </span>
                      </div>
                      {/* Online Status Indicator */}
                      <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-base-100 ${getUserStatusColor(user)}`}></div>
                    </div>

                    {/* User Info */}
                    <div className="flex-1 min-w-0">
                      <h3 className="card-title text-base">
                        {user.display_name || user.username}
                        {user.id === currentUser?.id && (
                          <span className="badge badge-primary badge-sm">You</span>
                        )}
                      </h3>
                      <p className="text-sm text-base-content/70 truncate">
                        @{user.username}
                      </p>
                      {user.role === 'admin' && (
                        <div className="badge badge-warning badge-sm mt-1">Admin</div>
                      )}
                    </div>
                  </div>

                  {/* User Stats */}
                  <div className="stats stats-horizontal shadow mt-4">
                    <div className="stat py-2 px-3">
                      <div className="stat-title text-xs">Joined</div>
                      <div className="stat-value text-sm">
                        {new Date(user.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  {user.id !== currentUser?.id && (
                    <div className="card-actions justify-end mt-4">
                      <button
                        className="btn btn-primary btn-sm"
                        onClick={() => handleStartChat(user.id)}
                      >
                        <MessageCircle size={16} />
                        Chat
                      </button>
                      <button className="btn btn-outline btn-sm">
                        <UserPlus size={16} />
                        Add Friend
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import Header from '@/components/layout/Header';
import { 
  Users, 
  MessageSquare, 
  Shield, 
  Activity, 
  TrendingUp, 
  Calendar,
  Search,
  MoreVertical,
  Ban,
  UserCheck,
  Trash2
} from 'lucide-react';
import { User, AdminStats } from '@/types';
import { api } from '@/lib/api';

export default function AdminPage() {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  const { user } = useAuth();
  const router = useRouter();

  // Check if user is admin
  useEffect(() => {
    if (user && user.role !== 'admin') {
      router.push('/chat');
      return;
    }
  }, [user, router]);

  // Load admin data
  useEffect(() => {
    const loadAdminData = async () => {
      try {
        setIsLoading(true);
        const [statsResponse, usersResponse] = await Promise.all([
          api.getAdminStats(),
          api.getUsers()
        ]);
        
        setStats(statsResponse);
        setUsers(usersResponse.users);
      } catch (error) {
        console.error('Failed to load admin data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    if (user?.role === 'admin') {
      loadAdminData();
    }
  }, [user]);

  const handleUserAction = async (userId: string, action: 'ban' | 'unban' | 'delete') => {
    try {
      switch (action) {
        case 'ban':
          await api.banUser(userId);
          break;
        case 'unban':
          await api.unbanUser(userId);
          break;
        case 'delete':
          await api.deleteUser(userId);
          break;
      }
      
      // Refresh users list
      const usersResponse = await api.getUsers();
      setUsers(usersResponse.users);
      setSelectedUser(null);
    } catch (error) {
      console.error(`Failed to ${action} user:`, error);
    }
  };

  const filteredUsers = users.filter(u =>
    u.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.display_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (user?.role !== 'admin') {
    return null; // Will redirect in useEffect
  }

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
          <h1 className="text-3xl font-bold mb-2">Admin Dashboard</h1>
          <p className="text-base-content/70">
            Manage users, monitor activity, and oversee the chat application
          </p>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="stat bg-base-200 rounded-lg shadow-lg">
              <div className="stat-figure text-primary">
                <Users size={32} />
              </div>
              <div className="stat-title">Total Users</div>
              <div className="stat-value text-primary">{stats.total_users}</div>
              <div className="stat-desc">
                {stats.new_users_today} new today
              </div>
            </div>

            <div className="stat bg-base-200 rounded-lg shadow-lg">
              <div className="stat-figure text-secondary">
                <MessageSquare size={32} />
              </div>
              <div className="stat-title">Messages Today</div>
              <div className="stat-value text-secondary">{stats.messages_today}</div>
              <div className="stat-desc">
                <TrendingUp size={16} className="inline mr-1" />
                {stats.total_messages} total
              </div>
            </div>

            <div className="stat bg-base-200 rounded-lg shadow-lg">
              <div className="stat-figure text-accent">
                <Activity size={32} />
              </div>
              <div className="stat-title">Online Users</div>
              <div className="stat-value text-accent">{stats.online_users}</div>
              <div className="stat-desc">Currently active</div>
            </div>

            <div className="stat bg-base-200 rounded-lg shadow-lg">
              <div className="stat-figure text-warning">
                <Shield size={32} />
              </div>
              <div className="stat-title">Active Rooms</div>
              <div className="stat-value text-warning">{stats.active_rooms}</div>
              <div className="stat-desc">
                <Calendar size={16} className="inline mr-1" />
                This week
              </div>
            </div>
          </div>
        )}

        {/* User Management */}
        <div className="card bg-base-200 shadow-lg">
          <div className="card-body">
            <div className="flex items-center justify-between mb-6">
              <h2 className="card-title text-xl">User Management</h2>
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search users..."
                  className="input input-bordered pl-10"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-base-content/50" size={18} />
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="table table-zebra w-full">
                <thead>
                  <tr>
                    <th>User</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Joined</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map((u) => (
                    <tr key={u.id}>
                      <td>
                        <div className="flex items-center gap-3">
                          <div className="avatar placeholder">
                            <div className="bg-neutral text-neutral-content rounded-full w-8">
                              <span className="text-xs">
                                {(u.display_name || u.username).charAt(0).toUpperCase()}
                              </span>
                            </div>
                          </div>
                          <div>
                            <div className="font-bold">{u.display_name || u.username}</div>
                            <div className="text-sm opacity-50">@{u.username}</div>
                          </div>
                        </div>
                      </td>
                      <td>{u.email}</td>
                      <td>
                        <div className={`badge ${u.role === 'admin' ? 'badge-warning' : 'badge-ghost'}`}>
                          {u.role}
                        </div>
                      </td>
                      <td>
                        <div className={`badge ${u.is_active ? 'badge-success' : 'badge-error'}`}>
                          {u.is_active ? 'Active' : 'Banned'}
                        </div>
                      </td>
                      <td>{new Date(u.created_at).toLocaleDateString()}</td>
                      <td>
                        {u.id !== user?.id && (
                          <div className="dropdown dropdown-end">
                            <label tabIndex={0} className="btn btn-ghost btn-sm">
                              <MoreVertical size={16} />
                            </label>
                            <ul tabIndex={0} className="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
                              {u.is_active ? (
                                <li>
                                  <button
                                    onClick={() => handleUserAction(u.id, 'ban')}
                                    className="text-warning"
                                  >
                                    <Ban size={16} />
                                    Ban User
                                  </button>
                                </li>
                              ) : (
                                <li>
                                  <button
                                    onClick={() => handleUserAction(u.id, 'unban')}
                                    className="text-success"
                                  >
                                    <UserCheck size={16} />
                                    Unban User
                                  </button>
                                </li>
                              )}
                              <li>
                                <button
                                  onClick={() => handleUserAction(u.id, 'delete')}
                                  className="text-error"
                                >
                                  <Trash2 size={16} />
                                  Delete User
                                </button>
                              </li>
                            </ul>
                          </div>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {filteredUsers.length === 0 && (
              <div className="text-center py-8">
                <Users size={48} className="mx-auto text-base-content/30 mb-4" />
                <p className="text-base-content/70">No users found</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

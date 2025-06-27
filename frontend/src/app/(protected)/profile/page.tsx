'use client';

import React, { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import Header from '@/components/layout/Header';
import { Edit, Save, X, Camera, Mail, User, Calendar, Shield, Key } from 'lucide-react';
import { isValidEmail, isValidUsername } from '@/lib/utils';

export default function ProfilePage() {
  const { user, updateUser, updatePassword } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const [profileData, setProfileData] = useState({
    username: user?.username || '',
    display_name: user?.display_name || '',
    email: user?.email || '',
  });

  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setProfileData(prev => ({ ...prev, [name]: value }));
    
    // Clear specific field error
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPasswordData(prev => ({ ...prev, [name]: value }));
    
    // Clear specific field error
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateProfile = () => {
    const newErrors: { [key: string]: string } = {};

    if (!profileData.username) {
      newErrors.username = 'Username is required';
    } else if (!isValidUsername(profileData.username)) {
      newErrors.username = 'Username must be 3-20 characters, alphanumeric and underscores only';
    }

    if (!profileData.email) {
      newErrors.email = 'Email is required';
    } else if (!isValidEmail(profileData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const validatePassword = () => {
    const newErrors: { [key: string]: string } = {};

    if (!passwordData.currentPassword) {
      newErrors.currentPassword = 'Current password is required';
    }

    if (!passwordData.newPassword) {
      newErrors.newPassword = 'New password is required';
    } else if (passwordData.newPassword.length < 6) {
      newErrors.newPassword = 'Password must be at least 6 characters long';
    }

    if (!passwordData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your new password';
    } else if (passwordData.newPassword !== passwordData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSaveProfile = async () => {
    if (!validateProfile()) return;

    setIsLoading(true);
    try {
      await updateUser(profileData);
      setIsEditing(false);
      setErrors({});
    } catch (error: any) {
      setErrors({ general: error.message || 'Failed to update profile' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSavePassword = async () => {
    if (!validatePassword()) return;

    setIsLoading(true);
    try {
      await updatePassword(passwordData.currentPassword, passwordData.newPassword);
      setIsChangingPassword(false);
      setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
      setErrors({});
    } catch (error: any) {
      setErrors({ password: error.message || 'Failed to update password' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setProfileData({
      username: user?.username || '',
      display_name: user?.display_name || '',
      email: user?.email || '',
    });
    setIsEditing(false);
    setErrors({});
  };

  const handleCancelPassword = () => {
    setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
    setIsChangingPassword(false);
    setErrors({});
  };

  if (!user) {
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
      
      <div className="flex-1 container mx-auto px-4 py-8 max-w-4xl">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Profile Settings</h1>
          <p className="text-base-content/70">
            Manage your account information and preferences
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Profile Picture Section */}
          <div className="lg:col-span-1">
            <div className="card bg-base-200 shadow-lg">
              <div className="card-body items-center text-center">
                <div className="avatar placeholder mb-4">
                  <div className="bg-neutral text-neutral-content rounded-full w-24">
                    <span className="text-3xl">
                      {(user.display_name || user.username).charAt(0).toUpperCase()}
                    </span>
                  </div>
                </div>
                <h3 className="text-xl font-bold">{user.display_name || user.username}</h3>
                <p className="text-base-content/70">@{user.username}</p>
                {user.role === 'admin' && (
                  <div className="badge badge-warning">Admin</div>
                )}
                <button className="btn btn-outline btn-sm mt-4">
                  <Camera size={16} />
                  Change Photo
                </button>
              </div>
            </div>

            {/* Account Stats */}
            <div className="card bg-base-200 shadow-lg mt-6">
              <div className="card-body">
                <h3 className="card-title text-lg mb-4">Account Stats</h3>
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <Calendar size={16} className="text-base-content/70" />
                    <div>
                      <p className="text-sm text-base-content/70">Member since</p>
                      <p className="font-medium">{new Date(user.created_at).toLocaleDateString()}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Shield size={16} className="text-base-content/70" />
                    <div>
                      <p className="text-sm text-base-content/70">Role</p>
                      <p className="font-medium capitalize">{user.role}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Profile Information */}
          <div className="lg:col-span-2 space-y-6">
            {/* General Information */}
            <div className="card bg-base-200 shadow-lg">
              <div className="card-body">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="card-title">General Information</h3>
                  {!isEditing ? (
                    <button
                      className="btn btn-outline btn-sm"
                      onClick={() => setIsEditing(true)}
                    >
                      <Edit size={16} />
                      Edit
                    </button>
                  ) : (
                    <div className="flex gap-2">
                      <button
                        className="btn btn-primary btn-sm"
                        onClick={handleSaveProfile}
                        disabled={isLoading}
                      >
                        {isLoading ? (
                          <span className="loading loading-spinner loading-xs"></span>
                        ) : (
                          <Save size={16} />
                        )}
                        Save
                      </button>
                      <button
                        className="btn btn-outline btn-sm"
                        onClick={handleCancelEdit}
                        disabled={isLoading}
                      >
                        <X size={16} />
                        Cancel
                      </button>
                    </div>
                  )}
                </div>

                {errors.general && (
                  <div className="alert alert-error mb-4">
                    <span>{errors.general}</span>
                  </div>
                )}

                <div className="space-y-4">
                  <div className="form-control">
                    <label className="label">
                      <span className="label-text">Username</span>
                    </label>
                    <div className="relative">
                      <input
                        type="text"
                        name="username"
                        value={profileData.username}
                        onChange={handleProfileChange}
                        className={`input input-bordered w-full pl-10 ${errors.username ? 'input-error' : ''}`}
                        disabled={!isEditing}
                      />
                      <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-base-content/50" size={18} />
                    </div>
                    {errors.username && (
                      <label className="label">
                        <span className="label-text-alt text-error">{errors.username}</span>
                      </label>
                    )}
                  </div>

                  <div className="form-control">
                    <label className="label">
                      <span className="label-text">Display Name</span>
                    </label>
                    <div className="relative">
                      <input
                        type="text"
                        name="display_name"
                        value={profileData.display_name}
                        onChange={handleProfileChange}
                        className="input input-bordered w-full pl-10"
                        disabled={!isEditing}
                        placeholder="Your display name"
                      />
                      <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-base-content/50" size={18} />
                    </div>
                  </div>

                  <div className="form-control">
                    <label className="label">
                      <span className="label-text">Email</span>
                    </label>
                    <div className="relative">
                      <input
                        type="email"
                        name="email"
                        value={profileData.email}
                        onChange={handleProfileChange}
                        className={`input input-bordered w-full pl-10 ${errors.email ? 'input-error' : ''}`}
                        disabled={!isEditing}
                      />
                      <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-base-content/50" size={18} />
                    </div>
                    {errors.email && (
                      <label className="label">
                        <span className="label-text-alt text-error">{errors.email}</span>
                      </label>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Password Section */}
            <div className="card bg-base-200 shadow-lg">
              <div className="card-body">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="card-title">Password & Security</h3>
                  {!isChangingPassword ? (
                    <button
                      className="btn btn-outline btn-sm"
                      onClick={() => setIsChangingPassword(true)}
                    >
                      <Key size={16} />
                      Change Password
                    </button>
                  ) : (
                    <div className="flex gap-2">
                      <button
                        className="btn btn-primary btn-sm"
                        onClick={handleSavePassword}
                        disabled={isLoading}
                      >
                        {isLoading ? (
                          <span className="loading loading-spinner loading-xs"></span>
                        ) : (
                          <Save size={16} />
                        )}
                        Update
                      </button>
                      <button
                        className="btn btn-outline btn-sm"
                        onClick={handleCancelPassword}
                        disabled={isLoading}
                      >
                        <X size={16} />
                        Cancel
                      </button>
                    </div>
                  )}
                </div>

                {errors.password && (
                  <div className="alert alert-error mb-4">
                    <span>{errors.password}</span>
                  </div>
                )}

                {isChangingPassword ? (
                  <div className="space-y-4">
                    <div className="form-control">
                      <label className="label">
                        <span className="label-text">Current Password</span>
                      </label>
                      <input
                        type="password"
                        name="currentPassword"
                        value={passwordData.currentPassword}
                        onChange={handlePasswordChange}
                        className={`input input-bordered w-full ${errors.currentPassword ? 'input-error' : ''}`}
                        placeholder="Enter current password"
                      />
                      {errors.currentPassword && (
                        <label className="label">
                          <span className="label-text-alt text-error">{errors.currentPassword}</span>
                        </label>
                      )}
                    </div>

                    <div className="form-control">
                      <label className="label">
                        <span className="label-text">New Password</span>
                      </label>
                      <input
                        type="password"
                        name="newPassword"
                        value={passwordData.newPassword}
                        onChange={handlePasswordChange}
                        className={`input input-bordered w-full ${errors.newPassword ? 'input-error' : ''}`}
                        placeholder="Enter new password"
                      />
                      {errors.newPassword && (
                        <label className="label">
                          <span className="label-text-alt text-error">{errors.newPassword}</span>
                        </label>
                      )}
                    </div>

                    <div className="form-control">
                      <label className="label">
                        <span className="label-text">Confirm New Password</span>
                      </label>
                      <input
                        type="password"
                        name="confirmPassword"
                        value={passwordData.confirmPassword}
                        onChange={handlePasswordChange}
                        className={`input input-bordered w-full ${errors.confirmPassword ? 'input-error' : ''}`}
                        placeholder="Confirm new password"
                      />
                      {errors.confirmPassword && (
                        <label className="label">
                          <span className="label-text-alt text-error">{errors.confirmPassword}</span>
                        </label>
                      )}
                    </div>
                  </div>
                ) : (
                  <p className="text-base-content/70">
                    Keep your account secure by using a strong password and changing it regularly.
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

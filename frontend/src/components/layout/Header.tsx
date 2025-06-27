'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { User, LogOut, Settings, MessageCircle, Users, Shield } from 'lucide-react';
import Image from 'next/image';

export default function Header() {
  const { user, logout, isAuthenticated } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <header className="navbar bg-primary text-primary-content shadow-lg">
      <div className="navbar-start">
        <Link href="/" className="btn btn-ghost text-xl font-bold">
          💬 ChatApp
        </Link>
      </div>

      <div className="navbar-center hidden lg:flex">
        {isAuthenticated && (
          <ul className="menu menu-horizontal px-1">
            <li>
              <Link href="/chat" className="flex items-center gap-2">
                <MessageCircle size={18} />
                Chat
              </Link>
            </li>
            <li>
              <Link href="/users" className="flex items-center gap-2">
                <Users size={18} />
                Users
              </Link>
            </li>
            {user?.role === 'ADMIN' && (
              <li>
                <Link href="/admin" className="flex items-center gap-2">
                  <Shield size={18} />
                  Admin
                </Link>
              </li>
            )}
          </ul>
        )}
      </div>

      <div className="navbar-end">
        {isAuthenticated ? (
          <div className="dropdown dropdown-end">
            <div tabIndex={0} role="button" className="btn btn-ghost btn-circle avatar">
              <div className="w-10 rounded-full">
                {user?.avatar_url ? (
                  <Image
                    width={40}
                    height={40}
                    alt={user.display_name || user.username}
                    src={user.avatar_url}
                    className="rounded-full"
                  />
                ) : (
                  <div className="avatar placeholder">
                    <div className="bg-neutral text-neutral-content rounded-full w-10">
                      <span className="text-sm">
                        {user?.display_name?.charAt(0) || user?.username?.charAt(0) || 'U'}
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </div>
            <ul
              tabIndex={0}
              className="menu menu-sm dropdown-content bg-base-100 text-base-content rounded-box z-[1] mt-3 w-52 p-2 shadow"
            >
              <li className="menu-title">
                <span>{user?.display_name || user?.username}</span>
              </li>
              <li>
                <Link href="/profile" className="flex items-center gap-2">
                  <User size={16} />
                  Profile
                </Link>
              </li>
              <li>
                <Link href="/settings" className="flex items-center gap-2">
                  <Settings size={16} />
                  Settings
                </Link>
              </li>
              <div className="divider my-1"></div>
              <li>
                <button onClick={handleLogout} className="flex items-center gap-2 text-error">
                  <LogOut size={16} />
                  Logout
                </button>
              </li>
            </ul>
          </div>
        ) : (
          <div className="flex gap-2">
            <Link href="/login" className="btn btn-info text-white">
              Login
            </Link>
            <Link href="/register" className="btn btn-info text-white">
              Sign Up
            </Link>
          </div>
        )}
      </div>

      {/* Mobile menu */}
      {isAuthenticated && (
        <div className="navbar-start lg:hidden">
          <div className="dropdown">
            <div tabIndex={0} role="button" className="btn btn-ghost btn-circle">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M4 6h16M4 12h16M4 18h7"
                />
              </svg>
            </div>
            <ul
              tabIndex={0}
              className="menu menu-sm dropdown-content bg-base-100 text-base-content rounded-box z-[1] mt-3 w-52 p-2 shadow"
            >
              <li>
                <Link href="/chat" className="flex items-center gap-2">
                  <MessageCircle size={18} />
                  Chat
                </Link>
              </li>
              <li>
                <Link href="/users" className="flex items-center gap-2">
                  <Users size={18} />
                  Users
                </Link>
              </li>
              {user?.role === 'ADMIN' && (
                <li>
                  <Link href="/admin" className="flex items-center gap-2">
                    <Shield size={18} />
                    Admin
                  </Link>
                </li>
              )}
            </ul>
          </div>
        </div>
      )}
    </header>
  );
}

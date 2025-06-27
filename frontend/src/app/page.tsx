'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import { MessageCircle, Users, Shield, Zap, Globe, Lock } from 'lucide-react';

export default function Home() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1">
        {/* Hero Section */}
        <section className="hero min-h-[80vh] bg-gradient-to-br from-primary to-info">
          <div className="hero-content text-center text-primary-content">
            <div className="max-w-md">
              <h1 className="mb-5 text-5xl font-bold">Real-time Chat</h1>
              <p className="mb-5 text-lg">
                Connect with people instantly through our modern, fast, and secure chat application.
                Built with cutting-edge technology for the best user experience.
              </p>
              {isAuthenticated ? (
                <Link href="/chat" className="btn btn-accent btn-lg">
                  Go to Chat
                </Link>
              ) : (
                <div className="flex gap-4 justify-center">
                  <Link href="/register" className="btn btn-outline btn-lg">
                    Get Started
                  </Link>
                  <Link href="/login" className="btn btn-outline btn-lg">
                    Login
                  </Link>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-base-100">
          <div className="container mx-auto px-4">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold mb-4">Features</h2>
              <p className="text-lg text-base-content/70">
                Everything you need for modern communication
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              <div className="card bg-base-200 shadow-xl">
                <div className="card-body items-center text-center">
                  <MessageCircle size={48} className="text-primary mb-4" />
                  <h3 className="card-title">Real-time Messaging</h3>
                  <p>Instant message delivery with WebSocket technology for seamless communication.</p>
                </div>
              </div>

              <div className="card bg-base-200 shadow-xl">
                <div className="card-body items-center text-center">
                  <Users size={48} className="text-secondary mb-4" />
                  <h3 className="card-title">User Management</h3>
                  <p>Find and connect with users, create private chats and group conversations.</p>
                </div>
              </div>

              <div className="card bg-base-200 shadow-xl">
                <div className="card-body items-center text-center">
                  <Shield size={48} className="text-accent mb-4" />
                  <h3 className="card-title">Admin Dashboard</h3>
                  <p>Comprehensive admin tools for user and room management with real-time analytics.</p>
                </div>
              </div>

              <div className="card bg-base-200 shadow-xl">
                <div className="card-body items-center text-center">
                  <Zap size={48} className="text-warning mb-4" />
                  <h3 className="card-title">Fast & Responsive</h3>
                  <p>Built with Next.js and optimized for speed with modern web technologies.</p>
                </div>
              </div>

              <div className="card bg-base-200 shadow-xl">
                <div className="card-body items-center text-center">
                  <Globe size={48} className="text-info mb-4" />
                  <h3 className="card-title">Cross-platform</h3>
                  <p>Works seamlessly across all devices and browsers with responsive design.</p>
                </div>
              </div>

              <div className="card bg-base-200 shadow-xl">
                <div className="card-body items-center text-center">
                  <Lock size={48} className="text-success mb-4" />
                  <h3 className="card-title">Secure</h3>
                  <p>End-to-end security with JWT authentication and secure data transmission.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Tech Stack Section */}
        <section className="py-20 bg-base-200">
          <div className="container mx-auto px-4">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold mb-4">Tech Stack</h2>
              <p className="text-lg text-base-content/70">
                Built with modern, reliable technologies
              </p>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="bg-base-100 rounded-lg p-6 shadow-lg">
                  <h3 className="font-bold text-lg mb-2">Frontend</h3>
                  <div className="space-y-2">
                    <div className="badge badge-primary">Next.js 15</div>
                    <div className="badge badge-secondary">React 19</div>
                    <div className="badge badge-accent">TypeScript</div>
                    <div className="badge badge-neutral">Tailwind CSS</div>
                    <div className="badge badge-info">DaisyUI</div>
                  </div>
                </div>
              </div>

              <div className="text-center">
                <div className="bg-base-100 rounded-lg p-6 shadow-lg">
                  <h3 className="font-bold text-lg mb-2">Backend</h3>
                  <div className="space-y-2">
                    <div className="badge badge-primary">FastAPI</div>
                    <div className="badge badge-secondary">Python</div>
                    <div className="badge badge-accent">SQLAlchemy</div>
                    <div className="badge badge-neutral">SQLite</div>
                  </div>
                </div>
              </div>

              <div className="text-center">
                <div className="bg-base-100 rounded-lg p-6 shadow-lg">
                  <h3 className="font-bold text-lg mb-2">Real-time</h3>
                  <div className="space-y-2">
                    <div className="badge badge-primary">WebSocket</div>
                    <div className="badge badge-secondary">Socket.IO</div>
                    <div className="badge badge-accent">Real-time Events</div>
                  </div>
                </div>
              </div>

              <div className="text-center">
                <div className="bg-base-100 rounded-lg p-6 shadow-lg">
                  <h3 className="font-bold text-lg mb-2">Security</h3>
                  <div className="space-y-2">
                    <div className="badge badge-primary">JWT</div>
                    <div className="badge badge-secondary">CORS</div>
                    <div className="badge badge-accent">Authentication</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        {!isAuthenticated && (
          <section className="py-20 bg-primary text-primary-content">
            <div className="container mx-auto px-4 text-center">
              <h2 className="text-4xl font-bold mb-4">Ready to Start Chatting?</h2>
              <p className="text-lg mb-8">
                Join our community and experience real-time communication like never before.
              </p>
              <div className="flex gap-4 justify-center">
                <Link href="/register" className="btn btn-outline btn-lg">
                  Create Account
                </Link>
                <Link href="/login" className="btn btn-outline btn-lg">
                  Sign In
                </Link>
              </div>
            </div>
          </section>
        )}
      </main>

      <Footer />
    </div>
  );
}

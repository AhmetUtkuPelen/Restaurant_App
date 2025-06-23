<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          Connect with Friends & Colleagues
        </h1>
        <p class="hero-description">
          Experience seamless real-time messaging with our secure and fast chat platform.
          Stay connected wherever you are.
        </p>
        <div class="hero-actions">
          <router-link to="/register" class="btn btn-primary">
            Get Started
          </router-link>
          <router-link to="/login" class="btn btn-secondary">
            Sign In
          </router-link>
        </div>
      </div>
      <div class="hero-image">
        <div class="chat-preview">
          <div class="chat-window">
            <div class="chat-header">
              <div class="chat-user">
                <div class="avatar"></div>
                <span>Team Chat</span>
              </div>
            </div>
            <div class="chat-messages">
              <div class="message">
                <div class="message-avatar"></div>
                <div class="message-content">Hey everyone! 👋</div>
              </div>
              <div class="message own">
                <div class="message-content">Hello! How's the project going?</div>
              </div>
              <div class="message">
                <div class="message-avatar"></div>
                <div class="message-content">Great progress today! 🚀</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="container">
        <h2 class="section-title">Why Choose ChatApp?</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3 class="feature-title">Real-time Messaging</h3>
            <p class="feature-description">
              Instant message delivery with WebSocket technology for seamless communication.
            </p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3 class="feature-title">Secure & Private</h3>
            <p class="feature-description">
              End-to-end encryption ensures your conversations remain private and secure.
            </p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h3 class="feature-title">Cross-Platform</h3>
            <p class="feature-description">
              Access your chats from any device - desktop, mobile, or tablet.
            </p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">👥</div>
            <h3 class="feature-title">Group Chats</h3>
            <p class="feature-description">
              Create group conversations and collaborate with your team effectively.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta">
      <div class="container">
        <div class="cta-content">
          <h2 class="cta-title">Ready to Start Chatting?</h2>
          <p class="cta-description">
            Join thousands of users who trust ChatApp for their communication needs.
          </p>
          <router-link to="/register" class="btn btn-primary btn-large">
            Create Free Account
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Landing'
}
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
}

.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
  min-height: 80vh;
}

.hero-content {
  max-width: 500px;
}

.hero-title {
  font-size: 3rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero-description {
  font-size: 1.25rem;
  color: #6b7280;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-block;
  text-align: center;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background-color: #2563eb;
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: transparent;
  color: #3b82f6;
  border: 2px solid #3b82f6;
}

.btn-secondary:hover {
  background-color: #3b82f6;
  color: white;
}

.btn-large {
  padding: 1rem 2.5rem;
  font-size: 1.125rem;
}

.hero-image {
  display: flex;
  justify-content: center;
  align-items: center;
}

.chat-preview {
  perspective: 1000px;
}

.chat-window {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  width: 350px;
  overflow: hidden;
  transform: rotateY(-5deg) rotateX(5deg);
}

.chat-header {
  background: #3b82f6;
  color: white;
  padding: 1rem;
  display: flex;
  align-items: center;
}

.chat-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.avatar, .message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(45deg, #f59e0b, #ef4444);
}

.message-avatar {
  width: 24px;
  height: 24px;
}

.chat-messages {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.message {
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
}

.message.own {
  flex-direction: row-reverse;
}

.message.own .message-content {
  background: #3b82f6;
  color: white;
}

.message-content {
  background: #f3f4f6;
  padding: 0.5rem 0.75rem;
  border-radius: 1rem;
  max-width: 200px;
}

.features {
  background: #f9fafb;
  padding: 5rem 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  font-size: 2.5rem;
  font-weight: bold;
  text-align: center;
  color: #1f2937;
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-4px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.feature-description {
  color: #6b7280;
  line-height: 1.6;
}

.cta {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  padding: 5rem 2rem;
  text-align: center;
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.cta-description {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta .btn-primary {
  background: white;
  color: #3b82f6;
}

.cta .btn-primary:hover {
  background: #f3f4f6;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 2rem 1rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-actions {
    justify-content: center;
  }

  .chat-window {
    width: 300px;
    transform: none;
  }

  .section-title {
    font-size: 2rem;
  }

  .cta-title {
    font-size: 2rem;
  }
}
</style>
<template>
  <div class="about-page">
    <div class="container">
      <div class="about-header">
        <h1 class="page-title">About ChatApp</h1>
        <p class="page-subtitle">
          A modern real-time chat application built with cutting-edge technology
        </p>
      </div>

      <div class="about-content">
        <section class="about-section">
          <h2 class="section-title">About the Developer</h2>
          <div class="developer-info">
            <div class="developer-card">
              <div class="developer-icon">👨‍💼</div>
              <div class="developer-details">
                <h3>Industrial Engineer</h3>
                <p class="section-text">
                  This project was developed by an Industrial Engineer with a passion for technology
                  and software development. Combining analytical thinking from engineering background
                  with modern web development practices to create efficient and scalable solutions.
                </p>
                <p class="section-text">
                  The intersection of industrial engineering principles and software development
                  brings a unique perspective to building robust, user-centered applications.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section class="about-section">
          <h2 class="section-title">Technology Stack</h2>
          <div class="tech-stack">
            <div class="tech-category">
              <h3 class="tech-title">🎨 Frontend</h3>
              <div class="tech-items">
                <div class="tech-item">
                  <span class="tech-name">Vue.js 3</span>
                  <span class="tech-desc">Progressive JavaScript framework with Composition API</span>
                </div>
                <div class="tech-item">
                  <span class="tech-name">Vue Router</span>
                  <span class="tech-desc">Client-side routing with navigation guards</span>
                </div>
                <div class="tech-item">
                  <span class="tech-name">Vite</span>
                  <span class="tech-desc">Fast build tool and development server</span>
                </div>
              </div>
            </div>

            <div class="tech-category">
              <h3 class="tech-title">⚙️ Backend</h3>
              <div class="tech-items">
                <div class="tech-item">
                  <span class="tech-name">FastAPI</span>
                  <span class="tech-desc">Modern Python web framework for building APIs</span>
                </div>
                <div class="tech-item">
                  <span class="tech-name">SQLAlchemy</span>
                  <span class="tech-desc">Python SQL toolkit and Object-Relational Mapping</span>
                </div>
                <div class="tech-item">
                  <span class="tech-name">SQLite</span>
                  <span class="tech-desc">Lightweight database for development</span>
                </div>
                <div class="tech-item">
                  <span class="tech-name">WebSockets</span>
                  <span class="tech-desc">Real-time bidirectional communication</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section class="about-section">
          <h2 class="section-title">Project Features</h2>
          <div class="features-list">
            <div class="feature-item">
              <h3>🔐 Authentication System</h3>
              <p>User registration, login, and role-based access control</p>
            </div>
            <div class="feature-item">
              <h3>⚡ Real-Time Messaging</h3>
              <p>WebSocket-powered instant messaging with live updates</p>
            </div>
            <div class="feature-item">
              <h3>👥 User Management</h3>
              <p>Admin dashboard for user administration and moderation</p>
            </div>
            <div class="feature-item">
              <h3>📱 Responsive Design</h3>
              <p>Mobile-first design that works on all devices</p>
            </div>
            <div class="feature-item">
              <h3>🗄️ Database Integration</h3>
              <p>SQLAlchemy ORM with proper data modeling and relationships</p>
            </div>
            <div class="feature-item">
              <h3>🚀 Modern Architecture</h3>
              <p>Clean separation of concerns with MVC pattern</p>
            </div>
          </div>
        </section>

        <section class="about-section">
          <h2 class="section-title">Project Goals</h2>
          <p class="section-text">
            This chat application serves as a demonstration of modern web development practices,
            showcasing the integration of Vue.js frontend with FastAPI backend.
          </p>
          <div class="goals-list">
            <div class="goal-item">
              <h4>🎯 Learning Objective</h4>
              <p>Explore full-stack development with modern frameworks and tools</p>
            </div>
            <div class="goal-item">
              <h4>🔧 Technical Implementation</h4>
              <p>Implement real-time features, authentication, and database management</p>
            </div>
            <div class="goal-item">
              <h4>📈 Best Practices</h4>
              <p>Apply software engineering principles and clean code architecture</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.about-page {
  padding: 2rem 0;
  min-height: 60vh;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 2rem;
}

.about-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 1rem;
}

.page-subtitle {
  font-size: 1.25rem;
  color: #6b7280;
  line-height: 1.6;
}

.about-content {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.about-section {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.section-text {
  color: #4b5563;
  line-height: 1.7;
  margin-bottom: 1rem;
}

.section-text:last-child {
  margin-bottom: 0;
}

.features-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.feature-item {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 0.5rem;
  border-left: 4px solid #3b82f6;
}

.feature-item h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.feature-item p {
  color: #6b7280;
  line-height: 1.5;
}

/* Developer Info Styles */
.developer-info {
  margin-top: 1rem;
}

.developer-card {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  background: #f9fafb;
  padding: 2rem;
  border-radius: 1rem;
  border-left: 4px solid #3b82f6;
}

.developer-icon {
  font-size: 3rem;
  flex-shrink: 0;
}

.developer-details h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

/* Tech Stack Styles */
.tech-stack {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 1rem;
}

.tech-category {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 0.75rem;
}

.tech-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.tech-items {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.tech-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.tech-name {
  font-weight: 600;
  color: #3b82f6;
  font-size: 0.875rem;
}

.tech-desc {
  font-size: 0.75rem;
  color: #6b7280;
  line-height: 1.4;
}

/* Goals Styles */
.goals-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.goal-item {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 0.5rem;
  border-left: 4px solid #10b981;
}

.goal-item h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.goal-item p {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .about-page {
    padding: 1rem 0;
  }

  .container {
    padding: 0 1rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .about-section {
    padding: 1.5rem;
  }

  .features-list {
    grid-template-columns: 1fr;
  }

  .developer-card {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .tech-stack {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .goals-list {
    grid-template-columns: 1fr;
  }
}
</style>
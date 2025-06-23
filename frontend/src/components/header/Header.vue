<template>
  <header class="app-header">
    <nav class="navbar">
      <!-- Logo/Brand -->
      <div class="navbar-brand">
        <router-link to="/" class="brand-link">
          <span class="brand-text">ChatApp</span>
        </router-link>
      </div>

      <!-- Mobile Menu Toggle -->
      <button
        class="mobile-menu-toggle"
        @click="toggleMobileMenu"
        :class="{ active: isMobileMenuOpen }"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      <!-- Navigation Links -->
      <div class="navbar-nav" :class="{ active: isMobileMenuOpen }">
        <!-- Public Navigation -->
        <template v-if="!isAuthenticated">
          <router-link to="/" class="nav-link" @click="closeMobileMenu">
            Home
          </router-link>
          <router-link to="/about" class="nav-link" @click="closeMobileMenu">
            About
          </router-link>
          <router-link to="/login" class="nav-link" @click="closeMobileMenu">
            Login
          </router-link>
          <router-link to="/register" class="nav-link btn-primary" @click="closeMobileMenu">
            Register
          </router-link>
        </template>

        <!-- Authenticated Navigation -->
        <template v-else>
          <router-link to="/" class="nav-link" @click="closeMobileMenu">
            Home
          </router-link>
          <router-link to="/about" class="nav-link" @click="closeMobileMenu">
            About
          </router-link>

          <!-- Admin Link (only for admins) -->
          <router-link
            v-if="isAdmin"
            to="/admin"
            class="nav-link"
            @click="closeMobileMenu"
          >
            Admin
          </router-link>

          <!-- User Menu Dropdown -->
          <div class="user-menu" @click="toggleUserMenu">
            <div class="user-avatar">
              <img :src="currentUser?.avatar" :alt="currentUser?.display_name" v-if="currentUser?.avatar" />
              <span v-else class="avatar-placeholder">{{ userInitials }}</span>
            </div>
            <span class="user-name">{{ currentUser?.display_name || currentUser?.username || 'User' }}</span>
            <div class="dropdown-menu" v-if="isUserMenuOpen">
              <router-link to="/profile" class="dropdown-item" @click="closeUserMenu">
                Profile
              </router-link>
              <router-link to="/settings" class="dropdown-item" @click="closeUserMenu">
                Settings
              </router-link>
              <hr class="dropdown-divider" />
              <button class="dropdown-item logout-btn" @click="handleLogout">
                Logout
              </button>
            </div>
          </div>
        </template>
      </div>
    </nav>
  </header>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from '../../composables/useToast'
import { useAuth } from '../../composables/useAuth'

export default {
  name: 'Header',
  setup() {
    const router = useRouter()
    const { showSuccess, showInfo } = useToast()
    const { isAuthenticated, isAdmin, currentUser, logout: authLogout, getUserInitials } = useAuth()
    const isMobileMenuOpen = ref(false)
    const isUserMenuOpen = ref(false)

    const userInitials = computed(() => {
      return getUserInitials()
    })

    const toggleMobileMenu = () => {
      isMobileMenuOpen.value = !isMobileMenuOpen.value
    }

    const closeMobileMenu = () => {
      isMobileMenuOpen.value = false
    }

    const toggleUserMenu = () => {
      isUserMenuOpen.value = !isUserMenuOpen.value
    }

    const closeUserMenu = () => {
      isUserMenuOpen.value = false
    }

    const handleLogout = () => {
      // Use the auth composable logout
      authLogout()
      closeUserMenu()

      showInfo('You have been logged out successfully. See you next time!', 'Logged Out')
      router.push('/')
    }

    // Close menus when clicking outside
    const handleClickOutside = (event) => {
      if (!event.target.closest('.user-menu')) {
        isUserMenuOpen.value = false
      }
      if (!event.target.closest('.navbar-nav') && !event.target.closest('.mobile-menu-toggle')) {
        isMobileMenuOpen.value = false
      }
    }

    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    return {
      isMobileMenuOpen,
      isUserMenuOpen,
      isAuthenticated,
      isAdmin,
      currentUser,
      userInitials,
      toggleMobileMenu,
      closeMobileMenu,
      toggleUserMenu,
      closeUserMenu,
      handleLogout
    }
  }
}
</script>

<style scoped>
.app-header {
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.navbar-brand .brand-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #1f2937;
  font-weight: bold;
  font-size: 1.5rem;
}



.brand-text {
  color: #3b82f6;
}

.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.mobile-menu-toggle span {
  width: 25px;
  height: 3px;
  background: #374151;
  margin: 3px 0;
  transition: 0.3s;
}

.navbar-nav {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-link {
  text-decoration: none;
  color: #374151;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.nav-link:hover {
  color: #3b82f6;
  background-color: #f3f4f6;
}

.nav-link.router-link-active {
  color: #3b82f6;
  background-color: #eff6ff;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background-color: #2563eb;
  color: white;
}

.user-menu {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
}

.user-menu:hover {
  background-color: #f3f4f6;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
}

.user-name {
  font-weight: 500;
  color: #374151;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  min-width: 160px;
  z-index: 1000;
  margin-top: 0.5rem;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 0.75rem 1rem;
  text-decoration: none;
  color: #374151;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #f3f4f6;
}

.dropdown-divider {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 0.5rem 0;
}

.logout-btn {
  color: #dc2626;
}

.logout-btn:hover {
  background-color: #fef2f2;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .mobile-menu-toggle {
    display: flex;
  }

  .navbar-nav {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border-top: 1px solid #e5e7eb;
    flex-direction: column;
    padding: 1rem;
    gap: 0.5rem;
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
  }

  .navbar-nav.active {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }

  .nav-link {
    width: 100%;
    text-align: center;
  }

  .user-menu {
    justify-content: center;
  }
}
</style>
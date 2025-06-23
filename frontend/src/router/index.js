import { createRouter, createWebHistory } from 'vue-router'

// Import page components
import Landing from '../pages/landing/Landing.vue'
import About from '../pages/about/About.vue'
import Login from '../pages/authentication/Login.vue'
import Register from '../pages/authentication/Register.vue'
import Chat from '../pages/chat/Chat.vue'
import Admin from '../pages/admin/admin.vue'

// Import layout component
import DefaultLayout from '../layouts/DefaultLayout.vue'

// Import auth composable
import { useAuth } from '../composables/useAuth'

const routes = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      {
        path: '',
        name: 'Landing',
        component: Landing,
        meta: {
          title: 'Welcome to Chat App',
          requiresAuth: false
        }
      },
      {
        path: '/about',
        name: 'About',
        component: About,
        meta: {
          title: 'About Us',
          requiresAuth: false
        }
      },
      {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: {
          title: 'Login',
          requiresAuth: false,
          hideForAuth: true // Hide this route if user is already authenticated
        }
      },
      {
        path: '/register',
        name: 'Register',
        component: Register,
        meta: {
          title: 'Register',
          requiresAuth: false,
          hideForAuth: true // Hide this route if user is already authenticated
        }
      },
      {
        path: '/chat',
        name: 'Chat',
        component: Chat,
        meta: {
          title: 'Chat',
          requiresAuth: true
        }
      },
      {
        path: '/profile',
        name: 'Profile',
        component: () => import('../pages/Profile.vue'),
        meta: {
          title: 'Profile',
          requiresAuth: true
        }
      },
      {
        path: '/admin',
        name: 'Admin',
        component: Admin,
        meta: {
          title: 'Admin Dashboard',
          requiresAuth: true,
          requiresAdmin: true
        }
      }
    ]
  },
  // Catch-all route for 404 pages
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../pages/error/NotFound.vue'),
    meta: {
      title: 'Page Not Found'
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // Always scroll to top when changing routes
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach((to, from, next) => {
  // Set page title
  if (to.meta.title) {
    document.title = to.meta.title
  }

  // Get auth state from composable
  const { isAuthenticated, isAdmin, currentUser } = useAuth()

  // Debug logging for admin route
  if (to.path === '/admin') {
    console.log('Accessing admin route:')
    console.log('- isAuthenticated:', isAuthenticated.value)
    console.log('- isAdmin:', isAdmin.value)
    console.log('- currentUser:', currentUser.value)
    console.log('- userRole from localStorage:', localStorage.getItem('userRole'))
  }

  // Redirect authenticated users away from login/register pages
  if (to.meta.hideForAuth && isAuthenticated.value) {
    next({ name: 'Chat' })
    return
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next({ name: 'Login' })
    return
  }

  // Check if route requires admin privileges
  if (to.meta.requiresAdmin && !isAdmin.value) {
    console.log('Admin access denied - redirecting to chat')
    next({ name: 'Chat' }) // Redirect to chat if not admin
    return
  }

  next()
})

// Note: Auth checks are now handled by the useAuth composable
// The helper functions below are kept for reference but not used

export default router

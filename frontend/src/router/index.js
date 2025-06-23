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

  // Check authentication (you'll need to implement this based on your auth system)
  const isAuthenticated = checkAuthStatus() // You'll implement this function
  const isAdmin = checkAdminStatus() // You'll implement this function

  // Redirect authenticated users away from login/register pages
  if (to.meta.hideForAuth && isAuthenticated) {
    next({ name: 'Chat' })
    return
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' })
    return
  }

  // Check if route requires admin privileges
  if (to.meta.requiresAdmin && !isAdmin) {
    next({ name: 'Chat' }) // Redirect to chat if not admin
    return
  }

  next()
})

// Helper functions (implement these based on your auth system)
function checkAuthStatus() {
  // Check if user is authenticated
  // This could check localStorage, Pinia store, or make an API call
  const token = localStorage.getItem('authToken')
  return !!token
}

function checkAdminStatus() {
  // Check if user has admin privileges
  // This could check user role from localStorage, Pinia store, etc.
  const userRole = localStorage.getItem('userRole')
  return userRole === 'admin'
}

export default router

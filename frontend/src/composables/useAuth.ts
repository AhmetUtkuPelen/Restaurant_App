import { ref, computed } from 'vue'

// Global reactive state for authentication
const authToken = ref<string | null>(null)
const userInfo = ref<any>(null)
const isAuthenticated = ref(false)

export function useAuth() {
  // Initialize auth state from localStorage
  const initAuth = () => {
    const token = localStorage.getItem('authToken')
    const user = localStorage.getItem('userInfo')
    
    if (token) {
      authToken.value = token
      isAuthenticated.value = true
      
      if (user) {
        try {
          userInfo.value = JSON.parse(user)
        } catch (error) {
          console.error('Failed to parse user info:', error)
          // Create default user info from token or other stored data
          const username = localStorage.getItem('username') || 'user'
          const email = localStorage.getItem('userEmail') || `${username}@example.com`
          userInfo.value = {
            id: generateUserId(username),
            username: username,
            email: email,
            display_name: username,
            role: localStorage.getItem('userRole') || 'user'
          }
          // Save the generated user info
          localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
        }
      } else {
        // Create user info from available data
        const username = localStorage.getItem('username') || 'user'
        const email = localStorage.getItem('userEmail') || `${username}@example.com`
        userInfo.value = {
          id: generateUserId(username),
          username: username,
          email: email,
          display_name: username,
          role: localStorage.getItem('userRole') || 'user'
        }
        localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
      }
    } else {
      isAuthenticated.value = false
      userInfo.value = null
    }
  }

  // Generate consistent user ID based on username
  const generateUserId = (username: string): string => {
    // Create a simple hash-like ID from username
    let hash = 0
    for (let i = 0; i < username.length; i++) {
      const char = username.charCodeAt(i)
      hash = ((hash << 5) - hash) + char
      hash = hash & hash // Convert to 32-bit integer
    }
    return `user_${Math.abs(hash)}`
  }

  // Login function
  const login = (credentials: any, userData?: any) => {
    // Store auth token
    authToken.value = credentials.token || 'mock-token'
    localStorage.setItem('authToken', authToken.value)
    
    // Store user role
    const role = credentials.role || userData?.role || 'user'
    localStorage.setItem('userRole', role)
    
    // Create and store user info
    const username = credentials.username || userData?.username || credentials.email?.split('@')[0] || 'user'
    const email = credentials.email || userData?.email || `${username}@example.com`
    
    userInfo.value = {
      id: generateUserId(username),
      username: username,
      email: email,
      display_name: userData?.display_name || username,
      role: role,
      created_at: new Date().toISOString()
    }
    
    // Store individual fields for backward compatibility
    localStorage.setItem('username', username)
    localStorage.setItem('userEmail', email)
    localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
    
    isAuthenticated.value = true
    
    return userInfo.value
  }

  // Logout function
  const logout = () => {
    authToken.value = null
    userInfo.value = null
    isAuthenticated.value = false
    
    // Clear all auth-related localStorage items
    localStorage.removeItem('authToken')
    localStorage.removeItem('userRole')
    localStorage.removeItem('username')
    localStorage.removeItem('userEmail')
    localStorage.removeItem('userInfo')
  }

  // Update user info
  const updateUserInfo = (updates: Partial<any>) => {
    if (userInfo.value) {
      userInfo.value = { ...userInfo.value, ...updates }
      localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
    }
  }

  // Computed properties
  const currentUser = computed(() => userInfo.value)
  const currentUserId = computed(() => userInfo.value?.id || null)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')
  const username = computed(() => userInfo.value?.username || '')
  const displayName = computed(() => userInfo.value?.display_name || userInfo.value?.username || '')

  // Check if user is authenticated
  const checkAuth = () => {
    const token = localStorage.getItem('authToken')
    return !!token
  }

  // Get user initials for avatar
  const getUserInitials = (name?: string) => {
    const displayName = name || userInfo.value?.display_name || userInfo.value?.username || 'U'
    return displayName
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  }

  return {
    // State
    authToken: computed(() => authToken.value),
    userInfo: computed(() => userInfo.value),
    isAuthenticated: computed(() => isAuthenticated.value),
    currentUser,
    currentUserId,
    isAdmin,
    username,
    displayName,
    
    // Methods
    initAuth,
    login,
    logout,
    updateUserInfo,
    checkAuth,
    getUserInitials
  }
}

// Initialize auth state when the module is imported
const { initAuth } = useAuth()
initAuth()

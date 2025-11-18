# Route Utilities Documentation

This file contains route protection utilities for the React application that work with the authentication system.

## Available Route Components (4 Types)

### 1. OpenRoute
- **Purpose**: Accessible to everyone (authenticated and non-authenticated users)
- **Use Case**: Home page, about page, contact page, product listings, login, register
- **Behavior**: No restrictions, everyone can access
- **Example**:
```tsx
<Route path="/" element={<OpenRoute><Home /></OpenRoute>} />
<Route path="/login" element={<OpenRoute><Login /></OpenRoute>} />
```

### 2. AuthenticatedRoute
- **Purpose**: Only for authenticated users
- **Use Case**: Profile, user settings, cart, orders, reservations, checkout
- **Behavior**:
  - Shows loading spinner while checking auth status
  - Redirects non-authenticated users to `/login` with return URL
- **Example**:
```tsx
<Route path="/profile" element={<AuthenticatedRoute><Profile /></AuthenticatedRoute>} />
```

### 3. AdminRoute
- **Purpose**: Only for users with admin role
- **Use Case**: Admin panel, user management, system settings
- **Behavior**:
  - Shows loading spinner while checking auth status
  - Redirects non-authenticated users to `/login` with return URL
  - Shows access denied page for non-admin users
- **Example**:
```tsx
<Route path="/admin" element={<AdminRoute><AdminPanel /></AdminRoute>} />
```

### 4. Error Route (NotFound)
- **Purpose**: Handles nonexistent routes
- **Use Case**: 404 page for invalid URLs
- **Behavior**: Shows NotFound component
- **Example**:
```tsx
<Route path="*" element={<NotFound />} />
```

## Features

### Loading States
All protected routes show a loading spinner while checking authentication status to prevent flash of wrong content.

### Return URL Handling
Protected routes remember where the user was trying to go and redirect them there after successful login.

### Access Denied Pages
Admin routes show user-friendly access denied messages with a "Go Back" button.

### Role-Based Access
- **Anyone**: Can access OpenRoute
- **Authenticated Users**: Can access OpenRoute + AuthenticatedRoute
- **Admin Users**: Can access OpenRoute + AuthenticatedRoute + AdminRoute

## Backend Role Mapping
Based on your backend UserRole enum:
- `UserRole.USER` → `'user'` → Can access Open + Authenticated routes
- `UserRole.STAFF` → `'staff'` → Can access Open + Authenticated routes
- `UserRole.ADMIN` → `'admin'` → Can access Open + Authenticated + Admin routes

## Usage Tips

1. **Use OpenRoute for public content** - Home, products, login, register
2. **Use AuthenticatedRoute for user features** - Profile, cart, orders
3. **Use AdminRoute for admin features** - Admin panel, user management
4. **Always include Error route** - Handles invalid URLs with `path="*"`
5. **Loading states are automatic** - No need to handle them manually

## Complete App Structure
```tsx
<Routes>
  {/* Open Routes - Everyone can access */}
  <Route path="/" element={<OpenRoute><Home /></OpenRoute>} />
  <Route path="/login" element={<OpenRoute><Login /></OpenRoute>} />
  <Route path="/products" element={<OpenRoute><Products /></OpenRoute>} />
  
  {/* Authenticated Routes - Only logged-in users */}
  <Route path="/profile" element={<AuthenticatedRoute><Profile /></AuthenticatedRoute>} />
  <Route path="/cart" element={<AuthenticatedRoute><Cart /></AuthenticatedRoute>} />
  
  {/* Admin Routes - Only admin users */}
  <Route path="/admin" element={<AdminRoute><AdminPanel /></AdminRoute>} />
  
  {/* Error Route - Invalid URLs */}
  <Route path="*" element={<NotFound />} />
</Routes>
```

## Security Benefits

✅ **Automatic Authentication Checks** - Routes check auth status automatically  
✅ **Role-Based Access Control** - Admin routes verify admin role  
✅ **Return URL Preservation** - Users redirected to intended page after login  
✅ **Loading States** - Prevents flash of unauthorized content  
✅ **Access Denied Handling** - User-friendly error messages for unauthorized access  
✅ **404 Handling** - Graceful handling of invalid routes
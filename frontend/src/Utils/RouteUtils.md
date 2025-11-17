# Route Utilities Documentation

This file contains route protection utilities for the React application that work with the authentication system.

## Available Route Components

### 1. PublicRoute
- **Purpose**: Accessible to everyone (authenticated and non-authenticated users)
- **Use Case**: Home page, about page, contact page, product listings
- **Example**:
```tsx
<Route path="/" element={<PublicRoute><Home /></PublicRoute>} />
```

### 2. AuthRoute
- **Purpose**: Only for non-authenticated users (redirects authenticated users away)
- **Use Case**: Login page, register page, forgot password page
- **Behavior**: 
  - Shows loading spinner while checking auth status
  - Redirects authenticated users to `/dashboard`
- **Example**:
```tsx
<Route path="/login" element={<AuthRoute><Login /></AuthRoute>} />
```

### 3. ProtectedRoute
- **Purpose**: Only for authenticated users
- **Use Case**: Dashboard, profile, user settings, cart, orders
- **Behavior**:
  - Shows loading spinner while checking auth status
  - Redirects non-authenticated users to `/login` with return URL
- **Example**:
```tsx
<Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
```

### 4. AdminRoute
- **Purpose**: Only for users with admin role
- **Use Case**: Admin panel, user management, system settings
- **Behavior**:
  - Shows loading spinner while checking auth status
  - Redirects non-authenticated users to `/login` with return URL
  - Shows access denied page for non-admin users
- **Example**:
```tsx
<Route path="/admin/*" element={<AdminRoute><AdminPanel /></AdminRoute>} />
```

### 5. StaffRoute
- **Purpose**: For users with staff or admin role
- **Use Case**: Staff dashboard, order management, inventory
- **Behavior**:
  - Shows loading spinner while checking auth status
  - Redirects non-authenticated users to `/login` with return URL
  - Shows access denied page for regular users
- **Example**:
```tsx
<Route path="/staff/*" element={<StaffRoute><StaffPanel /></StaffRoute>} />
```

## Features

### Loading States
All protected routes show a loading spinner while checking authentication status to prevent flash of wrong content.

### Return URL Handling
Protected routes remember where the user was trying to go and redirect them there after successful login.

### Access Denied Pages
Admin and Staff routes show user-friendly access denied messages instead of just redirecting.

### Role-Based Access
- `user`: Can access ProtectedRoute
- `staff`: Can access ProtectedRoute and StaffRoute
- `admin`: Can access ProtectedRoute, StaffRoute, and AdminRoute

## Backend Role Mapping
Based on your backend UserRole enum:
- `UserRole.USER` → `'user'`
- `UserRole.STAFF` → `'staff'`
- `UserRole.ADMIN` → `'admin'`

## Usage Tips

1. **Wrap your entire routing structure** with these components
2. **Use AuthRoute for login/register** to prevent authenticated users from seeing auth pages
3. **Use ProtectedRoute for user-specific content** like dashboard, profile
4. **Use AdminRoute for admin-only features** like user management
5. **Use StaffRoute for staff features** like order management
6. **Always handle loading states** - the components do this automatically

## Example App Structure
```tsx
<Routes>
  {/* Public */}
  <Route path="/" element={<PublicRoute><Home /></PublicRoute>} />
  
  {/* Auth only */}
  <Route path="/login" element={<AuthRoute><Login /></AuthRoute>} />
  
  {/* User only */}
  <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
  
  {/* Staff + Admin */}
  <Route path="/staff/*" element={<StaffRoute><StaffPanel /></StaffRoute>} />
  
  {/* Admin only */}
  <Route path="/admin/*" element={<AdminRoute><AdminPanel /></AdminRoute>} />
</Routes>
```
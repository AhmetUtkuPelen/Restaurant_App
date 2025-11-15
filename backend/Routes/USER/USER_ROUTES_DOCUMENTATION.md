# User Routes Documentation

## Base URL
All user routes are prefixed with `/api/users`

---

## Authentication Routes

### 1. Register User
**POST** `/api/users/register`

Register a new user account.

**Rate Limit:** 5 requests per minute

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "image_url": "https://example.com/avatar.jpg",
  "phone": "+905551234567",
  "address": "123 Main St, City"
}
```

**Response:** `201 Created`
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

---

### 2. Login
**POST** `/api/users/login`

Authenticate user and receive tokens.

**Rate Limit:** 10 requests per minute

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "USER"
  }
}
```

---

### 3. Logout
**POST** `/api/users/logout`

Logout current user (client should delete tokens).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "message": "Logged out successfully. Please delete your tokens."
}
```

---

### 4. Refresh Token
**POST** `/api/users/refresh`

Get new access token using refresh token.

**Rate Limit:** 20 requests per minute

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## User Profile Routes

### 5. Get My Profile
**GET** `/api/users/me`

Get current user's profile information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "image_url": "https://example.com/avatar.jpg",
  "phone": "+905551234567",
  "address": "123 Main St, City",
  "role": "USER",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "favourite_products": [1, 2, 3],
  "orders": [1, 2],
  "comments": [1],
  "cart": {...},
  "reservations": [1],
  "payments": [1]
}
```

---

### 6. Update My Profile
**PUT** `/api/users/me`

Update current user's profile. All fields are optional.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "username": "john_updated",
  "email": "john.new@example.com",
  "password": "NewSecurePass123!",
  "image_url": "https://example.com/new-avatar.jpg",
  "phone": "+905559876543",
  "address": "456 New St, City"
}
```

**Response:** `200 OK`
```json
{
  "message": "Profile updated successfully",
  "user": {...}
}
```

---

### 7. Change Password
**POST** `/api/users/me/change-password`

Change current user's password.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "current_password": "OldPass123!",
  "new_password": "NewSecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "message": "Password changed successfully"
}
```

---

## Admin Routes - User Management

**Note:** All admin routes require `ADMIN` role.

### 8. Get All Users
**GET** `/api/users/admin/all?skip=0&limit=100`

Get all users with pagination.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100)

**Response:** `200 OK`
```json
{
  "total": 150,
  "skip": 0,
  "limit": 100,
  "users": [...]
}
```

---

### 9. Get User by ID
**GET** `/api/users/admin/{user_id}`

Get single user by ID with all relationships.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "john_doe",
  ...
}
```

---

### 10. Create User (Admin)
**POST** `/api/users/admin/create`

Create a new user with any role.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Request Body:**
```json
{
  "username": "new_user",
  "email": "newuser@example.com",
  "password": "SecurePass123!",
  "role": "STAFF",
  "is_active": true
}
```

**Response:** `201 Created`
```json
{
  "message": "User created successfully",
  "user": {...}
}
```

---

### 11. Update User (Admin)
**PUT** `/api/users/admin/{user_id}`

Update any user's information.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Request Body:**
```json
{
  "username": "updated_username",
  "email": "updated@example.com",
  "role": "STAFF",
  "is_active": false
}
```

**Response:** `200 OK`
```json
{
  "message": "User updated successfully",
  "user": {...}
}
```

---

### 12. Hard Delete User
**DELETE** `/api/users/admin/{user_id}/hard`

Permanently delete user and all related data.

**⚠️ WARNING:** This action cannot be undone!

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Response:** `200 OK`
```json
{
  "message": "User john_doe permanently deleted"
}
```

---

### 13. Deactivate User
**POST** `/api/users/admin/{user_id}/deactivate`

Deactivate user account (soft delete).

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Response:** `200 OK`
```json
{
  "message": "User deactivated successfully",
  "user": {...}
}
```

---

### 14. Activate User
**POST** `/api/users/admin/{user_id}/activate`

Activate user account.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Response:** `200 OK`
```json
{
  "message": "User activated successfully",
  "user": {...}
}
```

---

### 15. Change User Role
**POST** `/api/users/admin/{user_id}/role`

Change user's role.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Request Body:**
```json
{
  "new_role": "STAFF"
}
```

**Response:** `200 OK`
```json
{
  "message": "User role changed from USER to STAFF",
  "user": {...}
}
```

---

## Admin Routes - Query & Search

### 16. Get Users by Role
**GET** `/api/users/admin/role/{role}`

Get all users with specific role.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Path Parameters:**
- `role`: USER, STAFF, or ADMIN

**Response:** `200 OK`
```json
[
  {...},
  {...}
]
```

---

### 17. Get Users by Status
**GET** `/api/users/admin/status/{is_active}`

Get users by active/inactive status.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Path Parameters:**
- `is_active`: true or false

**Response:** `200 OK`
```json
[
  {...},
  {...}
]
```

---

### 18. Search Users
**GET** `/api/users/admin/search/{search}`

Search users by username, email, or phone.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Path Parameters:**
- `search`: Search term

**Response:** `200 OK`
```json
[
  {...},
  {...}
]
```

---

### 19. Get User Statistics
**GET** `/api/users/admin/statistics`

Get user statistics for dashboard.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Response:** `200 OK`
```json
{
  "total_users": 150,
  "active_users": 140,
  "inactive_users": 10,
  "users_by_role": {
    "admin": 2,
    "staff": 8,
    "user": 140
  },
  "new_registrations_last_30_days": 25
}
```

---

## Admin Routes - User Activity

**Note:** These routes require `STAFF` or `ADMIN` role.

### 20. Get User Activity
**GET** `/api/users/admin/{user_id}/activity`

Get user activity summary.

**Headers:**
```
Authorization: Bearer <staff_or_admin_token>
```

**Response:** `200 OK`
```json
{
  "user_id": 1,
  "username": "john_doe",
  "total_orders": 5,
  "total_comments": 3,
  "total_reservations": 2,
  "total_payments": 5,
  "account_created": "2024-01-01T00:00:00",
  "last_updated": "2024-01-15T10:30:00"
}
```

---

### 21. Get User Orders
**GET** `/api/users/admin/{user_id}/orders`

Get all orders for a specific user.

**Headers:**
```
Authorization: Bearer <staff_or_admin_token>
```

**Response:** `200 OK`
```json
[
  {...},
  {...}
]
```

---

### 22. Get User Comments
**GET** `/api/users/admin/{user_id}/comments`

Get all comments for a specific user.

**Headers:**
```
Authorization: Bearer <staff_or_admin_token>
```

**Response:** `200 OK`
```json
[
  {...},
  {...}
]
```

---

### 23. Get User Favourites
**GET** `/api/users/admin/{user_id}/favourites`

Get all favourite products for a specific user.

**Headers:**
```
Authorization: Bearer <staff_or_admin_token>
```

**Response:** `200 OK`
```json
[
  {...},
  {...}
]
```

---

### 24. Get User Cart
**GET** `/api/users/admin/{user_id}/cart`

Get cart for a specific user.

**Headers:**
```
Authorization: Bearer <staff_or_admin_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "cart_items": [...],
  "total_items": 5,
  "total_price": "125.50"
}
```

---

### 25. Get User Reservations
**GET** `/api/users/admin/{user_id}/reservations`

Get all reservations for a specific user.

**Headers:**
```
Authorization: Bearer <staff_or_admin_token>
```

**Response:** `200 OK`
```json
[
  {...},
  {...}
]
```

---

### 26. Get User Payments
**GET** `/api/users/admin/{user_id}/payments`

Get all payments for a specific user.

**Headers:**
```
Authorization: Bearer <staff_or_admin_token>
```

**Response:** `200 OK`
```json
[
  {...},
  {...}
]
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Username already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Admin access required"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Registration failed: <error_message>"
}
```

---

## Authentication Flow

1. **Register** → POST `/api/users/register`
2. **Login** → POST `/api/users/login` (receive access_token & refresh_token)
3. **Use access_token** in Authorization header for protected routes
4. **When access_token expires** → POST `/api/users/refresh` with refresh_token
5. **Logout** → POST `/api/users/logout` (delete tokens on client)

---

## Role-Based Access Control

- **USER**: Can access own profile and update own information
- **STAFF**: Can view user activity and related data
- **ADMIN**: Full access to all user management functions

---

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character (!@#$%^&*(),.?":{}|<>)

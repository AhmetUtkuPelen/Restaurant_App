# User Routes - Quick Start Guide

## 🚀 Getting Started

### 1. Start the Server

```bash
cd backend
python main.py
```

Server will start at: `http://localhost:8000`

---

## 📖 API Documentation

Once server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **SQLAdmin**: http://localhost:8000/admin

---

## 🔥 Quick Test Commands

### Register a New User

```bash
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

**Save the `access_token` from the response!**

### Get Your Profile

```bash
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### Update Your Profile

```bash
curl -X PUT http://localhost:8000/api/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+905551234567",
    "address": "123 Main St"
  }'
```

---

## 🔐 Authentication Headers

For all protected routes, include:

```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

---

## 📊 Available Endpoints

### Public (No Auth Required)

- `POST /api/users/register` - Register
- `POST /api/users/login` - Login
- `POST /api/users/refresh` - Refresh token

### User (Requires Auth)

- `GET /api/users/me` - Get profile
- `PUT /api/users/me` - Update profile
- `POST /api/users/me/change-password` - Change password
- `POST /api/users/logout` - Logout

### Admin Only

- `GET /api/users/admin/all` - List all users
- `GET /api/users/admin/{id}` - Get user details
- `POST /api/users/admin/create` - Create user
- `PUT /api/users/admin/{id}` - Update user
- `DELETE /api/users/admin/{id}/hard` - Delete user
- `POST /api/users/admin/{id}/activate` - Activate user
- `POST /api/users/admin/{id}/deactivate` - Deactivate user
- `POST /api/users/admin/{id}/role` - Change role
- `GET /api/users/admin/role/{role}` - Filter by role
- `GET /api/users/admin/status/{status}` - Filter by status
- `GET /api/users/admin/search/{term}` - Search users
- `GET /api/users/admin/statistics` - Get stats

### Staff/Admin

- `GET /api/users/admin/{id}/activity` - User activity
- `GET /api/users/admin/{id}/orders` - User orders
- `GET /api/users/admin/{id}/comments` - User comments
- `GET /api/users/admin/{id}/favourites` - User favourites
- `GET /api/users/admin/{id}/cart` - User cart
- `GET /api/users/admin/{id}/reservations` - User reservations
- `GET /api/users/admin/{id}/payments` - User payments

---

## 🎯 Common Use Cases

### 1. User Registration & Login Flow

```
1. POST /api/users/register
2. POST /api/users/login (get tokens)
3. Use access_token for authenticated requests
4. When token expires, POST /api/users/refresh
```

### 2. Update User Information

```
1. GET /api/users/me (check current info)
2. PUT /api/users/me (update fields)
```

### 3. Admin User Management

```
1. GET /api/users/admin/all (list users)
2. GET /api/users/admin/{id} (view details)
3. PUT /api/users/admin/{id} (update user)
4. POST /api/users/admin/{id}/role (change role)
```

---

## ⚠️ Important Notes

### Password Requirements

- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 digit
- At least 1 special character

### Rate Limits

- Register: 5 requests/minute
- Login: 10 requests/minute
- Refresh: 20 requests/minute

### User Roles

- `USER` - Regular user (default)
- `STAFF` - Staff member
- `ADMIN` - Administrator

---

## 🐛 Troubleshooting

### "Token has expired"

→ Use refresh token: `POST /api/users/refresh`

### "Admin access required"

→ Your user role is not ADMIN

### "Username already registered"

→ Choose a different username

### "Invalid token"

→ Login again to get new tokens

---

## 📚 Full Documentation

For complete API documentation with all request/response examples, see:

- `USER_ROUTES_DOCUMENTATION.md`
- `IMPLEMENTATION_SUMMARY.md`

---

## ✅ Status

All 26 user endpoints are fully implemented and ready to use!

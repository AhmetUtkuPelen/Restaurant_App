# Chat API Documentation

## Overview

The Chat API is a comprehensive real-time messaging system built with FastAPI. It provides secure user authentication, real-time messaging via WebSockets, file sharing, and administrative controls.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.chatapp.com`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. All protected endpoints require a valid JWT token in the Authorization header.

### Getting a Token

1. **Register a new account**:
   ```bash
   curl -X POST "http://localhost:8000/users/register" \
        -H "Content-Type: application/json" \
        -d '{
          "username": "johndoe",
          "email": "john@example.com",
          "password": "securepassword123",
          "display_name": "John Doe"
        }'
   ```

2. **Login with existing credentials**:
   ```bash
   curl -X POST "http://localhost:8000/users/login" \
        -H "Content-Type: application/json" \
        -d '{
          "username_or_email": "johndoe",
          "password": "securepassword123"
        }'
   ```

### Using the Token

Include the JWT token in the Authorization header for all protected endpoints:

```bash
curl -X GET "http://localhost:8000/users/me" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## API Endpoints

### User Management

#### Register User
- **POST** `/users/register`
- **Description**: Create a new user account
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "display_name": "John Doe"
  }
  ```

#### Login User
- **POST** `/users/login`
- **Description**: Authenticate user and get JWT token
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username_or_email": "johndoe",
    "password": "securepassword123"
  }
  ```

#### Get Current User
- **GET** `/users/me`
- **Description**: Get authenticated user's profile
- **Authentication**: Required

#### Update User Profile
- **PUT** `/users/me`
- **Description**: Update authenticated user's profile
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "display_name": "John Smith",
    "bio": "Software developer",
    "avatar_url": "https://example.com/avatar.jpg"
  }
  ```

### Messaging

#### Get Messages
- **GET** `/messages/`
- **Description**: Get messages from chat rooms or conversations
- **Authentication**: Required
- **Query Parameters**:
  - `chat_id` (optional): Get messages from specific chat room
  - `recipient_id` (optional): Get conversation with specific user
  - `limit` (optional): Number of messages to return (default: 50, max: 100)
  - `skip` (optional): Number of messages to skip for pagination (default: 0)

#### Send Message
- **POST** `/messages/`
- **Description**: Send a new message
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "chat_id": "room_123",
    "content": "Hello everyone!",
    "message_type": "text"
  }
  ```

#### Update Message
- **PUT** `/messages/{message_id}`
- **Description**: Edit a message (only sender can edit)
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "content": "Updated message content",
    "is_edited": true
  }
  ```

#### Delete Message
- **DELETE** `/messages/{message_id}`
- **Description**: Delete a message (only sender can delete)
- **Authentication**: Required

### File Upload

#### Upload File
- **POST** `/files/upload`
- **Description**: Upload a file for sharing
- **Authentication**: Required
- **Content-Type**: `multipart/form-data`
- **Form Data**:
  - `file`: The file to upload
  - `description` (optional): File description

### Admin Operations

#### Get Dashboard Stats
- **GET** `/admin/dashboard/stats`
- **Description**: Get system statistics for admin dashboard
- **Authentication**: Required (Admin role)

#### Get All Users (Admin)
- **GET** `/admin/users`
- **Description**: Get all users with admin details
- **Authentication**: Required (Admin role)
- **Query Parameters**:
  - `skip` (optional): Pagination offset
  - `limit` (optional): Number of users to return
  - `search` (optional): Search by username or email
  - `status_filter` (optional): Filter by user status
  - `role_filter` (optional): Filter by user role

#### Ban User
- **POST** `/admin/users/{user_id}/ban`
- **Description**: Ban a user account
- **Authentication**: Required (Admin role)

#### Unban User
- **POST** `/admin/users/{user_id}/unban`
- **Description**: Unban a user account
- **Authentication**: Required (Admin role)

## WebSocket Connection

The API provides real-time messaging through WebSocket connections.

### Connection URL
```
ws://localhost:8000/ws/{user_id}
```

### Authentication
WebSocket connections require authentication. Include the JWT token in the connection headers or query parameters.

### Message Format

#### Sending Messages (Client → Server)
```json
{
  "message": "Hello, world!",
  "timestamp": "2024-01-01T12:00:00Z",
  "attachments": []
}
```

#### Receiving Messages (Server → Client)
```json
{
  "id": "msg_1234567890",
  "sender_id": "user123",
  "content": "Hello, world!",
  "created_at": "2024-01-01T12:00:00Z",
  "status": "delivered",
  "attachments": [],
  "is_edited": false
}
```

### Connection Events

#### User Online Status
```json
{
  "type": "user_status",
  "user_id": "user123",
  "status": "online",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### Message Delivery Confirmation
```json
{
  "type": "message_status",
  "message_id": "msg_123",
  "status": "delivered",
  "timestamp": "2024-01-01T12:00:01Z"
}
```

## Error Handling

The API uses consistent error response format:

```json
{
  "error": true,
  "message": "Error description",
  "code": "ERROR_CODE",
  "details": {},
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "req_123"
}
```

### Common Error Codes

- `VALIDATION_ERROR`: Invalid input data
- `AUTHENTICATION_ERROR`: Invalid or missing authentication
- `AUTHORIZATION_ERROR`: Insufficient permissions
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `RESOURCE_NOT_FOUND`: Requested resource not found
- `INTERNAL_ERROR`: Server error

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Default**: 100 requests per hour per user
- **Login attempts**: 5 attempts per 15 minutes
- **File uploads**: 10 uploads per hour
- **WebSocket messages**: 60 messages per minute

Rate limit headers are included in responses:
- `X-RateLimit-Limit`: Request limit
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Reset timestamp

## Security Features

### Password Security
- Minimum 8 characters
- Bcrypt hashing with salt
- Password strength validation

### Input Validation
- HTML sanitization to prevent XSS
- SQL injection prevention
- File type and size validation
- Request size limits

### Authentication Security
- JWT tokens with expiration
- Refresh token rotation
- Account lockout after failed attempts
- Session management

## SDK and Client Libraries

### JavaScript/TypeScript
```javascript
// Install the client library
npm install @chatapi/client

// Initialize the client
import { ChatClient } from '@chatapi/client';

const client = new ChatClient({
  baseUrl: 'http://localhost:8000',
  token: 'your-jwt-token'
});

// Send a message
await client.messages.send({
  chat_id: 'room_123',
  content: 'Hello everyone!'
});

// Connect to WebSocket
const ws = client.websocket.connect('user_123');
ws.on('message', (message) => {
  console.log('New message:', message);
});
```

### Python
```python
# Install the client library
pip install chatapi-client

# Initialize the client
from chatapi_client import ChatClient

client = ChatClient(
    base_url='http://localhost:8000',
    token='your-jwt-token'
)

# Send a message
response = client.messages.send(
    chat_id='room_123',
    content='Hello everyone!'
)

# Connect to WebSocket
ws = client.websocket.connect('user_123')
ws.on_message(lambda msg: print(f'New message: {msg}'))
```

## Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run specific test categories
pytest tests/test_auth.py
pytest tests/test_messages.py
pytest tests/test_websocket.py
```

### Test Coverage
The API maintains high test coverage:
- Unit tests: 85%+ coverage
- Integration tests: 70%+ coverage
- Security tests: 100% coverage for auth flows

## Deployment

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/chatdb

# Security
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760
ALLOWED_FILE_TYPES=.jpg,.png,.pdf,.txt

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://chatapp.com
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Health Checks
- **GET** `/` - Basic health check
- **GET** `/test-db` - Database connectivity check
- **GET** `/admin/system/health` - Comprehensive system health

## Support

For API support and questions:
- **Documentation**: `/docs` (Swagger UI)
- **Email**: support@chatapi.com
- **GitHub**: https://github.com/chatapi/api
- **Discord**: https://discord.gg/chatapi
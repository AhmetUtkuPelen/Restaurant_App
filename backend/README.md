# Real-time Chat Application API

A FastAPI-based real-time chat application with WebSocket support, user management, and message handling.

## Features

- **User Management**: Registration, login, profile updates, user search
- **Real-time Messaging**: WebSocket-based real-time chat
- **Message Features**: Text messages, reactions, replies, message editing/deletion
- **User Status**: Online/offline status tracking
- **Message History**: Conversation history and chat room messages

## Project Structure

```
backend/
├── Controllers/
│   ├── User/
│   │   └── UserController.py      # User business logic
│   └── Message/
│       └── MessageController.py   # Message business logic
├── Models/
│   ├── User/
│   │   └── UserModel.py          # User data models
│   └── Message/
│       └── MessageModel.py       # Message data models
├── Schemas/
│   ├── User/
│   │   └── UserSchemas.py        # User API schemas
│   └── Message/
│       └── MessageSchemas.py     # Message API schemas
├── Routes/
│   ├── User/
│   │   └── UserRoutes.py         # User API endpoints
│   └── Message/
│       └── MessageRoutes.py      # Message API endpoints
├── Services/
│   └── FileUpload.py             # File upload service
├── main.py                       # FastAPI application entry point
├── requirements.txt              # Python dependencies
└── test_api.py                   # API testing script
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## API Endpoints

### User Endpoints
- `POST /users/register` - Register a new user
- `POST /users/login` - User login
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update current user profile
- `GET /users/{user_id}` - Get user by ID
- `GET /users/` - Get all users (public info)
- `GET /users/search/` - Search users
- `PATCH /users/me/status` - Update user status
- `DELETE /users/me` - Delete user account

### Message Endpoints
- `POST /messages/` - Create a new message
- `GET /messages/{message_id}` - Get message by ID
- `PUT /messages/{message_id}` - Update message
- `DELETE /messages/{message_id}` - Delete message
- `GET /messages/conversation/{user_id}` - Get conversation with user
- `GET /messages/chat/{chat_id}` - Get chat room messages
- `POST /messages/{message_id}/reactions` - Add reaction to message
- `DELETE /messages/{message_id}/reactions` - Remove reaction
- `PATCH /messages/{message_id}/read` - Mark message as read

### WebSocket Endpoint
- `WS /ws/{user_id}` - WebSocket connection for real-time chat

## Testing

Run the test script to verify the API:
```bash
python test_api.py
```

## WebSocket Usage

Connect to the WebSocket endpoint to receive real-time messages:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/your_user_id');

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    console.log('Received:', message);
};

// Send a message
ws.send(JSON.stringify({
    message: "Hello, World!",
    timestamp: new Date().toISOString()
}));
```

## Example Usage

### Register a User
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

### Send a Message
```bash
curl -X POST "http://localhost:8000/messages/" \
     -H "Content-Type: application/json" \
     -d '{
       "recipient_id": "recipient_user_id",
       "content": "Hello there!",
       "message_type": "text"
     }'
```

## Next Steps

To make this production-ready, consider adding:

1. **Database Integration**: Replace in-memory storage with PostgreSQL/MongoDB
2. **Authentication**: Implement JWT tokens for secure authentication
3. **File Upload**: Complete file attachment functionality
4. **Rate Limiting**: Add rate limiting for API endpoints
5. **Logging**: Add comprehensive logging
6. **Testing**: Add unit and integration tests
7. **Docker**: Containerize the application
8. **Environment Configuration**: Add environment-based configuration

## Notes

- This implementation uses in-memory storage for simplicity
- Authentication is simplified (no JWT tokens yet)
- File upload functionality is not fully implemented
- This is a development setup - add proper security for production use

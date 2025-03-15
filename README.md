# google-drive-api-websocket-chat
# Google Drive & WebSocket API System

## Overview
This project provides an API system integrating Google Authentication, Google Drive file management, and real-time WebSocket-based chat. It allows users to authenticate with Google, upload/download files to Google Drive, and communicate in real-time via WebSockets.

## Features
- **Google Authentication**: Secure OAuth2-based authentication with Google.
- **Google Drive Integration**:
  - Upload files
  - List files
  - Download files
- **WebSocket Chat**: Real-time chat system for two pre-configured users.

## Project Structure
```
backend/
│── core/
│   ├── views.py 
│   ├── consumers.py  
│── backend/
│   ├── settings.py  
│── urls.py  
│── requirements.txt  
│── manage.py  
│── README.md
```

## API Endpoints
### 1. Google Authentication
- **Initiate Auth Flow**: `GET /auth/`
- **OAuth Callback**: `GET /auth/callback/`

### 2. Google Drive API
- **Upload File**: `POST /drive/upload/`
- **List Files**: `GET /drive/list/`
- **Download File**: `GET /drive/download/<file_id>/`

### 3. WebSocket Chat
- **WebSocket Connection**: `ws://localhost:8000/ws/chat/`

## How to Test the API
### 1. Clone Repository
```bash
git clone https://github.com/your-repo.git
cd backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Django Server
```bash
python manage.py runserver
```

### 4. Testing Google Authentication & Drive API
- Open `http://localhost:8000/auth/` in a browser and complete authentication.
- Use **Postman** or any API client to test endpoints.

### 5. Testing WebSocket Chat
- Open **two browser tabs**.
- Use the browser console:
```javascript
let socket = new WebSocket("ws://localhost:8000/ws/chat/");
socket.onmessage = (event) => console.log("Message received:", event.data);
socket.onopen = () => socket.send(JSON.stringify({"username": "userA", "message": "Hello!"}));
```

## Notes
- Ensure Google API credentials are configured in `settings.py`.
- WebSockets should be tested in a **supported environment**.




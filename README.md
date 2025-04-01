```markdown
# Audio File Management Service (Test-Task Pavepo)
 
*A test task for Pavepo with Yandex authentication and audio file uploads*

## 📌 Overview

This service provides:
- 🔐 OAuth2 authentication via Yandex
- 🎵 Audio file upload and management
- 📁 User-specific file storage
- 📄 API documentation with Swagger UI

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation
1. Copy the example environment file:
   cp .env.example .env
   
2. Edit `.env` with your credentials (Yandex OAuth details, database config, etc.)

3. Build and run the containers:
   sudo docker compose up --build
   If you use another port - change port in YANDEX_REDIRECT_URI!

4. Edit with your credentials (client_id) this url and open:

https://oauth.yandex.ru/authorize?response_type=code&client_id=YOUR_ID&redirect_uri=http://127.0.0.1:8000/api/v1/users/yandex-auth

#### After authorization, you will be redirected to the specified redirect_uri and using access_token you can log in to the system (/docs swagger ui)

### Accessing the API
After startup, the API will be available at:
- **API Docs**: http://localhost:8000/docs
- **Base URL**: http://localhost:8000/api/v1

## 🔧 Configuration

### Environment Variables
| Variable               | Description                | Example              |
|------------------------|----------------------------|----------------------|
| `POSTGRES_HOST`        | Postgres HOST              | db                   |
| `POSTGRES_USER`        | Postgres User              | postgres             |
| `POSTGRES_PASSWORD`    | Postgres Password          | postgres             |
| `POSTGRES_NAME`        | Postgres Name              | pavepo               |
| `POSTGRES_PORT`        | Postgres Port              | 5432                 |
| `YANDEX_CLIENT_ID`     | Yandex OAuth Client ID     | abc123...            |
| `YANDEX_CLIENT_SECRET` | Yandex OAuth Client Secret | xyz456...            |
| `SECRET_KEY`           | Application secret key     | your-secret-key-here |
| `ALGORITHM`            | JWT algorithm              | HS256                |

## 📚 API Endpoints

### Authentication
- `POST /users/yandex-auth` - authorization via yandex (callback)
- `POST /users/update_token` - Reset access_token
- `GET|PUT /users/me` - get info about current user or edit info about him
- `DELETE /users/{id}` - delete user (permission only for admin)

### Audio Files
- `POST /audio/list_of_user/` - Upload new audio file
- `GET /audio/upload/` - List user's audio files
---
```

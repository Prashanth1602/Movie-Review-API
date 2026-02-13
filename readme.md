# Movie Review API

A robust FastAPI application for managing movies and reviews, featuring secure authentication and vector-based search.

## Features
*   **Authentication**: Secure User Registration & Login (JWT Access + Refresh Tokens).
*   **Role-Based Access**: Admin role for managing movies.
*   **Movies**: Create, Read, Update, Delete (CRUD) with vector search support.
*   **Reviews**: Users can rate and review movies.
*   **Search**: Full-text and vector similarity search for movies.
*   **External API**: Secure programmatic access via API Key with Rate Limiting (Token Bucket).
*   **Optimized Database**: Automatic cleanup of expired tokens and efficient indexing.

## Tech Stack
*   **Framework**: FastAPI
*   **Database**: PostgreSQL (SQLAlchemy ORM)
*   **Security**: OAuth2 with Password (Bearer), Passlib (Bcrypt)
*   **Validation**: Pydantic

## Setup

### 1. Prerequisites
*   Python 3.10+
*   PostgreSQL running locally

### 2. Installation
```bash
# Clone the repository
git clone <repository-url>
cd Movie-Review-API

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=admin123
EXTERNAL_API_KEY=your_secure_random_string_here
```

### 4. Database Setup
The application automatically creates tables on startup.
```bash
# Start the server to initialize DB
uvicorn app.main:app --reload
```

## Usage

### Run the Server
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### External Access
To access movies programmatically without user login, use the External API:
```bash
curl -H "X-API-Key: your_secure_random_string_here" http://127.0.0.1:8000/api/external/movies
```
*   **Rate Limit**: 5 requests/second (Burst: 10).
*   **Endpoints**: `/api/external/movies`, `/api/external/search`

### Documentation
Explore the interactive API docs at:
*   **Swagger UI**: `http://127.0.0.1:8000/docs`
*   **ReDoc**: `http://127.0.0.1:8000/redoc`

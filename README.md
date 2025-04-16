# Messenger MIREA

A modern messaging application built with a microservices architecture.

## Project Structure

```
.
├── frontend/           # Frontend application
├── backend_src/       # Backend application
├── uploads/           # File uploads directory
├── certs/            # SSL certificates
└── docker-compose.yaml # Docker compose configuration
```

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- Node.js and npm (for local frontend development)

## Environment Setup

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Configure the following environment variables in `.env`:
- `DATABASE_USERNAME`: PostgreSQL username
- `DATABASE_PASSWORD`: PostgreSQL password
- `DATABASE_NAME`: Database name
- `REDIS_PORT`: Redis port (default: 6379)

## Running the Application

### Using Docker (Recommended)

1. Build and start all services:
```bash
docker-compose up --build
```

2. The application will be available at:
- Frontend: http://localhost
- Backend API: http://localhost:8000

## Services

- **Frontend**: React-based web application
- **Backend**: FastAPI-based REST API
- **PostgreSQL**: Main database
- **Redis**: Cache and session management

## API Documentation

Once the backend is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs


# Docker Setup Guide

This guide explains how to run the User Management System using Docker.

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually included with Docker Desktop)

## Quick Start

### 1. Development Mode (Recommended for first-time setup)

```bash
# Build and start the container
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

The application will be available at:
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Admin Login:** http://localhost:8000/admin/login

### 2. Production Mode

```bash
# Create .env file from example
cp .env.example .env

# Edit .env and set your production secrets
# Then run:
docker-compose -f docker-compose.prod.yml up -d --build
```

## Project Structure

```
User management/
├── Dockerfile                 # Docker image definition
├── docker-compose.yml        # Development configuration
├── docker-compose.prod.yml   # Production configuration
├── .dockerignore            # Files excluded from Docker build
├── .env.example             # Environment variables template
└── data/                    # Database files (created automatically)
    └── user_management.db
```

## Configuration

### Environment Variables

Create a `.env` file (or use `.env.example` as template):

```env
DATABASE_URL=sqlite:///./data/user_management.db
SECRET_KEY=your-secret-key-here
REFRESH_SECRET_KEY=your-refresh-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Important:** Generate secure keys for production:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Volumes

**Development (`docker-compose.yml`):**
- `./uploads` → `/app/uploads` (user uploaded images)
- `./data` → `/app/data` (database files)

**Production (`docker-compose.prod.yml`):**
- Named volumes for better Docker management
- Data persists even if containers are removed

## Common Commands

### Start Services
```bash
docker-compose up              # Start with logs
docker-compose up -d           # Start in background
docker-compose up --build      # Rebuild and start
```

### Stop Services
```bash
docker-compose down            # Stop and remove containers
docker-compose down -v        # Stop and remove volumes (WARNING: deletes data)
```

### View Logs
```bash
docker-compose logs           # All logs
docker-compose logs -f        # Follow logs (live)
docker-compose logs fastapi-app  # Specific service
```

### Execute Commands in Container
```bash
# Access container shell
docker-compose exec fastapi-app bash

# Run Python commands
docker-compose exec fastapi-app python create_admin.py
```

### Rebuild After Code Changes
```bash
docker-compose up --build
```

## Development Workflow

### Option 1: Mount Code for Hot Reload (Recommended for active development)

Edit `docker-compose.yml` and uncomment these lines:
```yaml
volumes:
  - ./app:/app/app
  - ./templates:/app/templates
  - ./static:/app/static
```

Then restart:
```bash
docker-compose restart
```

### Option 2: Rebuild After Changes
```bash
docker-compose up --build
```

## Database Management

### Create Admin User

```bash
# Execute the create_admin script inside container
docker-compose exec fastapi-app python create_admin.py
```

### Access Database (SQLite)

```bash
# Copy database from container
docker-compose cp fastapi-app:/app/data/user_management.db ./data/

# Or access via shell
docker-compose exec fastapi-app bash
sqlite3 /app/data/user_management.db
```

### Backup Database

```bash
# Copy database file
docker-compose cp fastapi-app:/app/data/user_management.db ./backup_$(date +%Y%m%d).db
```

### Reset Database

```bash
# Stop containers
docker-compose down

# Delete database file
rm ./data/user_management.db

# Start fresh
docker-compose up -d
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs fastapi-app

# Check if port is already in use
netstat -an | grep 8000  # Windows
lsof -i :8000            # Linux/Mac
```

### Database locked error
```bash
# Stop all containers
docker-compose down

# Wait a few seconds, then restart
docker-compose up -d
```

### Permission issues (Linux/Mac)
```bash
# Fix uploads directory permissions
sudo chown -R $USER:$USER ./uploads
sudo chown -R $USER:$USER ./data
```

### Rebuild from scratch
```bash
# Remove everything
docker-compose down -v
docker system prune -a

# Rebuild
docker-compose up --build
```

### View container status
```bash
docker-compose ps
docker ps
```

## Health Check

The container includes a health check endpoint:
```bash
curl http://localhost:8000/health
```

Check health status:
```bash
docker-compose ps
# Look for "healthy" status
```

## Security Notes

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Change default secrets** - Generate new keys for production
3. **Use production compose file** - `docker-compose.prod.yml` for production
4. **Review CORS settings** - Update in `app/main.py` for production

## Production Deployment

1. **Set environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

2. **Use production compose:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

3. **Set up reverse proxy** (Nginx/Traefik) for HTTPS

4. **Configure firewall** - Only expose necessary ports

5. **Set up backups** - Regular database backups

6. **Monitor logs:**
   ```bash
   docker-compose -f docker-compose.prod.yml logs -f
   ```

## Switching to PostgreSQL

If you want to use PostgreSQL instead of SQLite:

1. **Update `docker-compose.yml`:**
   ```yaml
   services:
     db:
       image: postgres:15-alpine
       environment:
         POSTGRES_USER: fastapi_user
         POSTGRES_PASSWORD: secure_password
         POSTGRES_DB: user_management
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
     fastapi-app:
       environment:
         DATABASE_URL: postgresql://fastapi_user:secure_password@db:5432/user_management
       depends_on:
         - db
   ```

2. **Install PostgreSQL driver:**
   ```bash
   # Add to requirements.txt:
   psycopg2-binary
   ```

3. **Rebuild:**
   ```bash
   docker-compose up --build
   ```

## Next Steps

- [ ] Create admin user: `docker-compose exec fastapi-app python create_admin.py`
- [ ] Access admin panel: http://localhost:8000/admin/login
- [ ] Test API: http://localhost:8000/docs
- [ ] Review and update `.env` with secure keys
- [ ] Set up backups for production

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)


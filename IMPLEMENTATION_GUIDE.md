# ThriveMentor - Step-by-Step Implementation Guide

This document provides a detailed, step-by-step guide to implement and run the ThriveMentor project.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Database Setup](#database-setup)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Running the Application](#running-the-application)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

- **Python 3.11+** installed
- **PostgreSQL 15+** installed and running
- **Flutter SDK 3.0+** installed
- **Docker & Docker Compose** (optional, for containerized setup)
- **Git** installed
- **Text Editor/IDE** (VS Code, PyCharm, etc.)

### Verify Installations

```bash
# Check Python version
python3 --version  # Should be 3.11 or higher

# Check PostgreSQL
psql --version

# Check Flutter
flutter --version

# Check Docker (optional)
docker --version
docker-compose --version
```

---

## Project Setup

### Step 1: Navigate to Project Directory

```bash
cd /home/sagark24/ThriveMentor
```

### Step 2: Verify Project Structure

```bash
tree -L 3 -I '__pycache__|*.pyc|venv|.git'
```

You should see:
```
ThriveMentor/
├── backend/
│   ├── auth_service/
│   ├── career_service/
│   ├── finance_service/
│   ├── health_service/
│   ├── shared/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   └── flutter_app/
├── docker-compose.yml
└── README.md
```

---

## Database Setup

### Option A: Using Docker (Recommended for Quick Start)

```bash
# Start PostgreSQL container
docker-compose up -d postgres

# Check if database is running
docker-compose ps

# View logs
docker-compose logs postgres
```

Wait until you see: `database system is ready to accept connections`

### Option B: Local PostgreSQL Installation

#### 1. Install PostgreSQL (if not installed)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
```

**Windows:**
Download from https://www.postgresql.org/download/windows/

#### 2. Start PostgreSQL Service

**Linux:**
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew services start postgresql
```

**Windows:**
Start PostgreSQL service from Services panel

#### 3. Create Database and User

```bash
# Switch to postgres user (Linux/macOS)
sudo -u postgres psql

# Or on Windows, open psql from PostgreSQL installation
```

In PostgreSQL shell:
```sql
-- Create database
CREATE DATABASE thrivementor;

-- Create user
CREATE USER thrivementor WITH PASSWORD 'password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE thrivementor TO thrivementor;

-- Exit
\q
```

#### 4. Verify Database Connection

```bash
psql -U thrivementor -d thrivementor -h localhost
# Enter password when prompted: password
```

---

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd /home/sagark24/ThriveMentor/backend
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

This will install:
- FastAPI
- SQLAlchemy
- PostgreSQL driver
- JWT libraries
- ML libraries (scikit-learn, pandas, numpy)
- And more...

### Step 4: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file
nano .env  # or use your preferred editor
```

Update the `.env` file:
```env
DATABASE_URL=postgresql://thrivementor:password@localhost:5432/thrivementor
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
```

**Important:** Generate a strong secret key:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 5: Initialize Database

```bash
# Run database initialization script
python init_db.py
```

You should see:
```
Creating database tables...
Database tables created successfully!
```

### Step 6: Verify Database Tables

```bash
psql -U thrivementor -d thrivementor -h localhost -c "\dt"
```

You should see tables:
- users
- career_goals
- health_records
- financial_transactions
- ml_recommendations

---

## Frontend Setup

### Step 1: Navigate to Flutter App Directory

```bash
cd /home/sagark24/ThriveMentor/frontend/flutter_app
```

### Step 2: Check Flutter Installation

```bash
flutter doctor
```

Fix any issues reported by `flutter doctor`.

### Step 3: Get Flutter Dependencies

```bash
flutter pub get
```

### Step 4: Create Assets Directory

```bash
mkdir -p assets/images assets/icons
```

### Step 5: Configure API Base URL

You need to update the API base URL in the Flutter app based on your platform:

**For Android Emulator:**
- Use `http://10.0.2.2:8000` (special IP for Android emulator)

**For iOS Simulator:**
- Use `http://localhost:8000`

**For Physical Device:**
- Find your computer's IP address:
  ```bash
  # Linux/macOS
  ifconfig | grep "inet " | grep -v 127.0.0.1
  
  # Windows
  ipconfig
  ```
- Use `http://YOUR_IP_ADDRESS:8000`

**For Web:**
- Use `http://localhost:8000`

Edit these files:
- `lib/services/auth_service.dart`
- `lib/services/api_service.dart`

Change:
```dart
static const String baseUrl = 'http://localhost:8000';
```

To your appropriate URL.

---

## Running the Application

### Step 1: Start Backend Server

```bash
# Make sure you're in backend directory with venv activated
cd /home/sagark24/ThriveMentor/backend
source venv/bin/activate  # if not already activated

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 2: Verify Backend is Running

Open your browser and visit:
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Root Endpoint:** http://localhost:8000/

### Step 3: Start Flutter App

**In a new terminal:**

```bash
cd /home/sagark24/ThriveMentor/frontend/flutter_app

# List available devices
flutter devices

# Run on connected device/emulator
flutter run

# Or specify device
flutter run -d <device-id>
```

### Step 4: Test the Application

1. **Register a New User:**
   - Open the app
   - Click "Register"
   - Fill in:
     - Email: test@example.com
     - Username: testuser
     - Password: testpass123
   - Click "Register"

2. **Login:**
   - Use your credentials to login
   - You should see the dashboard

3. **Add Career Goal:**
   - Go to Career tab
   - Click + button
   - Add: "Become a Senior Developer"
   - Description: "Learn advanced Python and system design"
   - Click "Add"

4. **Add Health Record:**
   - Go to Health tab
   - Click + button
   - Type: "weight"
   - Value: "70"
   - Unit: "kg"
   - Click "Add"

5. **Add Financial Transaction:**
   - Go to Finance tab
   - Click + button
   - Type: "income"
   - Category: "salary"
   - Amount: "5000"
   - Click "Add"

---

## Testing

### Test Backend API with curl

```bash
# 1. Register a user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123",
    "full_name": "Test User"
  }'

# 2. Login and get token
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"

# Save the access_token from response

# 3. Get career goals (replace YOUR_TOKEN with actual token)
curl -X GET "http://localhost:8000/career/goals" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 4. Create a career goal
curl -X POST "http://localhost:8000/career/goals" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Machine Learning",
    "description": "Complete ML course on Coursera"
  }'
```

### Test with Swagger UI

1. Open http://localhost:8000/docs
2. Click "Authorize" button
3. Enter your token (from login)
4. Try the endpoints interactively

### Test Flutter App

1. Run the app
2. Register/Login
3. Test all three tabs (Career, Health, Finance)
4. Verify data persistence

---

## Troubleshooting

### Backend Issues

#### Database Connection Error

**Error:** `could not connect to server`

**Solution:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list | grep postgresql  # macOS

# Check connection
psql -U thrivementor -d thrivementor -h localhost

# Verify DATABASE_URL in .env file
cat backend/.env
```

#### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # Linux/macOS
taskkill /PID <PID> /F  # Windows

# Or use a different port
uvicorn main:app --reload --port 8001
```

#### Import Errors

**Error:** `ModuleNotFoundError: No module named 'shared'`

**Solution:**
```bash
# Make sure you're in the backend directory
cd backend

# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues

#### Flutter Build Errors

**Error:** `Failed to build`

**Solution:**
```bash
# Clean build
flutter clean
flutter pub get
flutter run
```

#### API Connection Error

**Error:** `Failed to connect to API`

**Solution:**
1. Verify backend is running: http://localhost:8000/health
2. Check API base URL in `auth_service.dart` and `api_service.dart`
3. For Android emulator, use `http://10.0.2.2:8000`
4. For physical device, use your computer's IP address
5. Check firewall settings

#### CORS Errors (Web)

**Error:** `CORS policy blocked`

**Solution:**
- Backend already has CORS middleware configured
- Make sure backend is running
- Check browser console for specific error

### Database Issues

#### Tables Not Created

**Solution:**
```bash
cd backend
python init_db.py
```

#### Migration Errors

**Solution:**
```bash
# If using Alembic
alembic upgrade head

# Or recreate database
dropdb thrivementor
createdb thrivementor
python init_db.py
```

---

## Next Steps

After successfully running the application:

1. **Enhance ML Models:** Integrate more sophisticated ML algorithms
2. **Add More Features:** 
   - Push notifications
   - Data export
   - Advanced analytics
   - Social features
3. **Improve UI/UX:**
   - Add charts and graphs
   - Improve animations
   - Add dark mode
4. **Deploy:**
   - Backend: Deploy to AWS, Heroku, or DigitalOcean
   - Frontend: Deploy Flutter web or publish to app stores
5. **Add Testing:**
   - Unit tests
   - Integration tests
   - E2E tests

---

## Quick Reference

### Backend Commands

```bash
# Start server
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Initialize database
python init_db.py

# Run migrations (if using Alembic)
alembic upgrade head
```

### Frontend Commands

```bash
# Run app
cd frontend/flutter_app
flutter run

# Build for production
flutter build apk          # Android
flutter build ios          # iOS
flutter build web          # Web
```

### Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose up --build
```

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review error messages carefully
3. Check logs:
   - Backend: Terminal where uvicorn is running
   - Frontend: Flutter console output
   - Database: PostgreSQL logs
4. Verify all prerequisites are installed correctly
5. Ensure all services are running

---

**Happy Coding! 🚀**


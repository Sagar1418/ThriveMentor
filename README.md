# ThriveMentor - AI-Powered Personal Dashboard

A full-stack personal wellness & productivity hub integrating career mentor, health assistant, and financial planner. Built with FastAPI, PostgreSQL, JWT authentication, Flutter, and ML-powered recommendations.

## 🚀 Features

- **Career Management**: Set and track career goals with progress monitoring
- **Health Tracking**: Log health records (weight, exercise, mood, sleep, etc.)
- **Financial Planning**: Track income, expenses, and investments with analytics
- **AI Recommendations**: ML-powered personalized recommendations for all areas
- **JWT Authentication**: Secure user authentication and authorization
- **Microservices Architecture**: Scalable backend with separate services
- **Modern Flutter UI**: Beautiful, responsive mobile and web interface

## 🏗️ Architecture

### Backend (Microservices)
- **Auth Service**: User registration, login, JWT token management
- **Career Service**: Career goals management and recommendations
- **Health Service**: Health records tracking and analytics
- **Finance Service**: Financial transactions and budget analysis
- **Shared**: Common database models, schemas, security utilities, ML service

### Frontend
- **Flutter App**: Cross-platform mobile and web application
- **State Management**: Provider pattern
- **API Integration**: RESTful API communication

### Database
- **PostgreSQL**: Relational database for all data storage

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.11+
- PostgreSQL 15+
- Flutter SDK 3.0+
- Docker and Docker Compose (optional, for containerized deployment)
- Git

## 🛠️ Step-by-Step Implementation Guide

### Step 1: Clone and Set Up Project

```bash
# Navigate to your project directory
cd /home/sagark24/ThriveMentor

# Verify project structure
ls -la
```

### Step 2: Set Up PostgreSQL Database

#### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL container
docker-compose up -d postgres

# Wait for database to be ready (check logs)
docker-compose logs postgres
```

#### Option B: Local PostgreSQL Installation

```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql

# Create database and user
sudo -u postgres psql
```

In PostgreSQL shell:
```sql
CREATE DATABASE thrivementor;
CREATE USER thrivementor WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE thrivementor TO thrivementor;
\q
```

### Step 3: Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your database credentials and secret key
nano .env  # or use your preferred editor
```

Update `.env` file:
```
DATABASE_URL=postgresql://thrivementor:password@localhost:5432/thrivementor
SECRET_KEY=your-super-secret-key-change-this-in-production
```

```bash
# Initialize database tables
python init_db.py

# Run database migrations (if using Alembic)
alembic upgrade head
```

### Step 4: Start Backend Services

#### Option A: Run All Services Together (Development)

```bash
# From backend directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Option B: Run Services Separately (Microservices)

```bash
# Terminal 1 - Auth Service
cd auth_service
uvicorn main:app --reload --port 8001

# Terminal 2 - Career Service
cd career_service
uvicorn main:app --reload --port 8002

# Terminal 3 - Health Service
cd health_service
uvicorn main:app --reload --port 8003

# Terminal 4 - Finance Service
cd finance_service
uvicorn main:app --reload --port 8004
```

#### Option C: Using Docker Compose

```bash
# From project root
docker-compose up --build
```

### Step 5: Verify Backend API

```bash
# Test API health
curl http://localhost:8000/health

# View API documentation
# Open browser: http://localhost:8000/docs
```

### Step 6: Set Up Flutter Frontend

```bash
# Navigate to Flutter app directory
cd frontend/flutter_app

# Get Flutter dependencies
flutter pub get

# Create assets directory
mkdir -p assets/images assets/icons

# Update API base URL in lib/services/auth_service.dart and api_service.dart
# Change 'http://localhost:8000' to your backend URL
# For Android emulator: use 'http://10.0.2.2:8000'
# For iOS simulator: use 'http://localhost:8000'
# For physical device: use your computer's IP address
```

### Step 7: Run Flutter App

```bash
# Check Flutter setup
flutter doctor

# Run on connected device/emulator
flutter run

# Or build for specific platform
flutter build apk          # Android
flutter build ios          # iOS
flutter build web          # Web
```

### Step 8: Test the Application

1. **Register a New User**:
   - Open the app
   - Click "Register"
   - Fill in email, username, password
   - Submit

2. **Login**:
   - Use your credentials to login
   - You should see the dashboard with three tabs

3. **Add Career Goals**:
   - Go to Career tab
   - Click + button
   - Add a goal title and description
   - View your goals list

4. **Add Health Records**:
   - Go to Health tab
   - Click + button
   - Add record type (e.g., "weight"), value, and unit
   - View your health records

5. **Add Financial Transactions**:
   - Go to Finance tab
   - Click + button
   - Add transaction type, category, amount
   - View financial summary and transactions

6. **View Recommendations**:
   - After adding data, ML recommendations will be generated
   - Check recommendations endpoints via API or add UI components

## 📁 Project Structure

```
ThriveMentor/
├── backend/
│   ├── auth_service/
│   │   └── main.py              # Authentication service
│   ├── career_service/
│   │   └── main.py              # Career goals service
│   ├── health_service/
│   │   └── main.py              # Health tracking service
│   ├── finance_service/
│   │   └── main.py              # Financial planning service
│   ├── shared/
│   │   ├── database.py          # Database connection
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── security.py          # JWT & password hashing
│   │   └── ml_service.py        # ML recommendation service
│   ├── main.py                  # API Gateway
│   ├── init_db.py               # Database initialization
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Backend Docker image
│   └── .env.example             # Environment variables template
├── frontend/
│   └── flutter_app/
│       ├── lib/
│       │   ├── main.dart        # App entry point
│       │   ├── services/
│       │   │   ├── auth_service.dart
│       │   │   └── api_service.dart
│       │   └── screens/
│       │       ├── login_screen.dart
│       │       ├── dashboard_screen.dart
│       │       ├── career_tab.dart
│       │       ├── health_tab.dart
│       │       └── finance_tab.dart
│       └── pubspec.yaml         # Flutter dependencies
├── docker-compose.yml           # Docker orchestration
└── README.md                    # This file
```

## 🔧 Configuration

### Backend Environment Variables

Create `backend/.env`:
```env
DATABASE_URL=postgresql://thrivementor:password@localhost:5432/thrivementor
SECRET_KEY=your-secret-key-change-in-production
```

### Flutter API Configuration

Update `lib/services/auth_service.dart` and `api_service.dart`:
```dart
static const String baseUrl = 'http://YOUR_BACKEND_IP:8000';
```

For different platforms:
- **Android Emulator**: `http://10.0.2.2:8000`
- **iOS Simulator**: `http://localhost:8000`
- **Physical Device**: `http://YOUR_COMPUTER_IP:8000`
- **Web**: `http://localhost:8000`

## 🧪 Testing API Endpoints

### Using curl:

```bash
# Register user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"testpass123","full_name":"Test User"}'

# Login
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"

# Get career goals (replace TOKEN with actual token)
curl -X GET "http://localhost:8000/career/goals" \
  -H "Authorization: Bearer TOKEN"
```

### Using Swagger UI:

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🤖 ML Integration

The current ML service (`shared/ml_service.py`) provides basic recommendation logic. To enhance it:

1. **Integrate TensorFlow/PyTorch models**:
   ```python
   import tensorflow as tf
   # Load your trained model
   model = tf.keras.models.load_model('models/career_recommender.h5')
   ```

2. **Use scikit-learn for analytics**:
   ```python
   from sklearn.cluster import KMeans
   # Analyze user patterns
   ```

3. **Add more sophisticated recommendation algorithms**:
   - Collaborative filtering
   - Content-based filtering
   - Deep learning models

## 🚀 Deployment

### Backend Deployment

1. **Production Environment Variables**:
   ```bash
   export DATABASE_URL=postgresql://user:pass@prod-db:5432/thrivementor
   export SECRET_KEY=$(openssl rand -hex 32)
   ```

2. **Using Docker**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Using Gunicorn** (for production):
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
   ```

### Flutter Deployment

```bash
# Build for production
flutter build apk --release          # Android
flutter build ios --release          # iOS
flutter build web --release          # Web

# Deploy web version
flutter build web
# Upload build/web directory to your web server
```

## 📝 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/token` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Career
- `GET /career/goals` - List all career goals
- `POST /career/goals` - Create new career goal
- `GET /career/goals/{id}` - Get specific goal
- `PUT /career/goals/{id}` - Update goal
- `PATCH /career/goals/{id}/progress` - Update progress
- `GET /career/recommendations` - Get ML recommendations

### Health
- `GET /health/records` - List health records
- `POST /health/records` - Create health record
- `GET /health/analytics/summary` - Get health summary
- `GET /health/recommendations` - Get ML recommendations

### Finance
- `GET /finance/transactions` - List transactions
- `POST /finance/transactions` - Create transaction
- `GET /finance/analytics/summary` - Get financial summary
- `GET /finance/recommendations` - Get ML recommendations

## 🔒 Security Best Practices

1. **Change default SECRET_KEY** in production
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** in production
4. **Implement rate limiting** for API endpoints
5. **Add input validation** and sanitization
6. **Use prepared statements** (SQLAlchemy handles this)
7. **Implement CORS properly** (restrict origins in production)

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U thrivementor -d thrivementor -h localhost
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

### Flutter Build Issues
```bash
# Clean build
flutter clean
flutter pub get
flutter run
```

## 📚 Next Steps

1. **Enhance ML Models**: Integrate more sophisticated ML algorithms
2. **Add Real-time Features**: WebSocket support for live updates
3. **Implement Caching**: Redis for improved performance
4. **Add Testing**: Unit tests, integration tests
5. **CI/CD Pipeline**: Automated testing and deployment
6. **Monitoring**: Add logging and monitoring (e.g., Prometheus, Grafana)
7. **Mobile Features**: Push notifications, offline support
8. **Advanced Analytics**: More detailed charts and insights

## 📄 License

This project is open source and available under the MIT License.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on the repository.

---

**Built with ❤️ using FastAPI, PostgreSQL, Flutter, and ML**


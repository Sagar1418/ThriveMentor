# ThriveMentor - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites Check
```bash
python3 --version  # Need 3.11+
psql --version      # Need PostgreSQL
flutter --version   # Need Flutter 3.0+
```

### 1. Start Database (Choose One)

**Option A: Docker (Easiest)**
```bash
docker-compose up -d postgres
```

**Option B: Local PostgreSQL**
```bash
# Create database
sudo -u postgres psql -c "CREATE DATABASE thrivementor;"
sudo -u postgres psql -c "CREATE USER thrivementor WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE thrivementor TO thrivementor;"
```

### 2. Setup Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database URL
python init_db.py
```

### 3. Start Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Verify: Open http://localhost:8000/docs

### 4. Setup Flutter Frontend

```bash
cd ../frontend/flutter_app
flutter pub get
```

**Important:** Update API URL in:
- `lib/services/auth_service.dart`
- `lib/services/api_service.dart`

Change `baseUrl` to:
- Android Emulator: `http://10.0.2.2:8000`
- iOS Simulator: `http://localhost:8000`
- Physical Device: `http://YOUR_COMPUTER_IP:8000`

### 5. Run Flutter App

```bash
flutter run
```

### 6. Test It!

1. Register a new user
2. Login
3. Add career goals, health records, and financial transactions
4. View your dashboard!

---

## 📚 Full Documentation

- **Detailed Guide:** See [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
- **Project README:** See [README.md](README.md)

## 🆘 Troubleshooting

**Backend won't start?**
- Check PostgreSQL is running
- Verify DATABASE_URL in `.env`
- Check port 8000 is available

**Flutter can't connect?**
- Verify backend is running: http://localhost:8000/health
- Check API base URL in Flutter services
- For Android emulator, use `10.0.2.2` instead of `localhost`

**Database errors?**
- Run `python backend/init_db.py` again
- Check PostgreSQL is running: `sudo systemctl status postgresql`

---

**Need Help?** Check the full [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for detailed instructions.


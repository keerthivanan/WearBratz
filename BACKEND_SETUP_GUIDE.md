# 🚀 BACKEND SETUP GUIDE

## Quick Start

### 1. Install System Dependencies (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    postgresql-client \
    libpq-dev \
    python3-dev \
    build-essential \
    libmagic1 \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    redis-server
```

### 2. Install System Dependencies (macOS)
```bash
brew install python@3.12 postgresql redis libmagic cairo pango gdk-pixbuf
```

### 3. Create Virtual Environment
```bash
# Create virtual environment
python3.12 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

### 4. Install Python Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### 5. Create Environment Variables
```bash
# Copy example env file
cp .env.example .env

# Edit with your keys
nano .env
```

### 6. Run Migrations
```bash
# Initialize Alembic
alembic init alembic

# Create first migration
alembic revision --autogenerate -m "Initial tables"

# Apply migrations
alembic upgrade head
```

### 7. Start the Server
```bash
# Development (with auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 📦 What Each Package Does

### **Core Framework**
- `fastapi` - Modern API framework (like Express.js but Python)
- `uvicorn` - Lightning-fast ASGI server
- `pydantic` - Data validation (ensures data types are correct)

### **Database**
- `sqlalchemy` - ORM (talk to PostgreSQL without raw SQL)
- `alembic` - Database migrations (version control for your DB schema)
- `asyncpg` - Async PostgreSQL driver (super fast)

### **Caching**
- `redis` - In-memory cache (makes everything faster)
- `hiredis` - Redis speed booster

### **Authentication**
- `python-jose` - JWT tokens for login sessions
- `passlib` - Password hashing (security)

### **Payment**
- `stripe` - Accept payments

### **Email**
- `resend` - Send transactional emails

### **AI**
- `openai` - GPT-4o for product descriptions
- `anthropic` - Claude for complex quote analysis

### **Images**
- `cloudinary` - Image hosting & optimization
- `pillow` - Image processing
- `rembg` - AI background removal

### **Data Processing**
- `pandas` - Excel-like data manipulation
- `numpy` - Math operations

### **PDF Generation**
- `reportlab` - Create PDFs programmatically
- `weasyprint` - HTML to PDF conversion

### **Integrations**
- `gspread` - Google Sheets API
- `pyairtable` - Airtable API
- `meilisearch` - Fast search engine

### **Testing**
- `pytest` - Test framework
- `faker` - Generate fake data for tests

---

## 🔧 Configuration (.env file)

Create a `.env` file in your backend root:

```bash
# ==================== CORE ====================
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-super-secret-key-change-this-in-production
API_VERSION=v1

# ==================== DATABASE ====================
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dollstore
# For Railway: postgresql://user:password@containers-us-west-xxx.railway.app:5432/railway

# ==================== REDIS ====================
REDIS_URL=redis://localhost:6379/0
# For Railway: redis://default:password@containers-us-west-xxx.railway.app:6379

# ==================== STRIPE ====================
STRIPE_SECRET_KEY=sk_test_51xxx...
STRIPE_PUBLISHABLE_KEY=pk_test_51xxx...
STRIPE_WEBHOOK_SECRET=whsec_xxx...

# ==================== OPENAI ====================
OPENAI_API_KEY=sk-proj-xxx...

# ==================== ANTHROPIC ====================
ANTHROPIC_API_KEY=sk-ant-xxx...

# ==================== CLOUDINARY ====================
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=xxxxxxxxxxxxxxxxxxxxxx

# ==================== RESEND ====================
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxx
RESEND_FROM_EMAIL=hello@yourdollstore.com

# ==================== GOOGLE SHEETS ====================
GOOGLE_SHEETS_CREDENTIALS_JSON={"type": "service_account", ...}
GOOGLE_SHEETS_INVENTORY_ID=1aBcDeFgHiJkLmNoPqRsTuVwXyZ

# ==================== AIRTABLE ====================
AIRTABLE_API_KEY=keyxxxxxxxxxxxxx
AIRTABLE_BASE_ID=appxxxxxxxxxxxxx

# ==================== MEILISEARCH ====================
MEILISEARCH_URL=http://localhost:7700
MEILISEARCH_MASTER_KEY=masterKey

# ==================== FRONTEND URL ====================
FRONTEND_URL=http://localhost:3000
# Production: https://yourdollstore.com

# ==================== CORS ====================
ALLOWED_ORIGINS=http://localhost:3000,https://yourdollstore.com

# ==================== N8N WEBHOOKS ====================
N8N_WEBHOOK_URL=https://n8n.yourdollstore.com/webhook
N8N_WEBHOOK_SECRET=your-n8n-webhook-secret

# ==================== SENTRY (Error Tracking) ====================
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx

# ==================== RATE LIMITING ====================
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60
```

---

## 🐳 Docker Setup (Optional but Recommended)

### Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    libmagic1 \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run migrations and start server
CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/dollstore
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - .:/app
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8000

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dollstore
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=changethis
      - WEBHOOK_URL=http://localhost:5678
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  postgres_data:
  redis_data:
  n8n_data:
```

### Run with Docker
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_products.py

# Run and show print statements
pytest -s
```

---

## 📚 Common Commands

```bash
# Create new migration
alembic revision --autogenerate -m "Add new column"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Format code
black .

# Check code quality
flake8 .

# Sort imports
isort .

# Type checking
mypy app/

# Install new package
pip install package-name
pip freeze > requirements.txt
```

---

## 🚨 Troubleshooting

### "ModuleNotFoundError: No module named 'XXX'"
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

### "Connection refused" (PostgreSQL)
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list  # macOS

# Start PostgreSQL
sudo systemctl start postgresql  # Linux
brew services start postgresql  # macOS
```

### "Connection refused" (Redis)
```bash
# Check if Redis is running
redis-cli ping  # Should return "PONG"

# Start Redis
sudo systemctl start redis  # Linux
brew services start redis  # macOS
```

### WeasyPrint installation fails
```bash
# macOS
brew install cairo pango gdk-pixbuf libffi

# Ubuntu
sudo apt-get install libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0
```

---

## 🎯 Next Steps

1. ✅ Install all dependencies
2. ✅ Set up `.env` file with your API keys
3. ✅ Run database migrations
4. ✅ Start the development server
5. ✅ Test the API at `http://localhost:8000/docs`
6. 🚀 Build your endpoints!

---

**Need help?** Check the FastAPI docs: https://fastapi.tiangolo.com

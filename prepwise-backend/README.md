# Campus-Prep Backend API

FastAPI backend for PrepWise interview preparation platform.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file from `.env.example` and fill in your API keys

3. Run the server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

- `GEMINI_API_KEY`: Google Gemini API key
- `FIREBASE_CREDENTIALS_PATH`: Path to Firebase service account JSON
- `FIREBASE_PROJECT_ID`: Firebase project ID
- `DEBUG`: Enable debug mode
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)

## Deployment

Build Docker image:
```bash
docker build -t prepwise-backend .
```

Run container:
```bash
docker run -p 8000:8000 --env-file .env prepwise-backend
```

# PrepWise Frontend

React frontend for PrepWise interview preparation platform.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file from `.env.example` and fill in your Firebase config

3. Run the development server:
```bash
npm run dev
```

The app will be available at http://localhost:3000

## Environment Variables

- `VITE_FIREBASE_API_KEY`: Firebase API key
- `VITE_FIREBASE_AUTH_DOMAIN`: Firebase auth domain
- `VITE_FIREBASE_PROJECT_ID`: Firebase project ID
- `VITE_FIREBASE_STORAGE_BUCKET`: Firebase storage bucket
- `VITE_FIREBASE_MESSAGING_SENDER_ID`: Firebase messaging sender ID
- `VITE_FIREBASE_APP_ID`: Firebase app ID
- `VITE_BACKEND_URL`: Backend API URL (default: http://localhost:8000)

## Build

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

# Frontend - SWS AI Policy Assistant

This is the React + Vite frontend for the SWS AI Policy Assistant.

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file from the example:
```bash
cp .env.example .env
```

4. Update `.env` with your backend API URL (default is already set to `http://localhost:8000`)

## Development

Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Building

Build for production:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatBox.jsx         # Main chat component
│   │   ├── MessageBubble.jsx   # Individual message component
│   │   ├── SourceList.jsx      # Sources display component
│   │   ├── Loader.jsx          # Loading indicator
│   │   └── Header.jsx          # Application header
│   ├── App.jsx                 # Root component
│   ├── main.jsx                # Entry point
│   ├── App.css                 # Application styles
│   └── index.css               # Global styles
├── index.html                  # HTML template
├── vite.config.js             # Vite configuration
├── package.json               # Project dependencies
└── .env.example               # Environment variables template
```

## Features

- Clean, modern chat interface
- Real-time API communication with the backend
- Loading indicators and error handling
- Source document display
- Responsive design for mobile and desktop
- Professional white and blue theme with Livvic font

## API Integration

The frontend communicates with the backend via the following endpoints:

- `POST /api/chat` - Send a question and receive an answer
- `GET /api/health` - Check backend health
- `GET /api/info` - Get information about the RAG pipeline

## Troubleshooting

- If you see CORS errors, make sure the backend is running and CORS is enabled
- If the API connection fails, check that `VITE_API_URL` is set correctly
- Make sure the backend is running on `http://localhost:8000` before starting the frontend

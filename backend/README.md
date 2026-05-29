# Backend - SWS AI Policy Assistant

FastAPI backend for the SWS AI Policy Assistant with RAG-powered chatbot capabilities.

## Prerequisites

- Python 3.9+
- pip (Python package manager)
- Groq API Key (free from https://console.groq.com)

## Installation

### 1. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r app/requirements.txt
```

### 3. Setup Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_key_here
```

## Quick Start

### Step 1: Add PDF Documents

Place your PDF files in:
```
backend/data/pdfs/
```

Example structure:
```
backend/data/pdfs/
├── Leave_Policy.pdf
├── HR_Manual.pdf
├── Code_of_Conduct.pdf
└── Benefits_Guide.pdf
```

### Step 2: Ingest Documents

From the backend directory:
```bash
python app/ingest.py
```

Output will show:
```
============================================================
STARTING PDF INGESTION PIPELINE
============================================================

Found 4 PDF file(s)
...
Total chunks created: 245
✓ Successfully stored 245 chunks in ChromaDB
```

### Step 3: Start API Server

```bash
py app/main.py
```

Server will start at `http://localhost:8000`

View API documentation: `http://localhost:8000/docs`

## API Endpoints

### Chat Endpoint
Send a question to the RAG pipeline:
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the leave policy?"}'
```

Response:
```json
{
  "answer": "The leave policy provides employees with...",
  "sources": ["Leave_Policy.pdf"]
}
```

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Pipeline Info
```bash
curl http://localhost:8000/api/info
```

## Project Structure

```
backend/
├── app/
│   ├── main.py                  # FastAPI application and endpoints
│   ├── rag_pipeline.py          # RAG pipeline with LangChain
│   ├── ingest.py                # Document ingestion script
│   ├── config.py                # Configuration and settings
│   ├── prompts.py               # LLM prompt templates
│   ├── utils.py                 # Utility functions
│   ├── requirements.txt         # Python dependencies
│   └── __init__.py
│
├── data/
│   └── pdfs/                    # Place PDF files here
│
├── chroma_db/                   # Vector database (auto-created)
│
├── .env.example                 # Environment template
└── README.md                    # This file
```

## Configuration

### Adjust Chunking Parameters

Edit `backend/app/config.py`:
```python
CHUNK_SIZE = 500          # Increase for larger chunks
CHUNK_OVERLAP = 50        # Increase for more overlap
```

Then re-run:
```bash
python app/ingest.py
```

### Adjust Retrieval Settings

Edit `backend/app/config.py`:
```python
RETRIEVER_K = 4           # Number of chunks to retrieve
```

### Change API Port

Edit `backend/app/config.py`:
```python
API_PORT = 8001           # Use different port
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.104.1 | Web framework |
| uvicorn | 0.24.0 | ASGI server |
| langchain | 0.1.0 | RAG framework |
| langchain-community | 0.0.13 | LangChain extensions |
| langchain-groq | 0.1.0 | Groq LLM integration |
| chromadb | 0.4.10 | Vector database |
| sentence-transformers | 2.2.2 | Embeddings model |
| pymupdf | 1.23.5 | PDF extraction |
| python-dotenv | 1.0.0 | Environment variables |

## Development

### Enable Debug Mode

Edit `backend/app/config.py`:
```python
API_RELOAD = True  # Hot reload on file changes
```

### View Logs

The application outputs detailed logs:
- Document ingestion progress
- API startup/shutdown
- Request/response details
- Error traces

### Test API with cURL

```bash
# Test health
curl http://localhost:8000/api/health

# Test chat
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'

# View docs
curl http://localhost:8000/docs
```

## Troubleshooting

### Issue: "Module not found"
```bash
Solution: Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
```

### Issue: "Groq API Error"
```
1. Check API key in .env file
2. Get new key from https://console.groq.com
3. Restart the server
```

### Issue: "ChromaDB directory not found"
```bash
Solution: Create it manually
mkdir chroma_db
Then run: python app/ingest.py
```

### Issue: "PDF extraction error"
```
1. Check PDF file is valid
2. Try opening it in Adobe Reader
3. Check file permissions
4. Some PDFs may not be readable by PyMuPDF
```

### Issue: "Port 8000 already in use"
```bash
# Windows: Find process using port
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or use different port
# Edit config.py: API_PORT = 8001
```

## Performance Tips

1. **Reduce chunk size** - Faster retrieval, less context
   ```python
   CHUNK_SIZE = 300
   ```

2. **Reduce retriever_k** - Fewer API calls to Groq
   ```python
   RETRIEVER_K = 2
   ```

3. **Optimize embeddings** - Use cached embeddings on first request

4. **Database optimization** - ChromaDB uses local files for speed

## Extending the Application

### Add Custom LLM Provider
Modify `rag_pipeline.py`:
```python
# Replace ChatGroq with your provider
from langchain_openai import ChatOpenAI
self.llm = ChatOpenAI(model="gpt-4")
```

### Add Request Logging
Add to `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Add Rate Limiting
```python
from slowapi import Limiter
limiter = Limiter(key_func=...)
@app.post("/api/chat")
@limiter.limit("10/minute")
```

### Add Authentication
```python
from fastapi.security import HTTPBearer
security = HTTPBearer()

@app.post("/api/chat")
async def chat(request: ChatRequest, credentials = Depends(security)):
```

## Production Deployment

### Docker Support (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt
COPY app app/
CMD ["python", "app/main.py"]
```

### Environment Variables for Production

```bash
# Update .env
GROQ_API_KEY=your_production_key
API_HOST=0.0.0.0
API_PORT=8000
```

### Security Checklist

- ✅ Use environment variables for secrets
- ✅ Enable CORS for specific domains
- ✅ Add rate limiting
- ✅ Add API authentication
- ✅ Enable HTTPS
- ✅ Add request validation
- ✅ Add error logging
- ✅ Monitor API usage

## API Documentation

Once the server is running, visit:
```
http://localhost:8000/docs
```

Interactive API documentation powered by FastAPI and Swagger UI.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the main README.md
3. Check backend logs
4. Verify PDF files are valid

## License

Open source - Feel free to modify and use for your needs.

---

Made with ❤️ for SWS AI

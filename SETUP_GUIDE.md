# 🚀 Complete Setup Guide - SWS AI Policy Assistant

This guide will walk you through setting up and running the complete RAG-powered chatbot application on your local machine.

## 📋 Prerequisites

Before starting, make sure you have:

1. **Python 3.9 or higher**
   - Check: `python --version`
   - Download: https://www.python.org/downloads/

2. **Node.js v16 or higher**
   - Check: `node --version` and `npm --version`
   - Download: https://nodejs.org/

3. **Groq API Key (Free)**
   - Sign up: https://console.groq.com
   - Get API key from dashboard
   - No payment required for free tier!

4. **Text Editor or IDE**
   - VS Code (recommended): https://code.visualstudio.com/
   - PyCharm, Sublime Text, or any editor

## 📁 Step 0: Project Structure

Navigate to your project directory:
```bash
cd c:\Users\Mohamed Thoufiq\OneDrive\Desktop\Shaheen
```

Current structure:
```
Shaheen/
├── backend/
│   ├── app/
│   ├── data/pdfs/          ← Add PDFs here
│   ├── chroma_db/          ← Auto-created
│   └── .env.example
├── frontend/
│   └── src/
├── README.md
└── .gitignore
```

## 🔧 BACKEND SETUP (Python)

### Step 1: Create Python Virtual Environment

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in terminal.

### Step 2: Install Python Dependencies

```bash
pip install -r app/requirements.txt
```

This installs:
- FastAPI (web framework)
- LangChain (RAG framework)
- ChromaDB (vector database)
- sentence-transformers (embeddings)
- Groq API integration
- And more...

**Wait for installation to complete** (might take 2-3 minutes on first run)

### Step 3: Setup Environment Variables

Create `.env` file in backend directory:

**Windows (Command Prompt):**
```bash
copy .env.example .env
```

**Windows (PowerShell):**
```bash
Copy-Item .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

### Step 4: Add Your Groq API Key

Edit `backend/.env`:
```
GROQ_API_KEY=your_groq_api_key_here
```

Don't have a key? Get one free:
1. Visit https://console.groq.com
2. Sign up with email
3. Go to API Keys section
4. Copy your API key
5. Paste into `.env`

### Step 5: Add PDF Documents

1. Find your PDF policy documents
2. Copy them to `backend/data/pdfs/` folder

Example:
```
backend/data/pdfs/
├── Leave_Policy.pdf
├── HR_Manual.pdf
├── Benefits_Guide.pdf
└── Employee_Handbook.pdf
```

**Important**: Make sure PDFs are:
- Valid PDF files
- In English or supported language
- Readable (not scanned images only)
- Less than 50MB each

### Step 6: Ingest Documents

Run the ingestion pipeline:
```bash
py app/ingest.py
```

Expected output:
```
============================================================
STARTING PDF INGESTION PIPELINE
============================================================

Found 4 PDF file(s)
-----------
Processing: Leave_Policy.pdf
  - Extracted 8 page(s)

Processing: HR_Manual.pdf
  - Extracted 15 page(s)

...

Total pages extracted: 38
============================================================
SPLITTING DOCUMENTS INTO CHUNKS
============================================================
Chunk size: 500
Chunk overlap: 50

Total chunks created: 245
============================================================
INITIALIZING EMBEDDING MODEL
============================================================
Downloading model... (this may take a moment on first run)
✓ Embedding model loaded successfully

============================================================
STORING EMBEDDINGS IN CHROMADB
============================================================
✓ Successfully stored 245 chunks in ChromaDB

============================================================
INGESTION PIPELINE COMPLETED SUCCESSFULLY
============================================================
```

**First time?** The embedding model (~100MB) will be downloaded. This only happens once.

### Step 7: Start Backend Server

Keep the same terminal open and run:
```bash
py app/main.py
```

Expected output:
```
============================================================
Starting SWS AI Policy Assistant API
Host: 0.0.0.0:8000
============================================================

INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**✅ Backend is running!**

Test it:
- Open browser: http://localhost:8000/docs
- You should see interactive API documentation

**Keep this terminal open!** Don't close it while using the app.

---

## 💻 FRONTEND SETUP (React)

### Step 8: Open New Terminal Window

Open a NEW terminal (keep backend running in first terminal)

Navigate to frontend:
```bash
cd frontend
```

Make sure you're NOT in the `venv` from backend.

### Step 9: Install Node Dependencies

```bash
npm install
```

Expected output:
```
added 150 packages in 45s
```

### Step 10: Create Environment File

**Windows (Command Prompt):**
```bash
copy .env.example .env
```

**Windows (PowerShell):**
```bash
Copy-Item .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

The `.env` should contain:
```
VITE_API_URL=http://localhost:8000
```

This tells frontend where to find the backend API.

### Step 11: Start Frontend Development Server

```bash
npm run dev
```

Expected output:
```
  VITE v5.0.0  ready in 123 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### Step 12: Open the Application

1. Open your web browser
2. Visit: http://localhost:5173
3. You should see the chat interface!

**✅ Frontend is running!**

---

## ✨ Test the Application

### Test in Browser

1. **Type a question** in the chat box
   - Example: "What is the leave policy?"
   - Example: "How do I request time off?"

2. **Send the message**
   - Click send button or press Enter

3. **You should see**:
   - Loading indicator (dots bouncing)
   - AI response from your documents
   - Source documents listed below

### Troubleshooting First Run

**Issue: Empty answer or "no documents"**
```
Solution: Make sure you ran: python app/ingest.py
Check backend console for document count
```

**Issue: API Connection Error**
```
Solution:
1. Make sure backend is running (first terminal)
2. Check VITE_API_URL in frontend/.env
3. Both should use http://localhost:8000
```

**Issue: Groq API Error**
```
Solution:
1. Check API key in backend/.env
2. Get new key from https://console.groq.com
3. Restart backend server
```

---

## 🎯 What's Happening Behind the Scenes

### Question Flow

```
User types question in frontend
    ↓
Frontend sends to http://localhost:8000/api/chat
    ↓
Backend receives question
    ↓
Convert question to embeddings
    ↓
Search ChromaDB for similar document chunks
    ↓
Send context + question to Groq LLM
    ↓
LLM generates answer based on context
    ↓
Backend returns answer + sources
    ↓
Frontend displays answer and sources
```

### Key Components

1. **ChromaDB** - Stores embeddings of your PDFs locally
2. **sentence-transformers** - Converts text to vectors
3. **LangChain** - Orchestrates the RAG pipeline
4. **Groq LLM** - Generates answers (via API)
5. **FastAPI** - Serves the backend
6. **React** - Shows the UI

---

## 📊 Monitoring

### Check Backend Health

```bash
curl http://localhost:8000/api/health
```

Response:
```json
{
  "status": "ok",
  "message": "RAG pipeline is ready with 245 document chunks"
}
```

### Check Vector Store Info

```bash
curl http://localhost:8000/api/info
```

### View API Docs

Visit: http://localhost:8000/docs

Try endpoints directly from the browser!

---

## 🛑 Stopping the Application

1. **To stop backend**: Press `Ctrl+C` in backend terminal
2. **To stop frontend**: Press `Ctrl+C` in frontend terminal

---

## 🔄 Updating Documents

To update your PDFs:

1. Replace files in `backend/data/pdfs/`
2. Stop backend server (Ctrl+C)
3. Run ingestion again:
   ```bash
   python app/ingest.py
   ```
4. Start backend again:
   ```bash
   python app/main.py
   ```

The new documents will be ingested and available immediately.

---

## 📈 Performance Tips

### Faster Responses

1. **Reduce chunk retrieval**
   - Edit `backend/app/config.py`
   - Change `RETRIEVER_K = 2` (instead of 4)

2. **Smaller chunks**
   - Edit `backend/app/config.py`
   - Change `CHUNK_SIZE = 300` (instead of 500)
   - Re-run ingest.py

### Better Answers

1. **Larger chunks**
   - Change `CHUNK_SIZE = 800`
   - Re-run ingest.py

2. **More context**
   - Change `RETRIEVER_K = 6`
   - No need to re-ingest

---

## 🧪 Development Workflow

### For Backend Development

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Edit files in backend/app/

# Restart server
python app/main.py
```

### For Frontend Development

```bash
cd frontend
npm run dev

# Edit files in frontend/src/
# Changes auto-reload!
```

### Build Frontend for Production

```bash
cd frontend
npm run build
```

Creates optimized files in `frontend/dist/`

---

## 🚀 Deployment (Optional)

### Docker (Optional)

If you want to containerize:

**Backend Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/app/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/app .
CMD ["python", "main.py"]
```

**Frontend Dockerfile:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY frontend/package.json .
RUN npm install
COPY frontend/src src
COPY frontend/index.html .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

---

## 📚 Common Commands Reference

### Backend
```bash
# Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r app/requirements.txt

# Ingest documents
python app/ingest.py

# Start server
python app/main.py

# Deactivate environment
deactivate
```

### Frontend
```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## ✅ Checklist

Before running, verify:
- [ ] Python 3.9+ installed
- [ ] Node.js v16+ installed
- [ ] Groq API key obtained
- [ ] PDF files in backend/data/pdfs/
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] .env files created
- [ ] Ingest script ran successfully
- [ ] Backend server running
- [ ] Frontend server running
- [ ] Can access http://localhost:5173

---

## 🆘 Need Help?

1. **Check terminal output** - Error messages are usually helpful
2. **Verify prerequisites** - Make sure all tools are installed
3. **Check .env files** - Ensure API keys are correct
4. **Review README files** - Both backend and frontend have detailed READMEs
5. **Test with curl** - Use curl to test backend API directly

---

## 🎓 Learning Next

Once you get it running:

1. **Explore the code** - Read comments, understand the flow
2. **Modify prompts** - Edit `backend/app/prompts.py`
3. **Adjust chunking** - Try different `CHUNK_SIZE` values
4. **Add features** - Implement new endpoints
5. **Customize UI** - Modify React components

---

## 🎉 Congratulations!

You now have a production-ready RAG chatbot running locally!

**Next steps**:
- Test with your company documents
- Share with your team
- Deploy to production (when ready)
- Extend with more features

---

**Happy coding! 🚀**

Questions? Check the README.md files in backend/ and frontend/ directories.

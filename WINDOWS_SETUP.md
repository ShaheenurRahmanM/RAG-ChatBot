# 🚀 Windows Setup Guide - SWS AI Policy Assistant

**For Windows Users with `py` command**

This is the exact setup guide for Windows where only `py` works (not `python`).

---

## ✅ Prerequisites Check

Open PowerShell and run:

```powershell
py --version
node --version
npm --version
```

You should see versions like:
- Python 3.12.10
- Node v16+ or v18+
- npm 9+

**Don't have these?** Download:
- Python: https://www.python.org/downloads/ (includes `py`)
- Node.js: https://nodejs.org/

---

## 🔑 Step 1: Get Groq API Key

1. Visit: https://console.groq.com
2. Click "Sign Up" or "Login"
3. Go to "API Keys" section
4. Create a new API key
5. Copy the key (you'll need it later)

---

## 📁 Step 2: Navigate to Project

Open PowerShell and go to the project:

```powershell
cd c:\Users\Mohamed Thoufiq\OneDrive\Desktop\Shaheen
```

---

## 🔧 Step 3: Setup Backend

### Create Virtual Environment

```powershell
cd backend
py -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your prompt.

### Install Dependencies

```powershell
pip install -r app/requirements.txt
```

This will take 2-3 minutes. **Wait for it to complete.**

---

## 📄 Step 4: Add Your Groq API Key

Edit `backend\.env`:

```powershell
notepad .env
```

Replace the empty value with your Groq API key:

```
GROQ_API_KEY=gsk_your_actual_key_here_xxx
```

Save and close.

---

## 📚 Step 5: Add PDF Documents

1. Create a folder if not exists: `backend\data\pdfs\`
2. Add your PDF policy documents there

Example:
```
backend/data/pdfs/
├── Leave_Policy.pdf
├── HR_Manual.pdf
└── Benefits_Guide.pdf
```

**No PDFs?** The app will still run, but you won't get document-based answers.

---

## 🔄 Step 6: Ingest Documents

Make sure you're still in `backend` folder with `(venv)` active:

```powershell
py app/ingest.py
```

Wait for completion. You should see:
```
============================================================
INGESTION PIPELINE COMPLETED SUCCESSFULLY
============================================================
Total documents processed: X
Total chunks created: Y
```

If you see errors about ChromaDB or embeddings, that's normal on first run - dependencies are downloading.

---

## ▶️ Step 7: Start Backend Server

**In the same terminal** (backend folder, venv active):

```powershell
py app/main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!** Don't close it.

---

## 🎨 Step 8: Setup Frontend

**Open a NEW PowerShell window** (don't close the backend one):

```powershell
cd c:\Users\Mohamed Thoufiq\OneDrive\Desktop\Shaheen\frontend
```

### Install npm Dependencies

```powershell
npm install
```

Takes 1-2 minutes.

### Start Frontend Server

```powershell
npm run dev
```

You should see:
```
  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

---

## 🎉 Step 9: Open the App

Open your browser and visit:

```
http://localhost:5173
```

You should see:
- SWS AI Policy Assistant header
- Chat input box at bottom
- Empty chat history

**Success!** 🎊

---

## 💬 Step 10: Test It

1. Type in the chat box: `What is the leave policy?`
2. Press Enter or click send
3. Wait 3-5 seconds
4. You should see an AI response with source documents

---

## 🆘 Troubleshooting

### Issue: "Port 8000 already in use"
```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill it (replace PID with the number shown)
taskkill /PID 12345 /F
```

### Issue: "Groq API Error"
```
1. Check your API key in backend\.env
2. Make sure it's formatted correctly (no extra spaces)
3. Restart: py app/main.py
```

### Issue: "Frontend can't connect to backend"
```
1. Make sure backend terminal shows "Uvicorn running"
2. Visit http://localhost:8000/docs to test backend
3. Check frontend .env has VITE_API_URL=http://localhost:8000
```

### Issue: "PDF documents not found"
```
1. Make sure PDFs are in backend\data\pdfs\
2. Run: py app/ingest.py again
3. Restart backend: py app/main.py
```

### Issue: "ImportError" or "ModuleNotFoundError"
```powershell
# Make sure venv is activated (you see (venv) in prompt)
# If not, run:
venv\Scripts\activate

# Then reinstall:
pip install -r app/requirements.txt
```

### Issue: "pip install takes forever"
```powershell
# Try upgrading pip first:
py -m pip install --upgrade pip

# Then retry:
pip install -r app/requirements.txt
```

---

## 📊 How to Keep It Running

### Terminal 1 (Backend) - KEEP OPEN
```powershell
cd c:\Users\Mohamed Thoufiq\OneDrive\Desktop\Shaheen\backend
venv\Scripts\activate
py app/main.py
```

### Terminal 2 (Frontend) - KEEP OPEN
```powershell
cd c:\Users\Mohamed Thoufiq\OneDrive\Desktop\Shaheen\frontend
npm run dev
```

### Browser
- Open: http://localhost:5173
- Ask questions
- Enjoy!

---

## 🔄 Updating Documents

To add new PDFs:

1. Add PDFs to `backend\data\pdfs\`
2. Go to backend terminal
3. Press `Ctrl+C` to stop the server
4. Run: `py app/ingest.py`
5. Run: `py app/main.py`
6. Refresh browser (F5)

---

## 🚀 Next Steps

### Quick Wins
- [ ] Add more PDF documents
- [ ] Test with different questions
- [ ] Share with colleagues

### Learning
- Read the code comments
- Understand how RAG works
- Try modifying prompts

### Production
- Add user authentication
- Deploy to cloud (AWS/Azure/GCP)
- Setup monitoring

---

## 📚 Documentation

For more info:
- **Project Overview**: [README.md](../README.md)
- **Full Setup Guide**: [SETUP_GUIDE.md](../SETUP_GUIDE.md)
- **Architecture Deep Dive**: [PROJECT_SUMMARY.md](../PROJECT_SUMMARY.md)
- **Q&A & Issues**: [FAQ_AND_TROUBLESHOOTING.md](../FAQ_AND_TROUBLESHOOTING.md)
- **Backend Docs**: [backend/README.md](../backend/README.md)
- **Frontend Docs**: [frontend/README.md](../frontend/README.md)

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Check Python | `py --version` |
| Create venv | `py -m venv venv` |
| Activate venv | `venv\Scripts\activate` |
| Install deps | `pip install -r app/requirements.txt` |
| Ingest PDFs | `py app/ingest.py` |
| Start backend | `py app/main.py` |
| Start frontend | `npm run dev` |
| Test API | `curl http://localhost:8000/docs` |
| Access app | http://localhost:5173 |

---

## ✨ You're Ready!

Everything is set up. Your RAG chatbot is ready to answer questions!

**Current Status:**
- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:5173
- ✅ PDFs ingested and searchable
- ✅ Ready to chat!

---

## 🎯 Common Questions

**Q: Do I need to run ingest.py every time?**  
A: No, only when you add new PDFs.

**Q: Can I close the terminals?**  
A: No, keep them open while using the app.

**Q: Why is the first response slow?**  
A: First request loads the AI model (~1-2 seconds). Subsequent are faster.

**Q: Can I modify the answer style?**  
A: Yes! Edit `backend\app\prompts.py` and restart backend.

**Q: What if it still doesn't work?**  
A: See the Troubleshooting section above or check [FAQ_AND_TROUBLESHOOTING.md](../FAQ_AND_TROUBLESHOOTING.md)

---

**Happy chatting! 🎉**

*For Windows users with `py` command*  
*Last updated: May 2026*

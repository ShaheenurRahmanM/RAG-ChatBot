# 🎯 EXACT SETUP STEPS - Windows with `py` Command

**Follow these steps EXACTLY as written. Copy-paste the commands.**

---

## ✅ Prerequisites (2 minutes)

### 1. Check Python Installation

Open PowerShell and run:
```powershell
py --version
```

You should see: `Python 3.12.10` (or similar)

**If it says "not found":**
- Download Python from https://www.python.org/downloads/
- Choose Windows installer
- **IMPORTANT**: Check "Add Python to PATH"
- Reinstall and try again

### 2. Check Node.js Installation

```powershell
node --version
npm --version
```

Should show v16+ and npm 9+

**If not found:**
- Download from https://nodejs.org/
- Use LTS version
- Reinstall and try again

### 3. Get Groq API Key

Visit: https://console.groq.com
1. Click "Sign Up" (or login if you have account)
2. Verify your email
3. Go to "API Keys" section
4. Click "Create New API Key"
5. Copy the key starting with `gsk_`
6. Save it somewhere safe

**Keep this key, you'll need it in Step 5.**

---

## 🚀 EXACT SETUP COMMANDS

### Step 1: Navigate to Project

Open PowerShell and run:
```powershell
cd "c:\Users\Mohamed Thoufiq\OneDrive\Desktop\Shaheen"
```

Check it worked:
```powershell
dir
```

You should see: `backend`, `frontend`, `README.md`, etc.

### Step 2: Create Python Virtual Environment

```powershell
cd backend
py -m venv venv
```

Wait for it to complete (20-30 seconds)

### Step 3: Activate Virtual Environment

```powershell
venv\Scripts\activate
```

**Important:** You should now see `(venv)` at the beginning of your PowerShell prompt.

If you don't see `(venv)`, run again:
```powershell
venv\Scripts\activate
```

### Step 4: Install Python Dependencies

```powershell
pip install -r app/requirements.txt
```

**This will take 2-5 minutes.** 

You'll see lots of text scrolling - this is normal. Wait until it finishes and you see the prompt again.

### Step 5: Add Your Groq API Key

```powershell
notepad .env
```

Notepad will open. Replace the empty `GROQ_API_KEY=` with your actual key:

```
GROQ_API_KEY=gsk_your_actual_key_here_XXXXXXxxxx
```

Save and close Notepad (Ctrl+S, then close window)

### Step 6: Add PDF Documents

In PowerShell, create the PDFs folder if needed:
```powershell
New-Item -ItemType Directory -Path "data\pdfs" -Force
```

Then copy your PDF files to: `backend\data\pdfs\`

(You can use Windows Explorer to drag & drop PDFs)

### Step 7: Ingest Documents

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
Vector store persisted at: ...
```

**If you get errors:** Don't worry, dependencies are downloading. Just wait and the next command will work.

### Step 8: Start Backend Server

```powershell
py app/main.py
```

You should see:
```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Keep this PowerShell window open.** Do NOT close it.

---

## 🎨 Setup Frontend (New PowerShell Window)

### Step 9: Open NEW PowerShell Window

Click on PowerShell icon or press `Win+X` → PowerShell

### Step 10: Navigate to Frontend

```powershell
cd "c:\Users\Mohamed Thoufiq\OneDrive\Desktop\Shaheen\frontend"
```

### Step 11: Install Frontend Dependencies

```powershell
npm install
```

Wait for completion (1-2 minutes)

### Step 12: Start Frontend Server

```powershell
npm run dev
```

You should see:
```
  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

**Keep this window open too.**

---

## 🎉 Test It!

### Step 13: Open Browser

Open your browser and visit:
```
http://localhost:5173
```

You should see:
- "SWS AI Policy Assistant" title
- Chat input box at bottom
- Empty chat history

### Step 14: Ask a Question

Type in the chat box:
```
What information do we have in the documents?
```

Press Enter or click send button.

Wait 3-5 seconds for the response.

**Success!** 🎊 You should see an AI response.

---

## 🆘 Troubleshooting

### Problem: Backend Window Shows Error

**Error: "ModuleNotFoundError" or "ImportError"**
```
Solution:
1. Make sure venv is activated (you see "(venv)" in prompt)
2. If not, run: venv\Scripts\activate
3. Reinstall: pip install -r app/requirements.txt
4. Run again: py app/main.py
```

**Error: "Port 8000 already in use"**
```
Solution:
1. Close the other backend window if open
2. Or use different port:
   - Edit: backend\app\config.py
   - Change: API_PORT = 8001
   - Restart: py app/main.py
```

### Problem: Frontend Won't Connect

**You see: "Cannot reach server" or "Connection refused"**
```
Solution:
1. Make sure backend window shows "Uvicorn running"
2. Check frontend .env has correct URL:
   - Open: frontend\.env
   - Should contain: VITE_API_URL=http://localhost:8000
3. Restart frontend: npm run dev
4. Refresh browser: F5
```

### Problem: "Groq API Error"

**You see: "API Error" or "invalid API key"**
```
Solution:
1. Get new API key from https://console.groq.com
2. Edit: backend\.env
3. Replace API key: GROQ_API_KEY=gsk_xxx
4. Restart backend: py app/main.py
```

### Problem: No PDF Documents Ingested

**You see: "No documents have been ingested"**
```
Solution:
1. Add PDFs to: backend\data\pdfs\
2. Run: py app/ingest.py
3. Restart backend: py app/main.py
4. Refresh browser
```

### Problem: Import Errors

**You see: "ImportError: cannot import name ..."**
```
Solution:
1. Make sure venv is activated: (venv) in prompt
2. Reinstall everything:
   pip install --upgrade pip
   pip install -r app/requirements.txt --force-reinstall
3. Restart: py app/main.py
```

### Problem: pip install Fails or Takes Forever

```
Solution:
1. Upgrade pip first:
   py -m pip install --upgrade pip
2. Then install:
   pip install -r app/requirements.txt
```

### Problem: "Port 5173 already in use"

```
Solution:
1. Close other frontend windows
2. Or kill the process:
   netstat -ano | findstr :5173
   taskkill /PID xxxxx /F
3. Restart: npm run dev
```

---

## 📊 How to Keep It Running

**Terminal 1 (Always Open):**
```powershell
cd backend
venv\Scripts\activate
py app/main.py
# Shows: INFO: Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 (Always Open):**
```powershell
cd frontend
npm run dev
# Shows: ➜  Local: http://localhost:5173/
```

**Browser:**
```
http://localhost:5173
```

As long as both terminals show no errors, the app is running!

---

## 🔄 Updating Documents

To add new PDFs:

1. Copy PDF files to: `backend\data\pdfs\`
2. In backend terminal, press: `Ctrl+C`
3. Run: `py app/ingest.py`
4. Run: `py app/main.py`
5. In browser, refresh: `F5`

Done! New documents are now searchable.

---

## 🧪 Testing Backend

Open another PowerShell window and run:

```powershell
cd backend
pip install requests
py app/test_backend.py
```

This will test all API endpoints and show you what's working.

---

## 🎯 Quick Reference Commands

| What | Command |
|------|---------|
| Check Python | `py --version` |
| Check Node | `node --version` |
| Go to backend | `cd backend` |
| Go to frontend | `cd frontend` |
| Activate venv | `venv\Scripts\activate` |
| Install deps | `pip install -r app/requirements.txt` |
| Ingest PDFs | `py app/ingest.py` |
| Start backend | `py app/main.py` |
| Start frontend | `npm run dev` |
| Test API | `py app/test_backend.py` |

---

## 📚 Documentation Files

- **This file**: Step-by-step exact setup (YOU ARE HERE)
- [WINDOWS_SETUP.md](WINDOWS_SETUP.md) - Windows-specific guide
- [README.md](README.md) - Project overview
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - General setup guide
- [FAQ_AND_TROUBLESHOOTING.md](FAQ_AND_TROUBLESHOOTING.md) - Q&A
- [backend/README.md](backend/README.md) - Backend details
- [frontend/README.md](frontend/README.md) - Frontend details

---

## ✅ Success Checklist

Before testing, make sure you have:

- [ ] Python 3.9+ installed (`py --version` works)
- [ ] Node.js 16+ installed (`node --version` works)
- [ ] Groq API key obtained and saved
- [ ] Virtual environment created and activated (`(venv)` in prompt)
- [ ] Dependencies installed (`pip install -r app/requirements.txt` succeeded)
- [ ] .env file has your Groq API key
- [ ] PDF files in `backend\data\pdfs\`
- [ ] Ran ingest script (`py app/ingest.py` completed)
- [ ] Backend running (`py app/main.py` shows "Uvicorn running")
- [ ] Frontend running (`npm run dev` shows "Local: http://localhost:5173/")
- [ ] Browser shows http://localhost:5173 correctly
- [ ] Can ask a question and get a response

---

## 🚀 Next Steps

After everything is working:

1. **Test with your documents**
   - Add more PDFs to backend\data\pdfs\
   - Run py app/ingest.py
   - Ask questions about them

2. **Explore the code**
   - Read comments in Python files
   - Understand how RAG works
   - See React components

3. **Customize**
   - Edit prompts in backend\app\prompts.py
   - Change UI styles in frontend\src\App.css
   - Adjust parameters in backend\app\config.py

4. **Share with others**
   - Send them this guide
   - They can follow same steps
   - All will work on Windows

---

## ❓ Questions?

1. **Setup stuck?** → Check [Troubleshooting](#-troubleshooting) section
2. **Need more help?** → Read [FAQ_AND_TROUBLESHOOTING.md](FAQ_AND_TROUBLESHOOTING.md)
3. **Want details?** → Read [WINDOWS_SETUP.md](WINDOWS_SETUP.md) or [README.md](README.md)
4. **Backend issues?** → Check [backend/README.md](backend/README.md)
5. **Frontend issues?** → Check [frontend/README.md](frontend/README.md)

---

## 🎉 Ready to Start?

**Follow Steps 1-14 above in order. It will take about 20-30 minutes total.**

Copy each command exactly as shown and wait for completion before moving to the next step.

**Good luck! You've got this! 🚀**

---

*For Windows users with `py` command*  
*Version: May 2026*  
*Tested on: Python 3.12.10, Node 18.x, Windows 10+*

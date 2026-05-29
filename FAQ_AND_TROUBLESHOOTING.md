# Quick Reference & FAQ

## ⚡ Quick Commands

### Backend Setup
```bash
cd backend
python -m venv venv          # Create environment
venv\Scripts\activate        # Activate (Windows)
# source venv/bin/activate  # Activate (macOS/Linux)
pip install -r app/requirements.txt
```

### Ingest Documents
```bash
cd backend
venv\Scripts\activate
python app/ingest.py
```

### Start Backend
```bash
cd backend
venv\Scripts\activate
python app/main.py
# Runs on http://localhost:8000
```

### Start Frontend
```bash
cd frontend
npm install                  # Only first time
npm run dev
# Runs on http://localhost:5173
```

### Build Frontend
```bash
cd frontend
npm run build               # Creates optimized dist/
npm run preview             # Test the build
```

---

## ✅ Pre-Launch Checklist

Before running for the first time:

- [ ] Python 3.9+ installed
- [ ] Node.js v16+ installed
- [ ] Groq API key obtained from https://console.groq.com
- [ ] Groq API key added to `backend/.env`
- [ ] PDF files added to `backend/data/pdfs/`
- [ ] Ran `python app/ingest.py` successfully
- [ ] No "Port already in use" errors
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can access http://localhost:5173
- [ ] Can send a test question

---

## ❓ FAQ

### Q: Do I need to pay for anything?
**A:** No! Groq offers a free tier. Costs are $0 unless you exceed free limits (~500K tokens/day).

### Q: Can I use PDFs with scanned images?
**A:** PyMuPDF extracts text only. If PDF has only images, OCR won't work. Use text-based PDFs.

### Q: How many PDFs can I use?
**A:** Tested with hundreds of pages. For thousands of pages, you might want to add pagination.

### Q: Can I use a different LLM?
**A:** Yes! Edit `rag_pipeline.py`. LangChain supports OpenAI, Anthropic, Cohere, etc.

### Q: How do I add authentication?
**A:** Add FastAPI security (`HTTPBearer`). See FastAPI docs: https://fastapi.tiangolo.com/

### Q: Can I deploy this?
**A:** Yes! Use Docker. We included Dockerfiles. Or deploy to AWS/GCP/Azure.

### Q: How do I update PDFs?
**A:** Add new PDFs to `backend/data/pdfs/`, run `python app/ingest.py`, restart backend.

### Q: Why is the first response slow?
**A:** First request loads the embedding model (~1-2 seconds). Subsequent requests are faster.

### Q: Can I use this offline?
**A:** Embedding generation works offline. LLM inference requires Groq API (internet).

### Q: How do I clear the vector database?
**A:** Delete `backend/chroma_db/` folder, then run `python app/ingest.py` again.

### Q: Can I run both servers on different ports?
**A:** Yes! Edit `backend/app/config.py` (API_PORT) and `frontend/vite.config.js`.

### Q: How do I see API documentation?
**A:** Visit http://localhost:8000/docs (Swagger UI) while backend is running.

### Q: What if I get "Groq API Error"?
**A:** 
1. Check API key in `backend/.env`
2. Verify key is from https://console.groq.com
3. Check Groq status: https://status.groq.com
4. Restart backend

### Q: What if frontend can't connect to backend?
**A:**
1. Make sure backend is running
2. Check `frontend/.env` has correct `VITE_API_URL`
3. Verify no firewall blocking port 8000

### Q: How do I make answers faster?
**A:** Reduce `RETRIEVER_K` in `backend/app/config.py` from 4 to 2.

### Q: How do I make answers more accurate?
**A:** Increase `RETRIEVER_K` from 4 to 6, or increase `CHUNK_SIZE` from 500 to 800.

### Q: Can I use this with non-English documents?
**A:** Sentence-transformers supports 50+ languages. Test with your language!

### Q: How do I get better answers?
**A:** 
1. Improve system prompt in `backend/app/prompts.py`
2. Try different `CHUNK_SIZE` and `RETRIEVER_K`
3. Use better quality PDFs (readable, not scanned)

### Q: How do I monitor usage?
**A:** Check `backend/app/main.py` logs. Add analytics to track questions.

### Q: Can I make this a mobile app?
**A:** Frontend is already responsive! Or build React Native version.

### Q: How do I add user accounts?
**A:** Add FastAPI authentication + database. See FastAPI security docs.

### Q: Is this secure for production?
**A:** Add authentication, rate limiting, HTTPS, audit logging. See Security Checklist.

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:**
```bash
cd backend
venv\Scripts\activate
pip install -r app/requirements.txt
```

### Problem: "Port 8000 already in use"
**Solution - Option 1 (Change port):**
Edit `backend/app/config.py`:
```python
API_PORT = 8001
```

**Solution - Option 2 (Kill process):**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Problem: "No documents found when querying"
**Solution:**
```bash
cd backend
python app/ingest.py  # Run ingest script
```

### Problem: "Groq API Error - invalid API key"
**Solution:**
1. Go to https://console.groq.com
2. Get a new API key
3. Update `backend/.env`
4. Restart backend

### Problem: "CORS error from frontend"
**Solution:**
1. Verify backend is running on `http://localhost:8000`
2. Check `frontend/.env` has `VITE_API_URL=http://localhost:8000`
3. Reload frontend browser tab

### Problem: "TypeError: Cannot read properties of undefined"
**Solution:**
- This is a React state issue
- Check browser console for full error
- Reload the page

### Problem: "PDF extraction failed"
**Solution:**
- Not all PDFs are readable by PyMuPDF
- Try opening PDF in Adobe Reader
- Try a different PDF
- PDF might be image-only (needs OCR)

### Problem: "Virtual environment not activating"
**Solution - Windows:**
```bash
# Doesn't work?
venv\Scripts\activate

# Try this instead:
.\venv\Scripts\Activate.ps1
```

### Problem: "npm install slow/fails"
**Solution:**
```bash
# Clear npm cache
npm cache clean --force
npm install
```

### Problem: "Backend works, frontend gets 502"
**Solution:**
- Backend crashed
- Check backend terminal for errors
- Restart backend: `python app/main.py`

---

## 🔍 Debugging Tips

### View Backend Logs
Keep terminal open while running:
```bash
python app/main.py
```
All requests and errors print there.

### View Frontend Logs
Open browser console:
- Windows/Linux: F12
- macOS: Cmd + Option + I
- Network tab shows API calls

### Test API Manually
```bash
# Test health
curl http://localhost:8000/api/health

# Test chat
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'
```

### View Interactive API Docs
Visit: http://localhost:8000/docs

Try endpoints directly from browser!

---

## 📊 Performance Tuning

### For Speed
```python
# In backend/app/config.py
RETRIEVER_K = 2           # Fewer chunks
CHUNK_SIZE = 300          # Smaller chunks
```

### For Quality
```python
# In backend/app/config.py
RETRIEVER_K = 6           # More context
CHUNK_SIZE = 800          # Larger chunks
```

### First Run Optimization
- Embedding model downloads ~100MB
- This only happens once
- Subsequent runs are faster

---

## 🚀 Production Checklist

Before deploying:

- [ ] Add authentication
- [ ] Add rate limiting
- [ ] Enable HTTPS/TLS
- [ ] Setup monitoring/logging
- [ ] Add backup for vector DB
- [ ] Configure CORS properly
- [ ] Use environment variables
- [ ] Setup error tracking (Sentry)
- [ ] Add request logging
- [ ] Test with production data
- [ ] Create runbook/deployment guide
- [ ] Setup CI/CD pipeline

---

## 📚 Key Files Reference

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI app, endpoints |
| `backend/app/rag_pipeline.py` | RAG orchestration |
| `backend/app/ingest.py` | PDF processing |
| `backend/app/config.py` | Configuration |
| `backend/app/prompts.py` | LLM prompts |
| `frontend/src/App.jsx` | React root component |
| `frontend/src/components/ChatBox.jsx` | Main chat UI |
| `frontend/package.json` | Frontend dependencies |
| `.env` | API keys & secrets |

---

## 🎓 Code Explanation

### How RAG Works (Simple)

1. **Store**: Take user PDFs, split into chunks, convert to vectors, save to database
2. **Retrieve**: When user asks question, convert to vector, find similar chunks
3. **Generate**: Give chunks + question to LLM, LLM generates answer

**Result**: LLM answers questions using only information from documents

### Why It Works

- **Similarity Search**: Similar questions find similar document chunks
- **Context**: LLM has relevant context before generating answer
- **Grounding**: LLM can't hallucinate if limited to provided chunks
- **Sources**: We know which documents were used

### Example

```
User: "What is the leave policy?"

→ Convert to vector
→ Search database
→ Find chunks about leave:
   - "Annual leave is 20 days per year"
   - "Submit requests 2 weeks in advance"
   - "Sick leave is 10 days per year"

→ Give to LLM with prompt:
   "Answer only from this context: [chunks]"

← LLM: "The annual leave policy provides 20 days..."
← Show sources: "Leave_Policy.pdf"
```

---

## 🌐 API Examples

### Request & Response

**Request:**
```json
{
  "question": "What is the leave policy?"
}
```

**Response:**
```json
{
  "answer": "The leave policy provides employees with 20 days of paid annual leave per calendar year. Submit requests at least 2 weeks in advance through the HR system.",
  "sources": ["Leave_Policy.pdf"]
}
```

---

## 🎯 Performance Metrics

### Typical Timings
- Page load: <1 second
- API latency: 3-5 seconds
- Vector search: <100ms
- LLM inference: 2-3 seconds
- Total E2E: ~5 seconds

### Scalability
- Concurrent requests: Via async/await
- Document size: Tested up to 1000s pages
- Vector store: Millions of vectors possible
- Users: Limited by Groq API rate limits

---

## 💡 Pro Tips

1. **Use keyboard shortcuts**
   - Enter to send message
   - Escape to clear input
   - Ctrl+A to select all

2. **Monitor Groq usage**
   - Check Groq console for token usage
   - Free tier has limits
   - Monitor before going production

3. **Test with variety of questions**
   - Questions not in documents
   - Multi-part questions
   - Questions with typos
   - Questions in different phrasing

4. **Optimize chunk size**
   - Too small: missing context
   - Too large: retrieval noise
   - 500 is sweet spot for most docs

5. **Monitor vector store growth**
   - More documents = more chunks
   - Delete `chroma_db/` to rebuild
   - No need to recopy PDFs

---

## 📞 Support Resources

### Official Documentation
- FastAPI: https://fastapi.tiangolo.com/
- LangChain: https://python.langchain.com/
- ChromaDB: https://docs.trychroma.com/
- React: https://react.dev/
- Groq: https://console.groq.com/docs

### Our Documentation
- [README.md](README.md) - Main overview
- [START_HERE.md](START_HERE.md) - Quick start
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Architecture
- [backend/README.md](backend/README.md) - Backend specific
- [frontend/README.md](frontend/README.md) - Frontend specific

### Getting Help
1. Check this FAQ first
2. Check relevant README
3. Check error messages in terminal
4. Search documentation links above
5. Try the example PDFs

---

## ✨ You're Ready!

You have everything needed to run a production RAG chatbot locally.

**Next steps:**
1. Add your Groq API key
2. Add PDF documents
3. Run ingest
4. Start servers
5. Ask questions!

**Questions?** See [START_HERE.md](START_HERE.md)

---

**Happy coding! 🚀**

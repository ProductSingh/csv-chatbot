# Quick Reference Guide - Offline Changes

## 🚨 Common Issues & Quick Fixes

### Issue: "Units sold by month" not working
**File**: `backend/agent.py`  
**Location**: `group_by_and_aggregate()` function (line ~198)  
**Fix**: 
- Ensure function uses case-insensitive column matching
- Check that `group_column` and `aggregate_column` are correctly identified
- Verify the function returns proper dict structure

### Issue: Session errors ("Session not found" or "already exists")
**File**: `backend/agent.py`  
**Location**: `process_query()` function, session handling (line ~487)  
**Fix**: 
- Check if `get_session()` returns `None` (not exception)
- Ensure session is created if `None`
- Handle "already exists" error gracefully

### Issue: Agent asking too many questions
**File**: `backend/agent.py`  
**Location**: `create_agent()` function, `instruction` variable (line ~260)  
**Fix**: 
- Update instructions to be more proactive
- Add guidance on inferring context from conversation
- Reduce unnecessary follow-up questions

### Issue: Tool not being called
**File**: `backend/agent.py`  
**Location**: Tool function docstrings and agent instructions  
**Fix**: 
- Improve tool function docstrings (they guide the AI)
- Update agent instructions with clear tool usage examples
- Ensure tool is in the tools list returned by `create_dataframe_tools()`

### Issue: API key errors
**File**: `backend/.env`  
**Fix**: 
- Ensure `GOOGLE_API_KEY=your_key` (no quotes, no spaces)
- Restart backend after changing .env
- Verify key is valid at https://makersuite.google.com/app/apikey

### Issue: CORS errors
**File**: `backend/main.py`  
**Location**: CORS middleware (line ~18)  
**Fix**: Add your frontend URL to `allow_origins` list

### Issue: File upload fails
**File**: `frontend/src/App.jsx`  
**Location**: `handleFileUpload()` function  
**Fix**: 
- Check browser console for errors
- Verify `API_BASE_URL` is correct
- Check backend is running

---

## 📍 File Locations for Common Changes

| What to Change | File | Location |
|---------------|------|----------|
| Add new analysis tool | `backend/agent.py` | Inside `create_dataframe_tools()` |
| Change AI model | `backend/agent.py` | `create_agent()` function, `model_name` param |
| Modify agent behavior | `backend/agent.py` | `create_agent()` function, `instruction` variable |
| Add API endpoint | `backend/main.py` | Add new `@app.route()` function |
| Change backend port | `backend/main.py` | `uvicorn.run()` call |
| Change frontend port | `frontend/vite.config.js` | `server.port` |
| Modify upload UI | `frontend/src/components/FileUpload.jsx` | Component JSX |
| Modify chat UI | `frontend/src/components/ChatInterface.jsx` | Component JSX |
| Change styling | `frontend/src/**/*.css` | CSS files |
| Add environment variable | `backend/.env` | Add new line |

---

## 🔍 Debugging Checklist

When something doesn't work:

1. ✅ **Check Backend Logs**
   - Look for Python errors in terminal
   - Check for import errors
   - Verify API key is loaded

2. ✅ **Check Frontend Console**
   - Open browser DevTools (F12)
   - Look for JavaScript errors
   - Check Network tab for failed requests

3. ✅ **Verify Services Running**
   ```bash
   # Check backend
   curl http://localhost:8000/
   
   # Check frontend
   curl http://localhost:3000/
   ```

4. ✅ **Check Environment Variables**
   ```bash
   cd backend
   source venv/bin/activate
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GOOGLE_API_KEY'))"
   ```

5. ✅ **Test Agent Directly**
   ```python
   # In Python shell
   from agent import create_agent
   import pandas as pd
   df = pd.DataFrame({'test': [1,2,3]})
   agent = create_agent(df)
   # Should work without errors
   ```

---

## 🛠 Adding a New Tool (Step-by-Step)

1. **Define the function** in `backend/agent.py`, inside `create_dataframe_tools()`:
   ```python
   def my_new_tool(param: str) -> Dict[str, Any]:
       """Clear description of what the tool does.
       
       Args:
           param: Description of parameter.
       
       Returns:
           dict: Result with status and data.
       """
       try:
           # Your logic here
           result = df[param].some_operation()
           return {
               "status": "success",
               "result": result,
               "message": f"Operation result: {result}"
           }
       except Exception as e:
           return {
               "status": "error",
               "error_message": str(e)
           }
   ```

2. **Wrap with FunctionTool** in the return list:
   ```python
   return [
       # ... existing tools
       FunctionTool(func=my_new_tool),
   ]
   ```

3. **Update agent instructions** in `create_agent()`:
   - Add tool description to the instruction string
   - Explain when to use it

4. **Test it**:
   ```python
   # Test the tool directly
   tools = create_dataframe_tools(df)
   # Find your tool and test it
   ```

---

## 📦 Dependencies

### Backend (`backend/requirements.txt`)
- `fastapi==0.104.1`
- `uvicorn[standard]==0.24.0`
- `pandas==2.1.3`
- `google-adk` (latest)
- `python-dotenv==1.0.0`
- `python-multipart==0.0.6`

### Frontend (`frontend/package.json`)
- `react@^18.2.0`
- `react-dom@^18.2.0`
- `axios@^1.6.2`
- `vite@^5.0.8`
- `@vitejs/plugin-react@^4.2.1`

---

## 🔄 Restart Services

**Backend**:
```bash
# Kill existing
pkill -f "python.*main.py"

# Restart
cd backend
source venv/bin/activate
python main.py
```

**Frontend**:
```bash
# Kill existing (Ctrl+C in terminal)
# Restart
cd frontend
npm run dev
```

---

## 📝 Environment Variables

**Required**:
- `GOOGLE_API_KEY` - Your Google API key

**Location**: `backend/.env`

**Format**:
```
GOOGLE_API_KEY=AIzaSy...your_key_here
```

**Note**: No quotes, no spaces around `=`

---

## 🎯 Testing Queries

Test these to verify everything works:

1. **General**: "What can you help me with?"
2. **Stats**: "What is the mean of [column]?"
3. **Sum**: "Calculate the sum of [column]"
4. **Grouping**: "Show me [metric] by [category]"
5. **Info**: "What are the columns?"

---

**For detailed documentation, see [PROJECT_DOCUMENTATION.md](./PROJECT_DOCUMENTATION.md)**


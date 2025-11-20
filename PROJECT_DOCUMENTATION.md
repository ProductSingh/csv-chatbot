# CSV Chatbot Web App - Project Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Why This Structure?](#why-this-structure)
5. [Key Components](#key-components)
6. [Where to Make Changes](#where-to-make-changes)
7. [Troubleshooting Guide](#troubleshooting-guide)
8. [Deployment](#deployment)

---

## 🎯 Project Overview

This is a **CSV Data Analysis Chatbot** that allows users to:
- Upload CSV files through a web interface
- Ask natural language questions about their data
- Get AI-powered insights using Google's Agent Development Kit (ADK)
- Perform statistical analysis, filtering, grouping, and aggregation operations

The application uses a **React frontend** for the user interface and a **FastAPI backend** with an **AI agent** powered by Google's Gemini model.

---

## 🛠 Tech Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Axios** - HTTP client for API calls
- **CSS3** - Styling (no framework, custom CSS)

### Backend
- **FastAPI** - Python web framework
- **Google ADK (Agent Development Kit)** - AI agent framework
- **Google Gemini 2.0 Flash** - LLM model
- **Pandas** - Data manipulation and analysis
- **Uvicorn** - ASGI server
- **Python-dotenv** - Environment variable management

### Development Tools
- **Node.js & npm** - Frontend package management
- **Python 3.8+** - Backend runtime
- **Git** - Version control

---

## 📁 Project Structure

```
Uptio Project/
├── backend/                    # Python FastAPI backend
│   ├── main.py                # FastAPI application & API endpoints
│   ├── agent.py               # AI agent with ADK integration & tools
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables (API keys) - NOT in git
│   └── venv/                  # Python virtual environment - NOT in git
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.jsx      # CSV file upload component
│   │   │   ├── FileUpload.css      # Upload component styles
│   │   │   ├── ChatInterface.jsx   # Chat UI component
│   │   │   └── ChatInterface.css   # Chat component styles
│   │   ├── App.jsx            # Main application component
│   │   ├── App.css            # Main app styles
│   │   ├── main.jsx           # React entry point
│   │   └── index.css          # Global styles
│   ├── index.html             # HTML template
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite configuration
│   └── node_modules/          # Node packages - NOT in git
│
├── .gitignore                 # Git ignore rules
├── .env.example               # Example environment file
├── README.md                  # Quick start guide
└── PROJECT_DOCUMENTATION.md   # This file - comprehensive documentation
```

---

## 🤔 Why This Structure?

### Separation of Concerns
- **Frontend/Backend Split**: Clear separation allows independent development and deployment
- **Component-Based Frontend**: React components are modular and reusable
- **Service Layer**: Backend API is separate from business logic (agent)

### Scalability
- **Modular Tools**: Each dataframe operation is a separate tool function
- **Session Management**: Sessions are stored in memory (can be moved to database)
- **Agent Architecture**: ADK allows easy addition of new tools and capabilities

### Maintainability
- **Clear File Organization**: Easy to find and modify specific features
- **Configuration Files**: Dependencies and settings are clearly defined
- **Documentation**: Comprehensive docs for future developers

---

## 🔧 Key Components

### Backend Components

#### `backend/main.py`
**Purpose**: FastAPI application with API endpoints

**Key Functions**:
- `POST /upload` - Handles CSV file uploads
- `POST /query` - Processes user queries through the AI agent
- `GET /session/{session_id}/info` - Returns session information

**Where to Modify**:
- Add new API endpoints
- Change CORS settings
- Modify error handling
- Add authentication/authorization

#### `backend/agent.py`
**Purpose**: AI agent implementation using Google ADK

**Key Functions**:
- `create_agent()` - Creates ADK Agent with tools
- `create_dataframe_tools()` - Defines tool functions for data analysis
- `process_query()` - Executes queries using the agent
- Tool functions: `calculate_mean`, `sum_column`, `group_by_and_aggregate`, etc.

**Where to Modify**:
- Add new analysis tools (new functions in `create_dataframe_tools`)
- Modify agent instructions (in `create_agent`)
- Change model settings (model name, temperature)
- Add new tool types (filtering, transformations)

### Frontend Components

#### `frontend/src/App.jsx`
**Purpose**: Main application component, manages state

**Key State**:
- `sessionId` - Current session ID
- `fileInfo` - Uploaded file information
- `isLoading` - Loading state

**Where to Modify**:
- Add new features/state management
- Modify file upload flow
- Add new UI sections

#### `frontend/src/components/FileUpload.jsx`
**Purpose**: Handles CSV file upload UI

**Features**:
- Drag & drop file upload
- File validation
- File information display
- Remove/reupload functionality

**Where to Modify**:
- Change upload UI/UX
- Add file type validation
- Modify file preview display

#### `frontend/src/components/ChatInterface.jsx`
**Purpose**: Chat interface for user queries

**Features**:
- Message display
- Query input
- Example questions
- Loading states

**Where to Modify**:
- Change chat UI design
- Add message history features
- Modify example questions
- Add export functionality

---

## 🔨 Where to Make Changes

### Common Modifications

#### 1. **Add a New Data Analysis Tool**

**File**: `backend/agent.py`

**Location**: Inside `create_dataframe_tools()` function

**Example**:
```python
def calculate_variance(column: str) -> Dict[str, Any]:
    """Calculate variance of a numeric column."""
    try:
        variance = float(df[column].var())
        return {
            "status": "success",
            "result": variance,
            "message": f"Variance of {column}: {variance:.2f}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error calculating variance: {str(e)}"
        }

# Then add to return list:
return [
    # ... existing tools
    FunctionTool(func=calculate_variance),
]
```

**Also Update**: Agent instructions in `create_agent()` to mention the new tool

---

#### 2. **Change AI Model**

**File**: `backend/agent.py`

**Location**: `create_agent()` function, `model_name` parameter

**Current**: `model_name: str = "gemini-2.0-flash"`

**Options**: 
- `"gemini-2.0-flash-exp"` (experimental)
- `"gemini-1.5-pro"` (more capable, slower)
- `"gemini-1.5-flash"` (faster)

---

#### 3. **Modify Agent Instructions/Behavior**

**File**: `backend/agent.py`

**Location**: `create_agent()` function, `instruction` variable

**What to Change**:
- System prompts
- Tool usage guidelines
- Response formatting rules
- Guardrails and restrictions

---

#### 4. **Add New API Endpoint**

**File**: `backend/main.py`

**Example**:
```python
@app.post("/export")
async def export_data(session_id: str, format: str = "csv"):
    """Export session data"""
    if session_id not in dataframes:
        raise HTTPException(status_code=404, detail="Session not found")
    
    df = dataframes[session_id]
    # ... export logic
    return JSONResponse({"status": "success", "data": ...})
```

---

#### 5. **Change Frontend Styling**

**Files**: 
- `frontend/src/App.css` - Main app styles
- `frontend/src/components/FileUpload.css` - Upload component
- `frontend/src/components/ChatInterface.css` - Chat component
- `frontend/src/index.css` - Global styles

**Where**: Modify CSS classes and styles directly

---

#### 6. **Fix Session/Context Issues**

**File**: `backend/agent.py`

**Location**: `process_query()` function, session handling section

**Common Issues**:
- Session not found → Check session creation logic
- Conversation context lost → Verify session_id is passed correctly
- "Already exists" error → Check session existence before creation

---

#### 7. **Change Port Numbers**

**Backend**: `backend/main.py`
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change 8000
```

**Frontend**: `frontend/vite.config.js`
```javascript
server: {
  port: 3000,  // Change 3000
}
```

**Also Update**: CORS origins in `backend/main.py` if needed

---

#### 8. **Add Environment Variables**

**File**: `backend/.env`

**Add new variables**:
```
GOOGLE_API_KEY=your_key
NEW_VARIABLE=value
```

**Load in code**: `backend/agent.py` or `backend/main.py`
```python
from dotenv import load_dotenv
import os
load_dotenv()
new_var = os.getenv("NEW_VARIABLE")
```

---

## 🐛 Troubleshooting Guide

### Backend Issues

#### **Error: "GOOGLE_API_KEY environment variable is not set"**
- **Location**: `backend/.env`
- **Fix**: Create `.env` file with `GOOGLE_API_KEY=your_key`
- **Check**: Ensure `.env` is in `backend/` directory

#### **Error: "Session not found" or "Session already exists"**
- **Location**: `backend/agent.py`, `process_query()` function
- **Fix**: Check session creation logic (lines ~487-523)
- **Debug**: Add logging to see session_id being used

#### **Error: "Module not found" or Import errors**
- **Location**: `backend/requirements.txt`
- **Fix**: 
  ```bash
  cd backend
  source venv/bin/activate
  pip install -r requirements.txt
  ```

#### **Error: "Port already in use"**
- **Location**: `backend/main.py`
- **Fix**: Change port number or kill existing process
  ```bash
  lsof -ti:8000 | xargs kill -9
  ```

#### **Error: Tool function not working**
- **Location**: `backend/agent.py`, tool function definitions
- **Fix**: 
  - Check function signature matches docstring
  - Verify column names exist in dataframe
  - Check error handling in tool function
  - Review agent instructions for tool usage

---

### Frontend Issues

#### **Error: "Cannot connect to backend" or CORS errors**
- **Location**: `backend/main.py`, CORS middleware
- **Fix**: Add your frontend URL to `allow_origins`:
  ```python
  allow_origins=["http://localhost:3000", "http://localhost:5173", "your_url"]
  ```

#### **Error: "File upload fails"**
- **Location**: `frontend/src/App.jsx`, `handleFileUpload()`
- **Fix**: 
  - Check browser console for errors
  - Verify backend is running
  - Check file size limits
  - Verify API_BASE_URL is correct

#### **Error: "Component not rendering"**
- **Location**: React component files
- **Fix**: 
  - Check browser console for React errors
  - Verify all imports are correct
  - Check component props are passed correctly

#### **Error: "npm install fails"**
- **Location**: `frontend/package.json`
- **Fix**: 
  ```bash
  cd frontend
  rm -rf node_modules package-lock.json
  npm install
  ```

---

### Agent/AI Issues

#### **Error: "API key not valid"**
- **Location**: `backend/.env`
- **Fix**: 
  - Verify API key is correct (no quotes, no spaces)
  - Get new key from [Google AI Studio](https://makersuite.google.com/app/apikey)
  - Restart backend server after changing .env

#### **Error: "Tool not being called" or "Wrong tool selected"**
- **Location**: `backend/agent.py`, agent instructions
- **Fix**: 
  - Improve tool descriptions in function docstrings
  - Update agent instructions with clearer tool usage guidelines
  - Add examples in instructions

#### **Error: "Empty response" or "No data returned"**
- **Location**: `backend/agent.py`, `process_query()` function
- **Fix**: 
  - Check event handling logic (lines ~525-550)
  - Verify response extraction from ADK events
  - Add logging to see what events are received

---

## 🚀 Deployment

### Local Development

1. **Backend**:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   # Create .env with GOOGLE_API_KEY
   python main.py
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Production Deployment

#### Backend (FastAPI)
- Use **Gunicorn** or **Uvicorn** with multiple workers
- Set up **reverse proxy** (Nginx)
- Use **environment variables** for secrets
- Consider **Docker** containerization

#### Frontend (React)
- Build: `npm run build`
- Serve with **Nginx** or **CDN**
- Update API_BASE_URL to production backend URL

---

## 📝 Important Notes

### Security
- **Never commit** `.env` files to git
- **Never commit** API keys
- Use environment variables for all secrets
- Consider adding authentication for production

### Performance
- Current implementation stores dataframes in memory
- For production, consider database storage
- Session service is in-memory (consider persistent storage)
- Add rate limiting for API endpoints

### Limitations
- File size: No explicit limit (add if needed)
- Concurrent users: Limited by memory
- Session persistence: Lost on server restart
- No user authentication: Add for production

---

## 🔗 Useful Links

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Google AI Studio](https://makersuite.google.com/app/apikey)

---

## 📞 Support

If you encounter issues:
1. Check this documentation
2. Review error messages in console/logs
3. Check GitHub issues (if repository exists)
4. Review code comments in relevant files

---

**Last Updated**: 2025-01-27
**Version**: 1.0.0


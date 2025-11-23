from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import io
import os
from typing import Optional, List
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import pickle
import gzip
from agent import create_agent, process_query
from database import init_db, get_db, ChatSession, ChatMessage, engine

# Load environment variables
load_dotenv()

app = FastAPI(title="CSV Chatbot API")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on application startup"""
    init_db()
    print("✓ CSV Chatbot API started with PostgreSQL database")

# CORS middleware to allow React frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3003", "http://localhost:3004", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:3003", "http://127.0.0.1:3004", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    session_id: str
    query: str

class MessageResponse(BaseModel):
    id: str
    message_type: str
    content: str
    created_at: str

class ChatSessionResponse(BaseModel):
    id: str
    filename: str
    metadata: dict
    created_at: str
    messages: List[MessageResponse]

@app.get("/")
async def root():
    return {"message": "CSV Chatbot API is running", "database": "PostgreSQL"}

def serialize_dataframe(df: pd.DataFrame) -> bytes:
    """
    Serialize a DataFrame to bytes using pickle and compress with gzip
    This allows storing DataFrames in PostgreSQL
    """
    return gzip.compress(pickle.dumps(df))

def deserialize_dataframe(data: bytes) -> pd.DataFrame:
    """
    Deserialize a DataFrame from compressed pickle bytes
    """
    return pickle.loads(gzip.decompress(data))

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), session_id: str = None, db: Session = Depends(get_db)):
    """Upload a CSV file and store it in PostgreSQL with metadata"""
    try:
        # Generate session_id if not provided
        if not session_id:
            import uuid
            session_id = str(uuid.uuid4())
        
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        # Read file contents
        contents = await file.read()
        
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Parse CSV
        try:
            df = pd.read_csv(io.BytesIO(contents))
        except Exception as csv_error:
            raise HTTPException(status_code=400, detail=f"Invalid CSV file: {str(csv_error)}")
        
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file contains no data")
        
        # Prepare metadata
        metadata = {
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
        }
        
        # Serialize DataFrame for storage
        csv_data = serialize_dataframe(df)
        
        # Check if session already exists (update) or create new
        existing_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        
        if existing_session:
            # Update existing session
            existing_session.csv_data = csv_data
            existing_session.csv_metadata = metadata
            existing_session.filename = file.filename
        else:
            # Create new session
            chat_session = ChatSession(
                id=session_id,
                filename=file.filename,
                csv_data=csv_data,
                csv_metadata=metadata
            )
            db.add(chat_session)
        
        db.commit()
        
        return JSONResponse({
            "session_id": session_id,
            "message": "File uploaded successfully",
            "rows": len(df),
            "columns": list(df.columns),
            "preview": df.head().to_dict('records'),
            "storage": "PostgreSQL"
        })
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/query")
async def query_data(request: QueryRequest, db: Session = Depends(get_db)):
    """Process a query about the uploaded CSV data and save to chat history"""
    try:
        # Get session from database
        session = db.query(ChatSession).filter(ChatSession.id == request.session_id).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="No data found for this session. Please upload a CSV file first.")
        
        # Deserialize DataFrame
        df = deserialize_dataframe(session.csv_data)
        
        # Save user message to database
        user_message = ChatMessage(
            session_id=request.session_id,
            message_type="user",
            content=request.query
        )
        db.add(user_message)
        db.commit()
        
        try:
            # Create agent with the dataframe
            agent = create_agent(df)
            
            # Process the query with session_id to maintain conversation context
            response = await process_query(agent, request.query, df, session_id=request.session_id)
            
            # Save assistant response to database
            assistant_message = ChatMessage(
                session_id=request.session_id,
                message_type="assistant",
                content=response
            )
            db.add(assistant_message)
            db.commit()
            
            return JSONResponse({
                "session_id": request.session_id,
                "query": request.query,
                "response": response,
                "storage": "PostgreSQL"
            })
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/session/{session_id}/info")
async def get_session_info(session_id: str, db: Session = Depends(get_db)):
    """Get information about the uploaded CSV and chat history"""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get chat messages
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).all()
    
    return JSONResponse({
        "session_id": session.id,
        "filename": session.filename,
        "rows": session.csv_metadata.get("rows") if session.csv_metadata else 0,
        "columns": session.csv_metadata.get("columns") if session.csv_metadata else [],
        "dtypes": session.csv_metadata.get("dtypes") if session.csv_metadata else {},
        "message_count": len(messages),
        "created_at": session.created_at.isoformat() if session.created_at else None,
        "storage": "PostgreSQL"
    })

@app.get("/session/{session_id}/messages")
async def get_chat_messages(session_id: str, db: Session = Depends(get_db)):
    """Get all messages for a chat session"""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()
    
    return JSONResponse({
        "session_id": session_id,
        "messages": [msg.to_dict() for msg in messages]
    })

@app.get("/sessions")
async def list_sessions(db: Session = Depends(get_db)):
    """List all chat sessions for a user"""
    sessions = db.query(ChatSession).order_by(ChatSession.created_at.desc()).all()
    
    return JSONResponse({
        "sessions": [session.to_dict() for session in sessions]
    })

@app.delete("/session/{session_id}")
async def delete_session(session_id: str, db: Session = Depends(get_db)):
    """Delete a chat session and all its messages"""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        db.delete(session)
        db.commit()
        return JSONResponse({"message": "Session deleted successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


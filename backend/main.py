from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import io
import os
from typing import Optional
from dotenv import load_dotenv
from agent import create_agent, process_query

# Load environment variables
load_dotenv()

app = FastAPI(title="CSV Chatbot API")

# CORS middleware to allow React frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Store uploaded dataframes in memory (in production, use a proper storage solution)
dataframes = {}

class QueryRequest(BaseModel):
    session_id: str
    query: str

@app.get("/")
async def root():
    return {"message": "CSV Chatbot API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), session_id: str = None):
    """Upload a CSV file and store it as a dataframe"""
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
        
        # Store dataframe
        dataframes[session_id] = df
        
        return JSONResponse({
            "session_id": session_id,
            "message": "File uploaded successfully",
            "rows": len(df),
            "columns": list(df.columns),
            "preview": df.head().to_dict('records')
        })
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/query")
async def query_data(request: QueryRequest):
    """Process a query about the uploaded CSV data"""
    if request.session_id not in dataframes:
        raise HTTPException(status_code=404, detail="No data found for this session. Please upload a CSV file first.")
    
    df = dataframes[request.session_id]
    
    try:
        # Create agent with the dataframe
        agent = create_agent(df)
        
        # Process the query with session_id to maintain conversation context
        response = await process_query(agent, request.query, df, session_id=request.session_id)
        
        return JSONResponse({
            "session_id": request.session_id,
            "query": request.query,
            "response": response
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/session/{session_id}/info")
async def get_session_info(session_id: str):
    """Get information about the uploaded CSV"""
    if session_id not in dataframes:
        raise HTTPException(status_code=404, detail="Session not found")
    
    df = dataframes[session_id]
    return JSONResponse({
        "session_id": session_id,
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "preview": df.head().to_dict('records')
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


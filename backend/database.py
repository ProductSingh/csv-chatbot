"""
Database configuration and models for CSV Chatbot
"""
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, LargeBinary, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv
from datetime import datetime
import uuid

load_dotenv()

# Database URL configuration
# Format: postgresql://username:password@localhost:5432/database_name
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/csv_chatbot"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600  # Recycle connections after 1 hour
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class ChatSession(Base):
    """
    Represents a chat session with an uploaded CSV file
    """
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True, default="default_user")  # For multi-user support later
    filename = Column(String, nullable=False)
    
    # Store CSV data as binary (can be pickled or compressed)
    csv_data = Column(LargeBinary, nullable=False)
    
    # Store CSV metadata as JSON
    csv_metadata = Column(JSON, nullable=True)  # {rows: int, columns: list, dtypes: dict}
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship to messages
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "metadata": self.csv_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "message_count": len(self.messages)
        }


class ChatMessage(Base):
    """
    Represents a message in a chat session (query or response)
    """
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("chat_sessions.id"), nullable=False)
    
    # Message type: 'user' or 'assistant'
    message_type = Column(String, nullable=False)  # 'user' or 'assistant'
    
    # Message content
    content = Column(Text, nullable=False)
    
    # Additional metadata
    message_metadata = Column(JSON, nullable=True)  # Can store token count, latency, etc.
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationship to session
    session = relationship("ChatSession", back_populates="messages")
    
    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "message_type": self.message_type,
            "content": self.content,
            "metadata": self.message_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


def get_db():
    """
    Dependency to get database session for FastAPI endpoints
    Usage: async def endpoint(db: Session = Depends(get_db))
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables
    Call this once on application startup
    """
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")


def drop_all_tables():
    """
    Drop all tables (use with caution - for development/testing only)
    """
    Base.metadata.drop_all(bind=engine)
    print("✓ All database tables dropped")

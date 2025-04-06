from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base

class SentimentPrediction(Base):
    """
    Database model for storing sentiment predictions
    """
    __tablename__ = "sentiment_predictions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=False)
    sentiment = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    source = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SentimentHistory(Base):
    __tablename__ = "sentiment_history"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    cleaned_text = Column(Text)
    sentiment = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    probabilities = Column(JSON)
    language = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # เพิ่มฟิลด์เหล่านี้ใน migration แทน แต่ไม่ใช้ในโมเดลเพื่อให้ทำงานได้กับข้อมูลเดิม
    # ฟิลด์เหล่านี้จะถูกเพิ่มโดย migration script
    """
    user_id = Column(String(100), nullable=True, index=True)
    user_name = Column(String(200), nullable=True)
    platform = Column(String(20), nullable=True, index=True)
    group_id = Column(String(100), nullable=True, index=True)
    group_name = Column(String(200), nullable=True)
    """
    
    def __repr__(self):
        return f"<SentimentHistory(id={self.id}, sentiment={self.sentiment}, confidence={self.confidence})>"
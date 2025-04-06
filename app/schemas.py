from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class SentimentRequest(BaseModel):
    """
    Request schema for sentiment prediction
    """
    text: str = Field(..., description="Text to analyze", min_length=1)
    source: Optional[str] = Field(None, description="Source of the text")

class SentimentResponse(BaseModel):
    """
    Response schema for sentiment prediction
    """
    text: str
    sentiment: str
    confidence: float
    probabilities: Dict[str, float]
    prediction_id: int

class SentimentHistoryBase(BaseModel):
    text: str
    cleaned_text: Optional[str] = None
    sentiment: str
    confidence: float
    probabilities: Dict[str, float]
    language: Optional[str] = None

class SentimentHistoryCreate(SentimentHistoryBase):
    pass

class SentimentHistory(SentimentHistoryBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class SentimentStats(BaseModel):
    positive_count: int
    neutral_count: int
    negative_count: int
    positive_percent: float
    neutral_percent: float
    negative_percent: float
    thai_count: int
    english_count: int
    mixed_count: int
    thai_percent: float
    english_percent: float
    mixed_percent: float
    total_count: int

class HistoricalPrediction(BaseModel):
    """
    Schema for historical prediction data
    """
    id: int
    text: str
    sentiment: str
    confidence: float
    created_at: datetime
    
    class Config:
        orm_mode = True

class StatsResponse(BaseModel):
    """
    Schema for statistics response
    """
    total_predictions: int
    sentiment_distribution: Dict[str, int]
    recent_predictions: List[HistoricalPrediction]
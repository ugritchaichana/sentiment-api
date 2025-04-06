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
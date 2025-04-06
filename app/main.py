# app/main.py (simplified version)
from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List, Any
import app.utils as utils  # แก้ไขการ import ให้เหมาะสมกับโครงสร้างไฟล์
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import json
import os
from datetime import datetime

from app.database import get_db, engine
from app.models import Base, SentimentHistory
from app.schemas import SentimentRequest, SentimentResponse

# ตรวจสอบว่ามีการกำหนดค่า integration หรือไม่
ENABLE_LINE_INTEGRATION = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "") != ""
ENABLE_DISCORD_INTEGRATION = os.getenv("DISCORD_BOT_TOKEN", "") != ""

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Thai-English Sentiment Analysis API",
    description="Simple API for sentiment analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ในการใช้งานจริงควรระบุ domains ที่อนุญาตเท่านั้น
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# เพิ่ม integrations ถ้ามีการเปิดใช้งาน
if ENABLE_LINE_INTEGRATION:
    from app.integrations.line_webhook import router as line_router
    app.include_router(line_router, tags=["integrations"])
    print("Line integration enabled")

if ENABLE_DISCORD_INTEGRATION:
    from app.integrations.discord_webhook import router as discord_router
    app.include_router(discord_router, tags=["integrations"])
    print("Discord integration enabled")

# Jinja2 filter for formatting datetime
def format_datetime(value):
    if value:
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return ""

templates.env.filters["format_datetime"] = format_datetime

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "active_page": "home"})

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request, db: Session = Depends(get_db)):
    # Get sentiment counts
    sentiment_counts = db.query(
        SentimentHistory.sentiment, 
        func.count(SentimentHistory.id).label("count")
    ).group_by(SentimentHistory.sentiment).all()
    
    positive_count = 0
    neutral_count = 0
    negative_count = 0
    
    for sentiment, count in sentiment_counts:
        if sentiment == "Positive":
            positive_count = count
        elif sentiment == "Neutral":
            neutral_count = count
        elif sentiment == "Negative":
            negative_count = count
    
    total_count = positive_count + neutral_count + negative_count
    
    # Get language counts
    language_counts = db.query(
        SentimentHistory.language, 
        func.count(SentimentHistory.id).label("count")
    ).group_by(SentimentHistory.language).all()
    
    thai_count = 0
    english_count = 0
    mixed_count = 0
    
    for language, count in language_counts:
        if language == "thai":
            thai_count = count
        elif language == "english":
            english_count = count
        elif language == "mixed":
            mixed_count = count
    
    # Calculate percentages
    # Avoid division by zero
    if total_count > 0:
        positive_percent = round((positive_count / total_count) * 100, 1)
        neutral_percent = round((neutral_count / total_count) * 100, 1)
        negative_percent = round((negative_count / total_count) * 100, 1)
        
        language_total = thai_count + english_count + mixed_count
        thai_percent = round((thai_count / language_total) * 100, 1) if language_total > 0 else 0
        english_percent = round((english_count / language_total) * 100, 1) if language_total > 0 else 0
        mixed_percent = round((mixed_count / language_total) * 100, 1) if language_total > 0 else 0
    else:
        positive_percent = neutral_percent = negative_percent = 0
        thai_percent = english_percent = mixed_percent = 0
    
    # Get recent history
    recent_history = db.query(SentimentHistory).order_by(desc(SentimentHistory.created_at)).limit(5).all()
    
    stats = {
        "positive_count": positive_count,
        "neutral_count": neutral_count,
        "negative_count": negative_count,
        "positive_percent": positive_percent,
        "neutral_percent": neutral_percent,
        "negative_percent": negative_percent,
        "thai_count": thai_count,
        "english_count": english_count,
        "mixed_count": mixed_count,
        "thai_percent": thai_percent,
        "english_percent": english_percent,
        "mixed_percent": mixed_percent,
        "total_count": total_count
    }
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "active_page": "dashboard",
        "stats": stats,
        "recent_history": recent_history
    })

@app.get("/history", response_class=HTMLResponse)
async def get_history(request: Request, db: Session = Depends(get_db)):
    total = db.query(func.count(SentimentHistory.id)).scalar()
    
    # First page of history
    page = 1
    per_page = 10
    history_items = db.query(SentimentHistory).order_by(desc(SentimentHistory.created_at)).offset((page-1)*per_page).limit(per_page).all()
    
    pages = (total + per_page - 1) // per_page  # ceiling division
    
    return templates.TemplateResponse("history.html", {
        "request": request, 
        "active_page": "history",
        "history_items": history_items,
        "total": total,
        "page": page,
        "pages": pages
    })

@app.get("/history-partial", response_class=HTMLResponse)
async def get_history_partial(
    request: Request, 
    page: int = 1,
    db: Session = Depends(get_db)
):
    per_page = 10
    total = db.query(func.count(SentimentHistory.id)).scalar()
    pages = (total + per_page - 1) // per_page  # ceiling division
    
    history_items = db.query(SentimentHistory).order_by(desc(SentimentHistory.created_at)).offset((page-1)*per_page).limit(per_page).all()
    
    return templates.TemplateResponse("partials/history_table.html", {
        "request": request,
        "history_items": history_items,
        "total": total,
        "page": page,
        "pages": pages
    })

@app.get("/history/{history_id}", response_class=HTMLResponse)
async def get_history_details(history_id: int, request: Request, db: Session = Depends(get_db)):
    history = db.query(SentimentHistory).filter(SentimentHistory.id == history_id).first()
    
    if not history:
        raise HTTPException(status_code=404, detail="History record not found")
    
    return templates.TemplateResponse("partials/history_details.html", {
        "request": request,
        "history": history
    })

@app.get("/api-tester", response_class=HTMLResponse)
async def get_api_tester(request: Request):
    return templates.TemplateResponse("api_tester.html", {"request": request, "active_page": "api-tester"})

@app.post("/test-sentiment", response_class=HTMLResponse)
async def test_sentiment(request: Request, text: str = Form(...), db: Session = Depends(get_db)):
    prediction_result = utils.predict_sentiment(text)
    
    # Save to history
    history = SentimentHistory(
        text=text,
        cleaned_text=prediction_result.get("cleaned_text", ""),
        sentiment=prediction_result["sentiment"],
        confidence=prediction_result["confidence"],
        probabilities=prediction_result["probabilities"],
        language=prediction_result.get("language", "")
    )
    
    db.add(history)
    db.commit()
    db.refresh(history)
    
    # Format JSON for display
    result_json = json.dumps({
        "text": prediction_result["text"],
        "sentiment": prediction_result["sentiment"],
        "confidence": prediction_result["confidence"],
        "probabilities": prediction_result["probabilities"]
    }, indent=2)
    
    return templates.TemplateResponse("partials/sentiment_result.html", {
        "request": request,
        "result": prediction_result,
        "result_json": result_json
    })

@app.post("/predict", response_model=SentimentResponse)
def predict_sentiment(request: SentimentRequest, db: Session = Depends(get_db)):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    prediction_result = utils.predict_sentiment(request.text)
    
    # Save to history
    history = SentimentHistory(
        text=request.text,
        cleaned_text=prediction_result.get("cleaned_text", ""),
        sentiment=prediction_result["sentiment"],
        confidence=prediction_result["confidence"],
        probabilities=prediction_result["probabilities"],
        language=prediction_result.get("language", "")
    )
    
    db.add(history)
    db.commit()
    
    return {
        "text": prediction_result["text"],
        "sentiment": prediction_result["sentiment"],
        "confidence": prediction_result["confidence"],
        "probabilities": prediction_result["probabilities"]
    }

# เพิ่ม health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": app.version}
import os
from fastapi import APIRouter, Request, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import httpx
import json

from app.database import get_db
from app.models import SentimentHistory
import app.utils as utils

router = APIRouter()

# กำหนดค่า Line API
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_API_URL = "https://api.line.me/v2/bot/message/reply"

@router.post("/webhook/line")
async def line_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_line_signature: str = Header(None)
):
    """
    Line Messaging API webhook
    
    รับข้อความจาก Line และวิเคราะห์ความรู้สึก
    """
    # ตรวจสอบว่าได้กำหนดค่า Line API หรือไม่
    if not LINE_CHANNEL_SECRET or not LINE_CHANNEL_ACCESS_TOKEN:
        return {"status": "not_configured"}
    
    # อ่านข้อมูลจาก request
    payload = await request.json()
    events = payload.get("events", [])
    
    for event in events:
        # ประมวลผลเฉพาะข้อความข้อความ
        if event["type"] == "message" and event["message"]["type"] == "text":
            message_text = event["message"]["text"]
            reply_token = event["replyToken"]
            
            # ข้อมูลผู้ส่ง
            source_type = event["source"]["type"]  # user, group, room
            user_id = event["source"].get("userId")
            
            # ข้อมูลกลุ่ม (ถ้ามี)
            group_id = None
            group_name = None
            
            if source_type == "group":
                group_id = event["source"].get("groupId")
                # ไม่สามารถดึงชื่อกลุ่มได้โดยตรง ต้องใช้ Group API
            elif source_type == "room":
                group_id = event["source"].get("roomId")
            
            # วิเคราะห์ความรู้สึก
            result = utils.predict_sentiment(message_text)
            
            # บันทึกลงฐานข้อมูล
            history = SentimentHistory(
                text=message_text,
                cleaned_text=result.get("cleaned_text", ""),
                sentiment=result["sentiment"],
                confidence=result["confidence"],
                probabilities=result["probabilities"],
                language=result.get("language", ""),
                user_id=user_id,
                platform="line",
                group_id=group_id,
                group_name=group_name
            )
            
            db.add(history)
            db.commit()
            
            # ตอบกลับไปยัง Line (ตัวอย่าง)
            try:
                await reply_line_message(reply_token, f"ความรู้สึก: {result['sentiment']} (ความมั่นใจ {result['confidence']:.1f}%)")
            except Exception as e:
                print(f"Error replying to Line: {str(e)}")
    
    return {"status": "success"}

async def reply_line_message(reply_token, message_text):
    """ส่งข้อความตอบกลับไปยัง Line"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    
    data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": message_text
            }
        ]
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            LINE_API_URL,
            headers=headers,
            json=data,
        )
        
        if response.status_code != 200:
            raise Exception(f"Error from Line API: {response.text}") 
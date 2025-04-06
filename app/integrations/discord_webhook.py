import os
import json
from fastapi import APIRouter, Request, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import httpx

from app.database import get_db
from app.models import SentimentHistory
import app.utils as utils

router = APIRouter()

# กำหนดค่า Discord API
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
DISCORD_API_URL = "https://discord.com/api/v10"

@router.post("/webhook/discord")
async def discord_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_signature_ed25519: str = Header(None),
    x_signature_timestamp: str = Header(None)
):
    """
    Discord webhook
    
    รับข้อความจาก Discord และวิเคราะห์ความรู้สึก
    """
    # ตรวจสอบว่าได้กำหนดค่า Discord API หรือไม่
    if not DISCORD_BOT_TOKEN:
        return {"status": "not_configured"}
    
    # อ่านข้อมูลจาก request
    payload = await request.json()
    
    # ตรวจสอบว่าเป็น ping จาก Discord
    if payload.get("type") == 1:  # PING
        return {"type": 1}  # PONG
    
    # ตรวจสอบว่าเป็นข้อความหรือไม่
    if payload.get("type") != 2:  # APPLICATION_COMMAND
        return {"status": "ignored"}
    
    # รับข้อมูลจาก payload
    try:
        data = payload.get("data", {})
        command_name = data.get("name")
        
        # รองรับเฉพาะคำสั่ง sentiment
        if command_name != "sentiment":
            return {"status": "unknown_command"}
        
        # รับข้อความที่ต้องการวิเคราะห์
        options = data.get("options", [])
        message_text = next((option["value"] for option in options if option["name"] == "text"), None)
        
        if not message_text:
            return {"status": "no_text"}
        
        # ข้อมูลผู้ใช้
        user_id = payload.get("member", {}).get("user", {}).get("id")
        user_name = payload.get("member", {}).get("user", {}).get("username")
        
        # ข้อมูลกลุ่ม
        guild_id = payload.get("guild_id")
        channel_id = payload.get("channel_id")
        
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
            user_name=user_name,
            platform="discord",
            group_id=guild_id
        )
        
        db.add(history)
        db.commit()
        
        # ตอบกลับไปยัง Discord
        response_text = f"ความรู้สึก: {result['sentiment']} (ความมั่นใจ {result['confidence']:.1f}%)"
        
        return {
            "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE
            "data": {
                "content": response_text,
                "flags": 64  # EPHEMERAL - เห็นเฉพาะผู้ใช้ที่ส่งคำสั่ง
            }
        }
    
    except Exception as e:
        print(f"Error processing Discord command: {str(e)}")
        return {
            "type": 4,
            "data": {
                "content": f"เกิดข้อผิดพลาด: {str(e)}",
                "flags": 64
            }
        }

# สร้างคำสั่ง Discord (ต้องรันแยกต่างหาก)
async def register_discord_commands():
    """ลงทะเบียนคำสั่ง slash command กับ Discord"""
    if not DISCORD_BOT_TOKEN:
        print("Discord bot token not configured")
        return
    
    application_id = os.getenv("DISCORD_APPLICATION_ID", "")
    if not application_id:
        print("Discord application ID not configured")
        return
    
    # คำสั่งที่ต้องการลงทะเบียน
    commands = [
        {
            "name": "sentiment",
            "description": "วิเคราะห์ความรู้สึกของข้อความ",
            "options": [
                {
                    "name": "text",
                    "description": "ข้อความที่ต้องการวิเคราะห์",
                    "type": 3,  # STRING
                    "required": True
                }
            ]
        }
    ]
    
    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        for command in commands:
            try:
                response = await client.post(
                    f"{DISCORD_API_URL}/applications/{application_id}/commands",
                    headers=headers,
                    json=command
                )
                
                if response.status_code == 200 or response.status_code == 201:
                    print(f"Successfully registered command: {command['name']}")
                else:
                    print(f"Failed to register command {command['name']}: {response.text}") 
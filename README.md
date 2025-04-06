# Thai-English Sentiment Analysis API

ระบบวิเคราะห์ความรู้สึก (Sentiment Analysis) ที่รองรับทั้งภาษาไทยและภาษาอังกฤษ พร้อม Dashboard สำหรับแสดงผลและทดสอบ API

![Dashboard Screenshot](https://media.discordapp.net/attachments/1019596138975867014/1358531954022158426/image.png?ex=67f42efa&is=67f2dd7a&hm=1e616c6118c331e68966b4e772ab79efa8fcd81522efe216595196ff64692dd6&=&format=webp&quality=lossless)

## คุณสมบัติ

- วิเคราะห์ความรู้สึกของข้อความเป็น Positive, Neutral หรือ Negative
- รองรับทั้งภาษาไทยและภาษาอังกฤษ
- แสดงค่าความมั่นใจ (Confidence) และความน่าจะเป็น (Probability) ของแต่ละความรู้สึก
- จัดเก็บข้อมูลใน PostgreSQL
- สร้างด้วย FastAPI, HTMX และ Docker
- มี Dashboard สำหรับแสดงผลและทดสอบ API
- พร้อมรองรับการเชื่อมต่อกับ Line และ Discord (กำลังพัฒนา)

## การติดตั้ง

### วิธีที่ 1: ใช้ Docker (แนะนำ)

1. **สิ่งที่ต้องมี:**
   - [Docker](https://www.docker.com/get-started)
   - [Docker Compose](https://docs.docker.com/compose/install/)

2. **Clone โปรเจค:**
   ```bash
   git clone https://github.com/yourusername/sentiment-api.git
   cd sentiment-api
   ```

3. **ตั้งค่า Environment Variables (ทางเลือก):**
   ```bash
   cp .env.example .env
   # แก้ไขไฟล์ .env ตามต้องการ
   ```

4. **รัน Docker Compose:**
   ```bash
   docker-compose up -d
   ```

5. **เข้าถึง API และ Dashboard:**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Dashboard: http://localhost:8000/dashboard

### วิธีที่ 2: ใช้ Conda (สำหรับการพัฒนา)

1. **สิ่งที่ต้องมี:**
   - [Anaconda](https://www.anaconda.com/download/) หรือ [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
   - [PostgreSQL](https://www.postgresql.org/download/)

2. **Clone โปรเจค:**
   ```bash
   git clone https://github.com/yourusername/sentiment-api.git
   cd sentiment-api
   ```

3. **สร้าง Conda Environment:**
   ```bash
   conda create -n sentiment-api python=3.9
   conda activate sentiment-api
   pip install -r requirements.txt
   ```

4. **ตั้งค่า PostgreSQL:**
   - สร้างฐานข้อมูล `sentimentdb`
   - ตั้งค่า environment variables:
     ```bash
     # Windows
     set DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sentimentdb
     
     # Linux/Mac
     export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sentimentdb
     ```

5. **รันแอปพลิเคชัน:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **เข้าถึง API และ Dashboard:**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Dashboard: http://localhost:8000/dashboard

### วิธีที่ 3: Deploy บน Render.com

1. Fork โปรเจคนี้บน GitHub
2. ไปที่ [Render.com](https://render.com) และสร้างบัญชี
3. เลือก "New" > "Blueprint" (เพื่อใช้ไฟล์ render.yaml)
4. เชื่อมต่อกับ GitHub repository ของคุณ
5. Render จะสร้าง Web Service และ PostgreSQL database ให้โดยอัตโนมัติ

## วิธีใช้งาน

### REST API

API สามารถเข้าถึงได้ผ่าน endpoints ต่อไปนี้:

#### 1. วิเคราะห์ข้อความ

```
POST /predict
```

Request:
```json
{
  "text": "สวัสดีค่ะ วันนี้อารมณ์ดีมาก"
}
```

Response:
```json
{
  "text": "สวัสดีค่ะ วันนี้อารมณ์ดีมาก",
  "sentiment": "Positive",
  "confidence": 92.5,
  "probabilities": {
    "Positive": 92.5,
    "Neutral": 5.3,
    "Negative": 2.2
  }
}
```

#### 2. ตรวจสอบสถานะ API

```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Dashboard

Dashboard มีคุณสมบัติต่อไปนี้:

1. **หน้าหลัก (Home):**
   - ภาพรวมของระบบ
   - เชื่อมโยงไปยังหน้าอื่นๆ
   - คำแนะนำการใช้งาน API

2. **แผงควบคุม (Dashboard):**
   - สรุปสถิติการวิเคราะห์ความรู้สึก
   - กราฟแสดงการกระจายตัวของความรู้สึก
   - กราฟแสดงการกระจายตัวของภาษา
   - กิจกรรมล่าสุด

3. **ทดสอบ API (API Tester):**
   - ส่งข้อความเพื่อวิเคราะห์ความรู้สึก
   - แสดงผลลัพธ์แบบเรียลไทม์
   - ตัวอย่างการเรียกใช้ API

4. **ประวัติ (History):**
   - แสดงประวัติการวิเคราะห์ทั้งหมด
   - ดูรายละเอียดของแต่ละการวิเคราะห์
   - กรองและค้นหาตามเงื่อนไข

## การเชื่อมต่อกับฐานข้อมูล

คุณสามารถเชื่อมต่อกับฐานข้อมูล PostgreSQL โดยใช้เครื่องมือเช่น DBeaver:

1. ดาวน์โหลดและติดตั้ง [DBeaver](https://dbeaver.io/download/)
2. สร้างการเชื่อมต่อ PostgreSQL ใหม่:
   - Host: `localhost` (หรือชื่อโฮสต์ของ database)
   - Port: `5432`
   - Database: `sentimentdb`
   - Username: `postgres`
   - Password: `postgres`
3. เชื่อมต่อและเรียกดูตาราง:
   - `sentiment_history` - เก็บประวัติการวิเคราะห์ความรู้สึก
   - `sentiment_predictions` - เก็บข้อมูลการทำนาย

## แผนการพัฒนาในอนาคต

### การเชื่อมต่อกับแพลตฟอร์มแชท

1. **Line Messaging API:**
   - รับข้อความจากกลุ่ม Line
   - วิเคราะห์ความรู้สึกแบบอัตโนมัติ
   - ส่งผลลัพธ์กลับไปยัง Line
   - เก็บข้อมูลผู้ใช้และกลุ่ม

2. **Discord Bot:**
   - รับข้อความจากเซิร์ฟเวอร์ Discord
   - คำสั่ง slash command สำหรับวิเคราะห์ความรู้สึก
   - แสดงผลลัพธ์ในรูปแบบ embed
   - เก็บข้อมูลผู้ใช้และเซิร์ฟเวอร์

### การปรับปรุง Dashboard

1. **Dashboard แบบกำหนดเอง:**
   - แยกตามแพลตฟอร์ม (Web, Line, Discord)
   - แยกตามกลุ่ม/ห้องแชท
   - ช่วงเวลาที่กำหนดเอง

2. **การวิเคราะห์เชิงลึก:**
   - แนวโน้มความรู้สึกตามเวลา
   - ผู้ใช้ที่มีความรู้สึกเชิงบวก/ลบมากที่สุด
   - คำหรือวลีที่พบบ่อยในแต่ละความรู้สึก

3. **การส่งออกรายงาน:**
   - ส่งออกเป็น CSV/Excel/PDF
   - รายงานประจำวัน/สัปดาห์/เดือน
   - การส่งอีเมลสรุปอัตโนมัติ

### การปรับปรุงโมเดล

1. **เพิ่มความแม่นยำ:**
   - ปรับปรุงโมเดลด้วยข้อมูลเพิ่มเติม
   - รองรับภาษาอื่นๆ
   - การวิเคราะห์เชิงลึกมากขึ้น (เช่น อารมณ์ย่อย)

2. **การประมวลผลภาษาธรรมชาติขั้นสูง:**
   - การวิเคราะห์บริบท
   - การระบุเอนทิตี
   - การสรุปข้อความ

## การใช้งานการตั้งค่าสำหรับ Line และ Discord

### Line Messaging API

1. **สร้าง Line Bot:**
   - สร้างบัญชี [Line Developers](https://developers.line.biz/)
   - สร้าง Provider และ Channel
   - รับ Channel Access Token และ Channel Secret

2. **ตั้งค่า Environment Variables:**
   ```bash
   # .env file
   LINE_CHANNEL_SECRET=your_channel_secret
   LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
   ```

3. **ตั้งค่า Webhook URL:**
   - ในหน้า Line Developers Console
   - ตั้งค่า Webhook URL เป็น `https://your-domain.com/webhook/line`
   - เปิดใช้งาน Webhook

### Discord Bot

1. **สร้าง Discord Bot:**
   - ไปที่ [Discord Developer Portal](https://discord.com/developers/applications)
   - สร้าง Application ใหม่
   - ไปที่แท็บ "Bot" และสร้าง Bot
   - รับ Bot Token

2. **ตั้งค่า Environment Variables:**
   ```bash
   # .env file
   DISCORD_BOT_TOKEN=your_bot_token
   DISCORD_APPLICATION_ID=your_application_id
   ```

3. **เชิญ Bot เข้าร่วมเซิร์ฟเวอร์:**
   - ไปที่แท็บ "OAuth2" > "URL Generator"
   - เลือก Scopes: bot, applications.commands
   - เลือก Bot Permissions ที่ต้องการ
   - ใช้ URL ที่สร้างขึ้นเพื่อเชิญ Bot เข้าร่วมเซิร์ฟเวอร์

4. **ลงทะเบียน Slash Commands:**
   - การลงทะเบียนจะเกิดขึ้นโดยอัตโนมัติเมื่อรันแอปพลิเคชัน
   - หรือรันสคริปต์แยกต่างหาก:
     ```python
     from app.integrations.discord_webhook import register_discord_commands
     import asyncio
     
     asyncio.run(register_discord_commands())
     ```

## การแก้ไขปัญหา

### ปัญหาการเชื่อมต่อฐานข้อมูล

```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```

**วิธีแก้ไข:**
- ตรวจสอบว่า PostgreSQL กำลังทำงาน
- ตรวจสอบการตั้งค่า DATABASE_URL
- ตรวจสอบว่าไฟร์วอลล์ไม่ได้บล็อกพอร์ต 5432

### ปัญหาการโหลดโมเดล

```
FileNotFoundError: [Errno 2] No such file or directory: 'thai_english_sentiment_model.pkl'
```

**วิธีแก้ไข:**
- ตรวจสอบว่ามีไฟล์โมเดลในไดเร็กทอรีที่ถูกต้อง
- ตั้งค่า MODEL_PATH ใน .env ให้ถูกต้อง
- ถ้าไม่มีไฟล์โมเดล ระบบจะใช้โมเดลจำลองแทน

## การอัปเดต

ระบบมีการพัฒนาอย่างต่อเนื่อง ติดตามการอัปเดตได้ที่ GitHub repository

## ร่วมพัฒนา

หากคุณสนใจร่วมพัฒนาโปรเจคนี้ โปรด:

1. Fork โปรเจค
2. สร้าง branch ใหม่ (`git checkout -b feature/amazing-feature`)
3. Commit การเปลี่ยนแปลงของคุณ (`git commit -m 'Add some amazing feature'`)
4. Push ไปยัง branch (`git push origin feature/amazing-feature`)
5. เปิด Pull Request

## ลิขสิทธิ์

โปรเจคนี้ได้รับการเผยแพร่ภายใต้ลิขสิทธิ์ MIT - ดู [LICENSE.md](LICENSE.md) สำหรับรายละเอียด

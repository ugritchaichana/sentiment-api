#!/bin/bash

# สร้างโฟลเดอร์เก็บไฟล์สำรองข้อมูลถ้ายังไม่มี
mkdir -p backups

# ชื่อไฟล์สำรองข้อมูลตามวันที่ปัจจุบัน
BACKUP_FILE="backups/sentimentdb_$(date +%Y%m%d_%H%M%S).sql"

# สำรองข้อมูลจากฐานข้อมูล
echo "Backing up database to $BACKUP_FILE..."
docker exec sentiment-api-db pg_dump -U postgres sentimentdb > $BACKUP_FILE

# ลบไฟล์สำรองข้อมูลที่เก่ากว่า 7 วัน
echo "Removing backups older than 7 days..."
find backups -name "sentimentdb_*.sql" -type f -mtime +7 -delete

echo "Backup completed at $(date)" 
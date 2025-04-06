from app.database import engine
from sqlalchemy import text

def migrate():
    """Add new columns to sentiment_history table for platform integrations"""
    with engine.connect() as conn:
        # ตรวจสอบว่ามีคอลัมน์ user_id หรือไม่
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'sentiment_history' AND column_name = 'user_id'
        """))
        
        # ถ้ายังไม่มีคอลัมน์ จึงเพิ่ม
        if result.rowcount == 0:
            print("Adding new columns for platform integrations...")
            conn.execute(text("""
                ALTER TABLE sentiment_history 
                ADD COLUMN user_id VARCHAR(100),
                ADD COLUMN user_name VARCHAR(200),
                ADD COLUMN platform VARCHAR(20),
                ADD COLUMN group_id VARCHAR(100),
                ADD COLUMN group_name VARCHAR(200)
            """))
            
            # สร้าง index
            conn.execute(text("CREATE INDEX idx_sentiment_history_user_id ON sentiment_history (user_id)"))
            conn.execute(text("CREATE INDEX idx_sentiment_history_platform ON sentiment_history (platform)"))
            conn.execute(text("CREATE INDEX idx_sentiment_history_group_id ON sentiment_history (group_id)"))
            
            conn.commit()
            print("Migration completed successfully")
        else:
            print("Columns already exist, skipping migration") 
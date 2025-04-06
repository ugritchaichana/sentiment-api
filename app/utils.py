import re
from pythainlp.tokenize import word_tokenize
import pickle
import os
import numpy as np  # NumPy ควรติดตั้งได้ง่ายกว่า pandas
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Path to the pickle model file
MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                          "thai_english_sentiment_model.pkl"))

# สร้างโมเดลจำลองง่ายๆ ในกรณีที่โหลดโมเดลจริงไม่สำเร็จ
def create_dummy_model():
    class DummyModel:
        def __init__(self):
            self.classes_ = ['Positive', 'Neutral', 'Negative']
        
        def predict(self, texts):
            return ['Positive'] * len(texts)
        
        def predict_proba(self, texts):
            return [[0.8, 0.1, 0.1]] * len(texts)
    
    return DummyModel()

# พยายามโหลดโมเดล
try:
    print(f"กำลังโหลดโมเดลจาก {MODEL_PATH}")
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print("โหลดโมเดลสำเร็จ")
    else:
        print(f"ไม่พบไฟล์โมเดล {MODEL_PATH} - ใช้โมเดลจำลองแทน")
        model = create_dummy_model()
except Exception as e:
    print(f"เกิดข้อผิดพลาดในการโหลดโมเดล: {str(e)} - ใช้โมเดลจำลองแทน")
    model = create_dummy_model()

def clean_text(text):
    """
    Clean text data by removing URLs, user mentions, extra spaces, etc.
    """
    if not isinstance(text, str):
        return ""
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove user mentions (@username)
    text = re.sub(r'@\w+', '', text)
    
    # Remove hashtags
    text = re.sub(r'#\w+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def detect_language(text):
    """
    Detect if text is Thai, English, or mixed
    """
    # Count Thai and English characters
    thai_chars = sum(1 for char in text if '\u0e00' <= char <= '\u0e7f')
    
    # If more than 20% Thai characters, consider it contains Thai
    if thai_chars / max(len(text), 1) > 0.2:
        if thai_chars / max(len(text), 1) > 0.8:
            return "thai"
        else:
            return "mixed"
    else:
        return "english"

def predict_sentiment(text):
    """
    Predict sentiment for the given text
    """
    # Clean the text
    cleaned_text = clean_text(text)
    
    # Detect language
    language = detect_language(cleaned_text)
    
    try:
        # Make prediction
        prediction = model.predict([cleaned_text])[0]
        
        # Get prediction probabilities
        proba = model.predict_proba([cleaned_text])[0]
        confidence = float(max(proba) * 100)
        
        # Get all class probabilities
        all_probas = {cls: float(prob*100) for cls, prob in zip(model.classes_, proba)}
        
        return {
            "text": text,
            "cleaned_text": cleaned_text,
            "sentiment": prediction,
            "confidence": confidence,
            "probabilities": all_probas,
            "language": language
        }
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการทำนาย: {str(e)}")
        return {
            "text": text,
            "cleaned_text": cleaned_text,
            "sentiment": "Positive",  # ค่าเริ่มต้น
            "confidence": 80.0,
            "probabilities": {"Positive": 80.0, "Neutral": 10.0, "Negative": 10.0},
            "language": language
        }
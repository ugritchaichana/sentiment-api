import pickle
from sklearn.ensemble import RandomForestClassifier

# สร้างโมเดลจำลอง
model = RandomForestClassifier()
model.classes_ = ['Positive', 'Neutral', 'Negative']

# สร้างฟังก์ชันปลอมๆ สำหรับการทำนาย
def dummy_predict(X):
    # สมมติให้ทำนายเป็น Positive เสมอ
    return ['Positive'] * len(X)

def dummy_predict_proba(X):
    # สมมติให้ความน่าจะเป็น Positive สูง
    return [[0.8, 0.1, 0.1]] * len(X)

# เพิ่มเมธอดให้โมเดล
model.predict = dummy_predict
model.predict_proba = dummy_predict_proba

# บันทึกโมเดล
with open('thai_english_sentiment_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("สร้างโมเดลจำลองเรียบร้อยแล้ว: thai_english_sentiment_model.pkl") 
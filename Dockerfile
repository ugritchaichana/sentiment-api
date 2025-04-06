FROM python:3.9-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make sure the script can be executed
RUN chmod +x /app/start.sh

# Add PORT environment variable for Render
ENV PORT=8000

# Create dummy model file if it doesn't exist
RUN if [ ! -f /app/thai_english_sentiment_model.pkl ]; then \
    python -c "import pickle; from sklearn.ensemble import RandomForestClassifier; model = RandomForestClassifier(); model.classes_ = ['Positive', 'Neutral', 'Negative']; model.predict = lambda X: ['Positive'] * len(X); model.predict_proba = lambda X: [[0.8, 0.1, 0.1]] * len(X); with open('/app/thai_english_sentiment_model.pkl', 'wb') as f: pickle.dump(model, f)"; \
    fi

# Expose the port
EXPOSE 8000

# Run the application
CMD ["/app/start.sh"]
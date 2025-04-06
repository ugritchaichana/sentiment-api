#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
sleep 5

# Add current directory to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/app"

# Allow Render to set the port via PORT environment variable
if [ -n "$PORT" ]; then
    PORT_FLAG="--port ${PORT}"
else
    PORT_FLAG="--port 8000"
fi

# Run database migrations (optional but recommended)
echo "Creating database tables..."
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"

# Run custom migrations
echo "Running database migrations..."
python -c "from app.migrations import migrate; migrate()"

# Start the API
echo "Starting API server..."
exec uvicorn app.main:app --host 0.0.0.0 ${PORT_FLAG}
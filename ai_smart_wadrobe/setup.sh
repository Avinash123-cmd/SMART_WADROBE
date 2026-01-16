#!/bin/bash

echo "🚀 Setting up AI Smart Wardrobe..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create uploads directory
echo "📁 Creating necessary directories..."
mkdir -p uploads
mkdir -p backend/uploads
mkdir -p ml_service/data
mkdir -p cv_service/data

echo "✅ Directories created"

# Create .env files if they don't exist
echo "⚙️ Setting up environment variables..."

if [ ! -f backend/.env ]; then
    cat > backend/.env << EOF
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=postgresql://postgres:password@db:5432/wardrobe_db
WEATHER_API_KEY=your_openweather_api_key_here
ML_API_URL=http://ml-service:8001
CV_API_URL=http://cv-service:8002
EOF
    echo "✅ Created backend/.env"
fi

if [ ! -f ml_service/.env ]; then
    cat > ml_service/.env << EOF
MODEL_PATH=model.pkl
TRAINING_DATA_PATH=data/training_data.csv
EOF
    echo "✅ Created ml_service/.env"
fi

# Build Docker images
echo "🐳 Building Docker images..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Docker images built successfully"
else
    echo "❌ Failed to build Docker images"
    exit 1
fi

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Initialize database
echo "🗄️ Initializing database..."
docker-compose exec backend python scripts/init_db.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "🌐 Access the application at:"
echo "   Web Interface: http://localhost:5000"
echo ""
echo "🔗 Demo Credentials:"
echo "   Username: demo"
echo "   Password: demo123"
echo ""
echo "📊 Services:"
echo "   Web Backend: http://localhost:5000"
echo "   ML Service:  http://localhost:8001"
echo "   CV Service:  http://localhost:8002"
echo "   API Docs:    http://localhost:8001/docs"
echo ""
echo "🛑 To stop the services:"
echo "   docker-compose down"
echo ""
echo "📝 To view logs:"
echo "   docker-compose logs -f"
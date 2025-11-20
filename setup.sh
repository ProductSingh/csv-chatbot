#!/bin/bash

echo "🚀 Setting up CSV Chatbot Web App..."

# Backend setup
echo "📦 Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Creating .env file..."
    echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
    echo "⚠️  Please edit backend/.env and add your Google API key!"
fi

cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend
npm install

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit backend/.env and add your GOOGLE_API_KEY"
echo "2. Start backend: cd backend && source venv/bin/activate && python main.py"
echo "3. Start frontend: cd frontend && npm run dev"
echo ""
echo "🌐 Frontend will be available at http://localhost:3000"
echo "🔧 Backend will be available at http://localhost:8000"


#!/bin/bash
# Quick PostgreSQL setup script for CSV Chatbot

echo "🗄️  CSV Chatbot - PostgreSQL Setup Script"
echo "=========================================="

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed. Please install it first:"
    echo "   macOS: brew install postgresql@15"
    echo "   Linux: sudo apt-get install postgresql postgresql-contrib"
    echo "   Windows: Download from https://www.postgresql.org/download/windows/"
    exit 1
fi

echo "✓ PostgreSQL found"

# Check if PostgreSQL is running
if ! pg_isready -h localhost -q; then
    echo "⚠️  PostgreSQL is not running. Starting PostgreSQL..."
    brew services start postgresql@15 2>/dev/null || sudo service postgresql start 2>/dev/null || true
    sleep 2
fi

if pg_isready -h localhost -q; then
    echo "✓ PostgreSQL is running"
else
    echo "❌ Could not connect to PostgreSQL. Please start it manually and run this script again."
    exit 1
fi

# Create user and database
echo ""
echo "Creating database and user..."

psql -U postgres <<EOF
-- Drop existing resources if they exist (optional)
-- DROP DATABASE IF EXISTS csv_chatbot;
-- DROP USER IF EXISTS csv_chatbot;

-- Create user if not exists
DO \$\$ BEGIN
    CREATE ROLE csv_chatbot WITH LOGIN PASSWORD 'csv_chatbot_secure_password_2024';
    EXCEPTION WHEN DUPLICATE_OBJECT THEN
        ALTER ROLE csv_chatbot WITH PASSWORD 'csv_chatbot_secure_password_2024';
END
\$\$;

-- Create database if not exists
SELECT 'CREATE DATABASE csv_chatbot OWNER csv_chatbot'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'csv_chatbot')\gexec

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE csv_chatbot TO csv_chatbot;
EOF

echo "✓ Database and user created"

# Update .env file
echo ""
echo "Updating .env file..."

if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "✓ Created backend/.env from template"
else
    echo "✓ backend/.env already exists"
fi

# Update DATABASE_URL in .env
if grep -q "DATABASE_URL=" backend/.env; then
    # Update existing DATABASE_URL
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' 's|^DATABASE_URL=.*|DATABASE_URL=postgresql://csv_chatbot:csv_chatbot_secure_password_2024@localhost:5432/csv_chatbot|' backend/.env
    else
        # Linux
        sed -i 's|^DATABASE_URL=.*|DATABASE_URL=postgresql://csv_chatbot:csv_chatbot_secure_password_2024@localhost:5432/csv_chatbot|' backend/.env
    fi
else
    echo "DATABASE_URL=postgresql://csv_chatbot:csv_chatbot_secure_password_2024@localhost:5432/csv_chatbot" >> backend/.env
fi

echo "✓ Updated DATABASE_URL in backend/.env"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."

if [ ! -d "backend/venv" ]; then
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
    cd ..
    echo "✓ Python dependencies installed"
else
    echo "✓ Virtual environment already exists"
fi

# Test connection
echo ""
echo "Testing database connection..."

psql -U csv_chatbot -d csv_chatbot -h localhost -c "SELECT 1;" &>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Database connection successful"
else
    echo "❌ Could not connect to database. Please check your PostgreSQL setup."
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ PostgreSQL setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Start the backend: cd backend && python main.py"
echo "2. In another terminal, start the frontend: cd frontend && npm run dev"
echo "3. Open http://localhost:3004 in your browser"
echo ""
echo "Database credentials:"
echo "  User: csv_chatbot"
echo "  Password: csv_chatbot_secure_password_2024"
echo "  Database: csv_chatbot"
echo "  Host: localhost:5432"
echo ""
echo "To view database contents via psql:"
echo "  psql -U csv_chatbot -d csv_chatbot"
echo ""
echo "See POSTGRES_SETUP.md for detailed documentation."

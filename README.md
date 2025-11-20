# 📊 CSV Chatbot Web App

A modern web application that allows users to upload CSV files and ask natural language questions about their data using an AI agent powered by Google's Agent Development Kit (ADK).

## ✨ Features

- 📤 **CSV File Upload**: Drag-and-drop or browse to upload CSV files
- 💬 **Natural Language Queries**: Ask questions about your data in plain English
- 🤖 **AI-Powered Analysis**: Uses Google's Gemini AI with custom tools for dataframe operations
- 📈 **Data Analysis Tools**: Calculate means, averages, sums, filter by date ranges, group by month/category, and more
- 🎨 **Modern UI**: Beautiful, responsive React frontend
- 🔄 **Session Management**: Maintain conversation context across queries
- 🛡️ **Guardrails**: Agent stays focused on CSV data analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "Uptio Project"
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Environment Variables**
   ```bash
   cd ../backend
   cp ../.env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

5. **Run the Application**

   **Terminal 1 (Backend)**:
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```

   **Terminal 2 (Frontend)**:
   ```bash
   cd frontend
   npm run dev
   ```

6. **Open Browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 📖 Documentation

For comprehensive documentation including:
- Project structure explanation
- Tech stack details
- Where to make changes
- Troubleshooting guide

See [PROJECT_DOCUMENTATION.md](./PROJECT_DOCUMENTATION.md)

## 🎯 Example Queries

- "What can you help me with?"
- "What is the mean of the sales column?"
- "Calculate the total revenue"
- "Show me units sold by month"
- "What are the columns in this dataset?"
- "Give me sales by category"

## 🛠 Tech Stack

**Frontend**: React 18, Vite, Axios  
**Backend**: FastAPI, Google ADK, Gemini AI, Pandas  
**AI**: Google Agent Development Kit (ADK), Gemini 2.0 Flash

## 📁 Project Structure

```
Uptio Project/
├── backend/          # FastAPI backend with AI agent
├── frontend/         # React frontend
├── README.md         # This file
└── PROJECT_DOCUMENTATION.md  # Comprehensive docs
```

## 🔧 Configuration

### Backend
- API Key: Set `GOOGLE_API_KEY` in `backend/.env`
- Port: Default 8000 (change in `backend/main.py`)

### Frontend
- API URL: Default `http://localhost:8000` (change in `frontend/src/App.jsx`)
- Port: Default 3000 (change in `frontend/vite.config.js`)

## 🐛 Troubleshooting

### Common Issues

**API Key Error**: Ensure `GOOGLE_API_KEY` is set in `backend/.env` (no quotes)

**Port Already in Use**: Change port or kill existing process

**Module Not Found**: Reinstall dependencies (`pip install -r requirements.txt` or `npm install`)

**Session Errors**: Check session handling in `backend/agent.py`

See [PROJECT_DOCUMENTATION.md](./PROJECT_DOCUMENTATION.md) for detailed troubleshooting.

## 📝 License

MIT

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**For detailed documentation, see [PROJECT_DOCUMENTATION.md](./PROJECT_DOCUMENTATION.md)**

# CSV Chatbot

A web application that lets you upload CSV files and chat with your data using AI. Ask questions in plain English and get instant answers.

## Features

- **Upload CSV Files**: Simply upload your CSV file to start
- **Ask Questions**: Write your questions in plain English, no SQL needed
- **Get Instant Results**: AI analyzes your data and gives answers
- **Chat History**: All your conversations are saved, you can go back and check anytime
- **Clean Design**: Simple, easy-to-use interface
- **Data Safety**: Your data stays private, not shared anywhere

## How to Set Up

### What You Need

- Python 3.8 or higher
- Node.js 16 or higher  
- Google API Key (free) - [Get it here](https://makersuite.google.com/app/apikey)
- PostgreSQL database (for saving your chats)

### Installation Steps

1. **Get the code**
   ```bash
   git clone <repository-url>
   cd csv-chatbot
   ```

2. **Set up database** (run this first, only once)
   ```bash
   bash postgres_setup.sh
   ```

3. **Set up everything else** (backend + frontend)
   ```bash
   bash setup.sh
   ```

4. **Add your Google API Key**
   - Open `backend/.env`
   - Add your API key there
   - Save the file

5. **Start the backend** (Terminal 1)
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```

6. **Start the frontend** (Terminal 2)
   ```bash
   cd frontend
   npm run dev
   ```

7. **Open in browser**
   - Go to: `http://localhost:3004`
   - Enter your name
   - Upload your CSV file
   - Start asking questions!

## What Can You Ask?

- "What are the average sales?"
- "Show me total revenue"
- "How many rows in this file?"
- "Group data by month"
- "What columns do we have?"
- "Filter where sales > 1000"

## Tech Used

- **Frontend**: React, Vite, modern UI
- **Backend**: Python, FastAPI, Google Gemini AI
- **Database**: PostgreSQL (stores your chats)

## Troubleshooting

**API Key not working?**
- Check `backend/.env` file
- Make sure you copied the key correctly
- No quotes needed around the key

**Port already in use?**
- Change the port in the config file, or
- Kill the process using that port

**Module missing?**
- Run `pip install -r requirements.txt` in backend folder
- Run `npm install` in frontend folder

**Database issues?**
- Run `bash postgres_setup.sh` again
- Make sure PostgreSQL is running

## License

MIT - You can use this for anything

## Questions?

Check the code files or create an issue in the repository.

---

Happy chatting with your data! 📊

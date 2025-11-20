import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import './ChatInterface.css'

const API_BASE_URL = 'http://localhost:8000'

function ChatInterface({ sessionId, fileInfo, onNewAnalysis }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput('')
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }])
    setIsLoading(true)

    try {
      const response = await axios.post(`${API_BASE_URL}/query`, {
        session_id: sessionId,
        query: userMessage,
      })

      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: response.data.response },
      ])
    } catch (error) {
      console.error('Error sending query:', error)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `Error: ${error.response?.data?.detail || error.message}`,
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const exampleQuestions = [
    'What is the mean of the numeric columns?',
    'Show me the total sales',
    'What are the columns in this dataset?',
    'Calculate the average of all numeric columns',
  ]

  const handleExampleClick = (question) => {
    setInput(question)
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-header-content">
          <div>
            <h2>💬 Ask Questions</h2>
            <p>Ask questions about your uploaded data</p>
          </div>
          {onNewAnalysis && (
            <button
              className="new-analysis-header-button"
              onClick={onNewAnalysis}
              title="Start new analysis"
            >
              🔄 New Analysis
            </button>
          )}
        </div>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <p>👋 Welcome! I'm your CSV Data Analysis Agent.</p>
            <p className="welcome-subtext">Ask me questions about your data or try:</p>
            <div className="example-questions">
              {exampleQuestions.map((q, idx) => (
                <button
                  key={idx}
                  className="example-question"
                  onClick={() => handleExampleClick(q)}
                >
                  {q}
                </button>
              ))}
            </div>
            <button
              className="example-question help-question"
              onClick={() => handleExampleClick("What can you help me with?")}
            >
              What can you help me with?
            </button>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-content">
              <div className="message-role">
                {msg.role === 'user' ? '👤 You' : '🤖 Assistant'}
              </div>
              <div className="message-text">{msg.content}</div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="message-role">🤖 Assistant</div>
              <div className="message-text loading">Thinking...</div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about your data..."
          className="chat-input"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="send-button"
          disabled={isLoading || !input.trim()}
        >
          {isLoading ? '⏳' : '➤'}
        </button>
      </form>
    </div>
  )
}

export default ChatInterface


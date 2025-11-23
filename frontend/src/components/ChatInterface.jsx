import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { Send, Loader } from 'lucide-react'
import './ChatInterface.css'

const API_BASE_URL = 'http://localhost:8000'

function ChatInterface({ sessionId, fileInfo, onNewChat, onFileDetailsClick, onReplaceCSV }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isLoadingHistory, setIsLoadingHistory] = useState(false)
  const messagesEndRef = useRef(null)
  const messagesContainerRef = useRef(null)

  // Load chat history when sessionId changes
  useEffect(() => {
    if (sessionId) {
      loadChatHistory()
    }
  }, [sessionId])

  const loadChatHistory = async () => {
    setIsLoadingHistory(true)
    try {
      const response = await axios.get(
        `${API_BASE_URL}/session/${sessionId}/messages`,
        { headers: { 'credentials': 'include' } }
      )
      if (response.data.messages) {
        // Convert backend format to frontend format
        const formattedMessages = response.data.messages.map((msg) => ({
          role: msg.message_type,
          content: msg.content,
        }))
        setMessages(formattedMessages)
      } else {
        setMessages([])
      }
    } catch (error) {
      console.error('Error loading chat history:', error)
      setMessages([])
    } finally {
      setIsLoadingHistory(false)
    }
  }

  const scrollToBottom = () => {
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, 0)
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading])

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
    'Show me key statistics',
    'What are the columns in this dataset?',
    'Give me a data summary',
  ]

  const handleExampleClick = (question) => {
    setInput(question)
  }

  return (
    <div className="chat-interface-wrapper">
      {/* Floating File Info Button */}
      <button 
        className="file-info-fab"
        onClick={onFileDetailsClick}
        title={`View details: ${fileInfo?.fileName}`}
      >
        <span className="fab-icon">📋</span>
        <span className="fab-label">File</span>
      </button>

      {/* File Info Bar */}
      <div className="file-info-bar">
        <div className="file-info-item">
          <span className="file-name">{fileInfo?.fileName || 'Untitled'}</span>
          <span className="file-stats">
            {fileInfo?.rows} rows • {fileInfo?.columns?.length} columns
          </span>
        </div>
        <button className="file-actions-btn" onClick={onNewChat}>
          + New Chat
        </button>
      </div>

      {/* Messages Container */}
      <div className="messages-container" ref={messagesContainerRef}>
        {isLoadingHistory ? (
          <div className="loading-history">
            <div className="spinner"></div>
            <p>Loading chat history...</p>
          </div>
        ) : messages.length === 0 ? (
          <div className="welcome-section">
            <div className="welcome-header">
              <h2>Ask anything about your data</h2>
              <p>Get instant insights with natural language queries</p>
            </div>

            <div className="suggested-prompts">
              <p className="prompts-title">Try asking:</p>
              {exampleQuestions.map((q, idx) => (
                <button
                  key={idx}
                  className="prompt-button"
                  onClick={() => handleExampleClick(q)}
                >
                  <span className="prompt-icon">→</span>
                  {q}
                </button>
              ))}
            </div>

            <div className="file-summary">
              <h3>File Summary</h3>
              <div className="summary-grid">
                <div className="summary-item">
                  <span className="summary-label">Rows</span>
                  <span className="summary-value">{fileInfo?.rows}</span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Columns</span>
                  <span className="summary-value">{fileInfo?.columns?.length}</span>
                </div>
              </div>
              <div className="columns-display">
                <p className="columns-title">Columns:</p>
                <div className="columns-list">
                  {fileInfo?.columns?.map((col, idx) => (
                    <span key={idx} className="column-badge">
                      {col}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, idx) => (
              <div key={idx} className={`message-wrapper ${msg.role}`}>
                <div className={`message ${msg.role}`}>
                  <div className="message-bubble">
                    <p className="message-text">{msg.content}</p>
                  </div>
                </div>
              </div>
            ))}
          </>
        )}

        {isLoading && (
          <div className="message-wrapper assistant">
            <div className="message assistant">
              <div className="message-bubble loading">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form className="input-form" onSubmit={handleSubmit}>
        <div className="input-wrapper">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Message CSV Chat..."
            className="message-input"
            disabled={isLoading}
            autoFocus
          />
          <button
            type="submit"
            className={`send-btn ${isLoading ? 'loading' : ''}`}
            disabled={isLoading || !input.trim()}
          >
            {isLoading ? (
              <Loader size={20} className="loader-icon" />
            ) : (
              <Send size={20} />
            )}
          </button>
        </div>
        <p className="input-hint"></p>
      </form>
    </div>
  )
}

export default ChatInterface


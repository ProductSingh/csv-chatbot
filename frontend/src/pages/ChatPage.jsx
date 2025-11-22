import React, { useState } from 'react'
import { Plus, LogOut, Menu, X } from 'lucide-react'
import ChatInterface from '../components/ChatInterface'
import FileUpload from '../components/FileUpload'
import '../styles/ChatPage.css'

function ChatPage({ userName, onLogout }) {
  const [sessionId, setSessionId] = useState(null)
  const [fileInfo, setFileInfo] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [chatHistory, setChatHistory] = useState([])
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [showUploadModal, setShowUploadModal] = useState(false)

  const handleFileUpload = async (file, existingSessionId = null) => {
    setIsLoading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)
      if (existingSessionId) {
        formData.append('session_id', existingSessionId)
      }

      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
        credentials: 'include',
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`Failed to upload file: ${response.status} - ${errorText}`)
      }

      const data = await response.json()

      setSessionId(data.session_id)
      setFileInfo({
        rows: data.rows,
        columns: data.columns,
        preview: data.preview,
        fileName: file.name,
      })
      setShowUploadModal(false)
    } catch (error) {
      console.error('Error uploading file:', error)
      alert(`Failed to upload file: ${error.message}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleNewChat = () => {
    setChatHistory([])
    setSessionId(null)
    setFileInfo(null)
    setShowUploadModal(true)
  }

  const handleLogout = () => {
    onLogout()
  }

  return (
    <div className="chat-page">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <span className="logo-icon">💬</span>
          </div>
          <button
            className="sidebar-toggle-mobile"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        <button className="new-chat-btn" onClick={handleNewChat}>
          <Plus size={20} />
          <span>New Chat</span>
        </button>

        <div className="sidebar-content">
          <div className="chat-history">
            <h3>History</h3>
            {chatHistory.length === 0 ? (
              <p className="empty-history">No chats yet</p>
            ) : (
              chatHistory.map((chat, idx) => (
                <div key={idx} className="history-item">
                  <span className="history-item-text">{chat.title}</span>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="sidebar-footer">
          <button className="logout-btn" onClick={handleLogout}>
            <LogOut size={20} />
            <span>Logout</span>
          </button>
          <div className="user-info">
            <p>Welcome, {userName}!</p>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <div className="chat-header">
          <button
            className="menu-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            <Menu size={24} />
          </button>
          <h1 className="page-title">CSV Data Analysis</h1>
          <div className="header-spacer"></div>
        </div>

        {/* Upload Modal/Dialog */}
        {showUploadModal && (
          <div className="upload-modal-overlay" onClick={() => setShowUploadModal(false)}>
            <div className="upload-modal" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h2>Upload CSV File</h2>
                <button
                  className="modal-close"
                  onClick={() => setShowUploadModal(false)}
                >
                  ✕
                </button>
              </div>
              <FileUpload
                onFileUpload={handleFileUpload}
                isLoading={isLoading}
              />
            </div>
          </div>
        )}

        {/* Chat Content */}
        <div className="chat-content">
          {!sessionId ? (
            <div className="empty-state">
              <div className="empty-state-icon">📊</div>
              <h2>No file uploaded yet</h2>
              <p>Upload a CSV file to start analyzing your data</p>
              <button className="upload-btn" onClick={() => setShowUploadModal(true)}>
                <Plus size={20} />
                Upload File
              </button>
            </div>
          ) : (
            <ChatInterface
              sessionId={sessionId}
              fileInfo={fileInfo}
              onNewChat={handleNewChat}
            />
          )}
        </div>
      </main>
    </div>
  )
}

export default ChatPage

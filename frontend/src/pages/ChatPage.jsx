import React, { useState, useEffect } from 'react'
import { Plus, LogOut, Menu, X, Trash2 } from 'lucide-react'
import ChatInterface from '../components/ChatInterface'
import FileUpload from '../components/FileUpload'
import '../styles/ChatPage.css'

function ChatPage({ userName, onLogout }) {
  const [sessionId, setSessionId] = useState(null)
  const [fileInfo, setFileInfo] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [sessions, setSessions] = useState([])
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [showUploadModal, setShowUploadModal] = useState(false)
  const [showFileDetails, setShowFileDetails] = useState(false)

  // Load sessions on component mount
  useEffect(() => {
    loadSessions()
  }, [])

  const loadSessions = async () => {
    try {
      const response = await fetch('http://localhost:8000/sessions', {
        credentials: 'include',
      })
      if (response.ok) {
        const data = await response.json()
        setSessions(data.sessions || [])
      }
    } catch (error) {
      console.error('Error loading sessions:', error)
    }
  }

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
      
      // Reload sessions to show the new upload
      loadSessions()
    } catch (error) {
      console.error('Error uploading file:', error)
      alert(`Failed to upload file: ${error.message}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleNewChat = () => {
    setSessionId(null)
    setFileInfo(null)
    setShowUploadModal(true)
  }

  const handleSelectSession = async (session) => {
    try {
      setSessionId(session.id)
      setFileInfo({
        rows: session.metadata?.rows || 0,
        columns: session.metadata?.columns || [],
        fileName: session.filename,
      })
      // Keep sidebar open on desktop, only close on mobile
      if (window.innerWidth <= 768) {
        setSidebarOpen(false)
      }
    } catch (error) {
      console.error('Error selecting session:', error)
    }
  }

  const handleDeleteSession = async (sessionId, e) => {
    e.stopPropagation()
    if (window.confirm('Are you sure you want to delete this session?')) {
      try {
        const response = await fetch(`http://localhost:8000/session/${sessionId}`, {
          method: 'DELETE',
          credentials: 'include',
        })
        if (response.ok) {
          if (sessionId === sessionId) {
            setSessionId(null)
            setFileInfo(null)
          }
          loadSessions()
        }
      } catch (error) {
        console.error('Error deleting session:', error)
        alert('Failed to delete session')
      }
    }
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
          {/* Chat History */}
          <div className="chat-history">
            <h3>Chat History</h3>
            {sessions.length === 0 ? (
              <p className="empty-history">No chats yet</p>
            ) : (
              sessions.map((session) => (
                <div
                  key={session.id}
                  className={`history-item ${sessionId === session.id ? 'active' : ''}`}
                  onClick={() => handleSelectSession(session)}
                >
                  <div className="history-item-content">
                    <span className="history-item-title">{session.filename}</span>
                    <span className="history-item-meta">
                      {session.metadata?.rows || 0} rows • {session.message_count} messages
                    </span>
                  </div>
                  <button
                    className="history-item-delete"
                    onClick={(e) => handleDeleteSession(session.id, e)}
                    title="Delete this session"
                  >
                    <Trash2 size={16} />
                  </button>
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
          <h1 className="page-title">CSV Chatbot</h1>
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

        {/* File Details Modal */}
        {showFileDetails && fileInfo && (
          <div className="modal-overlay" onClick={() => setShowFileDetails(false)}>
            <div className="file-details-modal" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h2>📄 File Details</h2>
                <button
                  className="modal-close"
                  onClick={() => setShowFileDetails(false)}
                >
                  ✕
                </button>
              </div>
              <div className="file-details-content">
                <div className="detail-section">
                  <h3>File Name</h3>
                  <p className="detail-value">{fileInfo.fileName}</p>
                </div>

                <div className="detail-section">
                  <h3>Statistics</h3>
                  <div className="stats-grid">
                    <div className="stat-card">
                      <span className="stat-label">Rows</span>
                      <span className="stat-number">{fileInfo.rows}</span>
                    </div>
                    <div className="stat-card">
                      <span className="stat-label">Columns</span>
                      <span className="stat-number">{fileInfo.columns?.length || 0}</span>
                    </div>
                  </div>
                </div>

                {fileInfo.columns && fileInfo.columns.length > 0 && (
                  <div className="detail-section">
                    <h3>Columns ({fileInfo.columns.length})</h3>
                    <div className="columns-list-detailed">
                      {fileInfo.columns.map((col, idx) => (
                        <div key={idx} className="column-item">
                          <span className="column-number">{idx + 1}</span>
                          <span className="column-name">{col}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="modal-actions">
                  <button 
                    className="action-btn replace-btn"
                    onClick={() => {
                      setShowFileDetails(false)
                      setShowUploadModal(true)
                    }}
                  >
                    🔄 Replace CSV
                  </button>
                  <button 
                    className="action-btn close-btn"
                    onClick={() => setShowFileDetails(false)}
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Chat Content */}
        <div className="chat-content">
          {!sessionId ? (
            <div className="empty-state">
              <div className="empty-state-icon">📊</div>
              <h2>No file selected</h2>
              <p>Upload a CSV file or select one from history to start analyzing</p>
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
              onFileDetailsClick={() => setShowFileDetails(true)}
              onReplaceCSV={() => setShowUploadModal(true)}
            />
          )}
        </div>
      </main>
    </div>
  )
}

export default ChatPage

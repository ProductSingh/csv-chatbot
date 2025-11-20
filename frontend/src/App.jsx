import React, { useState } from 'react'
import FileUpload from './components/FileUpload'
import ChatInterface from './components/ChatInterface'
import './App.css'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [sessionId, setSessionId] = useState(null)
  const [fileInfo, setFileInfo] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleFileUpload = async (file, existingSessionId = null) => {
    setIsLoading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)
      if (existingSessionId) {
        formData.append('session_id', existingSessionId)
      }

      console.log('Uploading file:', file.name, 'Size:', file.size, 'Type:', file.type)

      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
        // Don't set Content-Type header - let browser set it with boundary for multipart/form-data
        credentials: 'include',
      })

      console.log('Upload response status:', response.status)

      if (!response.ok) {
        const errorText = await response.text()
        console.error('Upload error response:', errorText)
        throw new Error(`Failed to upload file: ${response.status} - ${errorText}`)
      }

      const data = await response.json()
      console.log('Upload successful:', data)
      
      setSessionId(data.session_id)
      setFileInfo({
        rows: data.rows,
        columns: data.columns,
        preview: data.preview,
      })
    } catch (error) {
      console.error('Error uploading file:', error)
      alert(`Failed to upload file: ${error.message}. Please try again.`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleRemoveFile = () => {
    setSessionId(null)
    setFileInfo(null)
  }

  const handleNewAnalysis = () => {
    setSessionId(null)
    setFileInfo(null)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>📊 CSV Chatbot</h1>
        <p>Upload a CSV file and ask questions about your data</p>
      </header>

      <div className="app-content">
        <FileUpload
          onFileUpload={handleFileUpload}
          onRemoveFile={handleRemoveFile}
          onNewAnalysis={handleNewAnalysis}
          isLoading={isLoading}
          fileInfo={fileInfo}
          sessionId={sessionId}
        />

        {sessionId && (
          <ChatInterface
            sessionId={sessionId}
            fileInfo={fileInfo}
            onNewAnalysis={handleNewAnalysis}
          />
        )}
      </div>
    </div>
  )
}

export default App


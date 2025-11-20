import React, { useRef, useState } from 'react'
import './FileUpload.css'

function FileUpload({ onFileUpload, onRemoveFile, onNewAnalysis, isLoading, fileInfo, sessionId }) {
  const fileInputRef = useRef(null)
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = (file) => {
    if (!file) {
      console.error('No file provided')
      return
    }
    
    // Check file type more flexibly
    const isValidCSV = file.type === 'text/csv' || 
                      file.type === 'application/vnd.ms-excel' ||
                      file.name.toLowerCase().endsWith('.csv')
    
    if (!isValidCSV) {
      alert('Please upload a CSV file')
      return
    }
    
    console.log('File selected:', file.name, 'Type:', file.type, 'Size:', file.size)
    
    // Pass the file and current sessionId (if any) to allow re-upload
    onFileUpload(file, sessionId)
  }

  return (
    <div className="file-upload-container">
      <div
        className={`file-upload-area ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleChange}
          className="file-input"
          disabled={isLoading}
        />
        <div className="upload-content">
          <div className="upload-icon">📁</div>
          <p className="upload-text">
            {isLoading ? 'Uploading...' : 'Drag & drop your CSV file here'}
          </p>
          <p className="upload-subtext">or</p>
          <button
            className="browse-button"
            onClick={() => fileInputRef.current?.click()}
            disabled={isLoading}
          >
            Browse Files
          </button>
        </div>
      </div>

      {fileInfo && (
        <div className="file-info">
          <div className="file-info-header">
            <h3>📄 File Information</h3>
            <div className="file-actions">
              <button
                className="remove-file-button"
                onClick={onRemoveFile}
                title="Remove current file"
              >
                🗑️ Remove
              </button>
              <button
                className="new-analysis-button"
                onClick={onNewAnalysis}
                title="Start new analysis"
              >
                🔄 New Analysis
              </button>
            </div>
          </div>
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">Rows:</span>
              <span className="info-value">{fileInfo.rows}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Columns:</span>
              <span className="info-value">{fileInfo.columns.length}</span>
            </div>
          </div>
          <div className="columns-list">
            <strong>Columns:</strong>
            <div className="columns-tags">
              {fileInfo.columns.map((col, idx) => (
                <span key={idx} className="column-tag">
                  {col}
                </span>
              ))}
            </div>
          </div>
          <div className="upload-new-file">
            <p>Want to analyze a different file?</p>
            <button
              className="upload-new-button"
              onClick={() => {
                onRemoveFile()
                fileInputRef.current?.click()
              }}
            >
              📤 Upload New CSV
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default FileUpload


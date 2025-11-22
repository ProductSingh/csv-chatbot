import React, { useRef, useState } from 'react'
import { Upload } from 'lucide-react'
import './FileUpload.css'

function FileUpload({ onFileUpload, isLoading }) {
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

    const isValidCSV =
      file.type === 'text/csv' ||
      file.type === 'application/vnd.ms-excel' ||
      file.name.toLowerCase().endsWith('.csv')

    if (!isValidCSV) {
      alert('Please upload a CSV file')
      return
    }

    console.log('File selected:', file.name, 'Type:', file.type, 'Size:', file.size)
    onFileUpload(file)
  }

  return (
    <div className="file-upload-area-wrapper">
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
        <div className="upload-content" onClick={(e) => e.stopPropagation()}>
          <div className="upload-icon">
            <Upload size={48} />
          </div>
          <p className="upload-text">
            {isLoading ? 'Uploading...' : 'Drag and drop your CSV here'}
          </p>
          <p className="upload-subtext">or</p>
          <button
            className="browse-button"
            onClick={(e) => {
              e.preventDefault()
              e.stopPropagation()
              fileInputRef.current?.click()
            }}
            disabled={isLoading}
            type="button"
          >
            Browse Files
          </button>
        </div>
      </div>
    </div>
  )
}

export default FileUpload


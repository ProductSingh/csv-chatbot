import React, { useState, useEffect } from 'react'
import { ArrowRight, Upload, MessageSquare, BarChart3 } from 'lucide-react'
import '../styles/LandingPage.css'

function LandingPage({ onEnterChat }) {
  const [userName, setUserName] = useState('')
  const [greeting, setGreeting] = useState('')

  useEffect(() => {
    // Get greeting based on time of day
    const hour = new Date().getHours()
    if (hour < 12) {
      setGreeting('Good morning')
    } else if (hour < 18) {
      setGreeting('Good afternoon')
    } else {
      setGreeting('Good evening')
    }
  }, [])

  const handleGetStarted = () => {
    onEnterChat(userName || 'Guest')
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleGetStarted()
    }
  }

  return (
    <div className="landing-page">
      <div className="landing-container">
        {/* Header */}
        <div className="landing-header">
          <div className="logo">
            {/* <div className="logo-icon">📊</div> */}
            <h1>Chat Bot</h1>
          </div>
          <p className="tagline">Analyze your data with conversational AI</p>
        </div>

        {/* Main Content */}
        <div className="landing-content">
          {/* Greeting Section */}
          <div className="greeting-section">
            <h2 className="greeting-text">
              {greeting}
              <span className="greeting-wave">👋</span>
            </h2>
            <p className="greeting-subtext">Enter your name to get started</p>

            <div className="input-group">
              <input
                type="text"
                placeholder="Your name"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                onKeyPress={handleKeyPress}
                className="name-input"
                autoFocus
              />
              <button onClick={handleGetStarted} className="get-started-btn">
                Get Started
                <ArrowRight size={20} />
              </button>
            </div>
          </div>

          {/* Features Section */}
          <div className="features-section">
            <h3>What you can do</h3>
            <div className="features-grid">
              <div className="feature-card">
                <div className="feature-icon">
                  <Upload size={32} />
                </div>
                <h4>Upload CSV Files</h4>
                <p>Drag and drop your CSV files to get started</p>
              </div>

              <div className="feature-card">
                <div className="feature-icon">
                  <MessageSquare size={32} />
                </div>
                <h4>Ask Questions</h4>
                <p>Use natural language to query your data</p>
              </div>

              <div className="feature-card">
                <div className="feature-icon">
                  <BarChart3 size={32} />
                </div>
                <h4>Get Insights</h4>
                <p>Get meaningful analysis and insights instantly</p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="landing-footer">
          <p>Built with React & powered by Google AI</p>
        </footer>
      </div>
    </div>
  )
}

export default LandingPage

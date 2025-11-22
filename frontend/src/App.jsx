import React, { useState } from 'react'
import LandingPage from './pages/LandingPage'
import ChatPage from './pages/ChatPage'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('landing')
  const [userName, setUserName] = useState('')

  const handleEnterChat = (name) => {
    setUserName(name)
    setCurrentPage('chat')
  }

  const handleLogout = () => {
    setUserName('')
    setCurrentPage('landing')
  }

  return (
    <div className="app">
      {currentPage === 'landing' ? (
        <LandingPage onEnterChat={handleEnterChat} />
      ) : (
        <ChatPage userName={userName} onLogout={handleLogout} />
      )}
    </div>
  )
}

export default App


'use client'

import { useState, useEffect } from 'react'
import Footer from '@/components/Footer'
import axios from 'axios'

interface Connection {
  id: number
  name: string
  url: string
  description: string
}

const connections: Connection[] = [
  {
    id: 1,
    name: "GitHub Repository",
    url: "https://github.com/XDM-ZSBW/yourl.cloud",
    description: "Source code and documentation"
  },
  {
    id: 2,
    name: "Google Cloud Run",
    url: "https://cloud.google.com/run",
    description: "Deploy and scale applications"
  },
  {
    id: 3,
    name: "Flask Framework",
    url: "https://flask.palletsprojects.com/",
    description: "Python web framework"
  },
  {
    id: 4,
    name: "Perplexity AI",
    url: "https://perplexity.ai",
    description: "AI-powered search and assistance"
  },
  {
    id: 5,
    name: "Cursor IDE",
    url: "https://cursor.sh",
    description: "AI-powered code editor"
  }
]

export default function HomePage() {
  const [currentPassword, setCurrentPassword] = useState<string>('')
  const [inputPassword, setInputPassword] = useState('')
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [authMessage, setAuthMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    // Fetch the current password from the API
    const fetchPassword = async () => {
      try {
        const response = await axios.get('/api/auth/password')
        setCurrentPassword(response.data.password)
      } catch (error) {
        console.error('Failed to fetch password:', error)
        setCurrentPassword('CLOUD123!') // Fallback
      }
    }
    fetchPassword()
  }, [])

  const handleAuthentication = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setAuthMessage('')

    try {
      const response = await axios.post('/api/auth/verify', {
        password: inputPassword
      })
      
      if (response.data.authenticated) {
        setIsAuthenticated(true)
        setAuthMessage('✅ Authentication successful! Welcome to Yourl.Cloud.')
      } else {
        setAuthMessage('❌ Authentication failed. Please check your password.')
      }
    } catch (error) {
      setAuthMessage('❌ Authentication error. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Main Container */}
        <div className="bg-white/95 rounded-2xl shadow-2xl p-8 my-8">
          {/* Header */}
          <div className="text-center pb-8 border-b-4 border-blue-600 mb-8">
            <h1 className="text-5xl font-bold text-blue-600 mb-4">
              Yourl.Cloud Inc.
            </h1>
            <p className="text-xl text-gray-600">
              Secure Cloud Infrastructure & API Services
            </p>
          </div>

          {/* Authentication Section */}
          <div className="bg-gray-50 rounded-xl p-8 mb-8 text-center">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              Secure Access Portal
            </h2>
            
            {!isAuthenticated ? (
              <form onSubmit={handleAuthentication} className="max-w-md mx-auto">
                <div className="mb-6">
                  <label className="block text-gray-700 font-semibold mb-3 text-lg">
                    Enter Access Code
                  </label>
                  <input
                    type="password"
                    value={inputPassword}
                    onChange={(e) => setInputPassword(e.target.value)}
                    className="w-full px-4 py-4 border-2 border-gray-300 rounded-xl text-center text-lg focus:border-blue-600 focus:outline-none transition-colors"
                    placeholder="Enter password..."
                    required
                  />
                </div>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-8 rounded-full text-lg font-bold transition-all duration-300 hover:from-blue-700 hover:to-purple-700 hover:transform hover:-translate-y-1 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? 'Authenticating...' : 'Authenticate'}
                </button>
              </form>
            ) : (
              <div className="text-center">
                <div className="text-6xl mb-4">🎉</div>
                <h3 className="text-2xl font-bold text-green-600 mb-2">
                  Access Granted!
                </h3>
                <p className="text-gray-600">
                  Welcome to Yourl.Cloud secure infrastructure
                </p>
              </div>
            )}

            {authMessage && (
              <div className={`mt-4 p-4 rounded-xl text-white font-semibold ${
                authMessage.includes('✅') ? 'bg-green-500' : 'bg-red-500'
              }`}>
                {authMessage}
              </div>
            )}
          </div>

          {/* Current Password Display */}
          {currentPassword && (
            <div className="bg-gradient-to-r from-red-500 to-orange-500 text-white rounded-xl p-6 mb-8 text-center">
              <h3 className="text-xl font-bold mb-2">Current Access Code</h3>
              <div className="text-3xl font-mono font-bold tracking-wider">
                {currentPassword}
              </div>
              <p className="text-sm mt-2 opacity-90">
                Use this code to access the system
              </p>
            </div>
          )}

          {/* Information Section */}
          <div className="bg-blue-50 rounded-xl p-6 mb-8 border-l-4 border-blue-600">
            <h3 className="text-xl font-bold text-blue-800 mb-3">
              About Yourl.Cloud
            </h3>
            <p className="text-blue-700">
              Professional cloud infrastructure and API services designed for modern applications. 
              Our secure platform provides reliable, scalable solutions for businesses and developers.
            </p>
          </div>

          {/* Connections Grid */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Platform Connections
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {connections.map((connection) => (
                <div
                  key={connection.id}
                  className="bg-white p-6 rounded-xl shadow-lg border-t-4 border-blue-600 hover:transform hover:-translate-y-2 transition-all duration-300"
                >
                  <h4 className="text-xl font-bold text-blue-600 mb-3">
                    {connection.name}
                  </h4>
                  <p className="text-gray-600 mb-4">
                    {connection.description}
                  </p>
                  <a
                    href={connection.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 font-semibold hover:underline transition-colors"
                  >
                    Visit Platform →
                  </a>
                </div>
              ))}
            </div>
          </div>

          {/* Status Badges */}
          <div className="text-center mb-8">
            <h3 className="text-xl font-bold text-gray-800 mb-4">
              System Status
            </h3>
            <div className="flex justify-center gap-4 flex-wrap">
              <span className="px-4 py-2 bg-green-100 text-green-800 rounded-full font-semibold text-sm uppercase">
                Operational
              </span>
              <span className="px-4 py-2 bg-blue-100 text-blue-800 rounded-full font-semibold text-sm uppercase">
                Secure
              </span>
              <span className="px-4 py-2 bg-purple-100 text-purple-800 rounded-full font-semibold text-sm uppercase">
                Monitored
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  )
}

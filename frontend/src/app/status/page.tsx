'use client'

import { useState, useEffect } from 'react'
import Footer from '@/components/Footer'

interface StatusData {
  application: string
  version: string
  environment: string
  status: string
  uptime: string
  lastCheck: string
  services: {
    name: string
    status: string
    responseTime: number
  }[]
}

export default function StatusPage() {
  const [statusData, setStatusData] = useState<StatusData | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate fetching status data
    const mockData: StatusData = {
      application: 'Yourl.Cloud API Server',
      version: '1.0.0',
      environment: 'production',
      status: 'operational',
      uptime: '2 days, 14 hours, 32 minutes',
      lastCheck: new Date().toISOString(),
      services: [
        { name: 'Web Server', status: 'operational', responseTime: 45 },
        { name: 'Database', status: 'operational', responseTime: 12 },
        { name: 'Cache', status: 'operational', responseTime: 8 },
        { name: 'External APIs', status: 'operational', responseTime: 156 },
        { name: 'File Storage', status: 'operational', responseTime: 23 },
        { name: 'Monitoring', status: 'operational', responseTime: 34 }
      ]
    }
    
    setStatusData(mockData)
    setIsLoading(false)
  }, [])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-xl">Loading status information...</div>
      </div>
    )
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'operational': return 'text-green-600 bg-green-100'
      case 'degraded': return 'text-yellow-600 bg-yellow-100'
      case 'down': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'operational': return '🟢'
      case 'degraded': return '🟡'
      case 'down': return '🔴'
      default: return '⚪'
    }
  }

  return (
    <div className="min-h-screen">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="bg-white/95 rounded-2xl shadow-2xl p-8 my-8">
          {/* Header */}
          <div className="text-center pb-8 border-b-4 border-blue-600 mb-8">
            <h1 className="text-4xl font-bold text-blue-600 mb-4">
              Application Status
            </h1>
            <p className="text-xl text-gray-600">
              Comprehensive system status and service health
            </p>
          </div>

          {/* Overall Status */}
          <div className="bg-blue-50 rounded-xl p-6 mb-8 border-l-4 border-blue-600">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-blue-800 mb-2">
                  {statusData?.application}
                </h2>
                <p className="text-blue-600">
                  Version {statusData?.version} • {statusData?.environment}
                </p>
              </div>
              <div className="text-right">
                <div className="text-3xl mb-2">🟢</div>
                <span className="text-2xl font-bold text-green-600 capitalize">
                  {statusData?.status}
                </span>
              </div>
            </div>
          </div>

          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white p-6 rounded-xl shadow-lg text-center">
              <div className="text-3xl mb-2">⏱️</div>
              <h3 className="text-lg font-bold text-gray-800 mb-2">Uptime</h3>
              <p className="text-2xl font-bold text-blue-600">
                {statusData?.uptime}
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-lg text-center">
              <div className="text-3xl mb-2">🔄</div>
              <h3 className="text-lg font-bold text-gray-800 mb-2">Last Check</h3>
              <p className="text-lg font-bold text-gray-600">
                {statusData?.lastCheck ? new Date(statusData.lastCheck).toLocaleTimeString() : 'N/A'}
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-lg text-center">
              <div className="text-3xl mb-2">📊</div>
              <h3 className="text-lg font-bold text-gray-800 mb-2">Services</h3>
              <p className="text-2xl font-bold text-green-600">
                {statusData?.services.filter(s => s.status === 'operational').length}/{statusData?.services.length}
              </p>
            </div>
          </div>

          {/* Service Status */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Service Status
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {statusData?.services.map((service, index) => (
                <div
                  key={index}
                  className="bg-white p-6 rounded-xl shadow-lg border-l-4 border-blue-600"
                >
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="text-xl font-bold text-gray-800">
                      {service.name}
                    </h4>
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">{getStatusIcon(service.status)}</span>
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold capitalize ${getStatusColor(service.status)}`}>
                        {service.status}
                      </span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Response Time:</span>
                    <span className="font-mono font-bold text-lg text-blue-600">
                      {service.responseTime}ms
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Performance Indicators */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Performance Indicators
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-gradient-to-r from-green-400 to-green-600 text-white p-4 rounded-xl text-center">
                <div className="text-2xl font-bold">99.9%</div>
                <div className="text-sm opacity-90">Uptime</div>
              </div>
              <div className="bg-gradient-to-r from-blue-400 to-blue-600 text-white p-4 rounded-xl text-center">
                <div className="text-2xl font-bold">45ms</div>
                <div className="text-sm opacity-90">Avg Response</div>
              </div>
              <div className="bg-gradient-to-r from-purple-400 to-purple-600 text-white p-4 rounded-xl text-center">
                <div className="text-2xl font-bold">1.2K</div>
                <div className="text-sm opacity-90">Requests/min</div>
              </div>
              <div className="bg-gradient-to-r from-orange-400 to-orange-600 text-white p-4 rounded-xl text-center">
                <div className="text-2xl font-bold">256</div>
                <div className="text-sm opacity-90">Active Users</div>
              </div>
            </div>
          </div>

          {/* Status Summary */}
          <div className="text-center">
            <h3 className="text-xl font-bold text-gray-800 mb-4">
              System Summary
            </h3>
            <div className="flex justify-center gap-4 flex-wrap">
              <span className="px-6 py-3 bg-green-100 text-green-800 rounded-full font-semibold text-lg uppercase">
                All Services Operational
              </span>
              <span className="px-6 py-3 bg-blue-100 text-blue-800 rounded-full font-semibold text-lg uppercase">
                Performance Optimal
              </span>
              <span className="px-6 py-3 bg-purple-100 text-purple-800 rounded-full font-semibold text-lg uppercase">
                Monitoring Active
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  )
}



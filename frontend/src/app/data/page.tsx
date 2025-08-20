'use client'

import { useState, useEffect } from 'react'
import Footer from '@/components/Footer'

interface DataStream {
  id: string
  type: string
  value: number
  timestamp: string
  status: 'active' | 'inactive' | 'error'
}

interface AnalyticsData {
  totalRecords: number
  activeStreams: number
  dataVolume: string
  lastUpdate: string
  streams: DataStream[]
}

export default function DataPage() {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [selectedStream, setSelectedStream] = useState<string | null>(null)

  useEffect(() => {
    // Simulate fetching analytics data
    const mockData: AnalyticsData = {
      totalRecords: 15420,
      activeStreams: 8,
      dataVolume: '2.4 GB',
      lastUpdate: new Date().toISOString(),
      streams: [
        {
          id: '1',
          type: 'User Activity',
          value: 1250,
          timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
          status: 'active'
        },
        {
          id: '2',
          type: 'System Metrics',
          value: 890,
          timestamp: new Date(Date.now() - 1000 * 60 * 3).toISOString(),
          status: 'active'
        },
        {
          id: '3',
          type: 'API Requests',
          value: 2100,
          timestamp: new Date(Date.now() - 1000 * 60 * 2).toISOString(),
          status: 'active'
        },
        {
          id: '4',
          type: 'Database Queries',
          value: 567,
          timestamp: new Date(Date.now() - 1000 * 60 * 4).toISOString(),
          status: 'active'
        },
        {
          id: '5',
          type: 'Error Logs',
          value: 23,
          timestamp: new Date(Date.now() - 1000 * 60 * 1).toISOString(),
          status: 'active'
        },
        {
          id: '6',
          type: 'Performance Metrics',
          value: 445,
          timestamp: new Date(Date.now() - 1000 * 60 * 6).toISOString(),
          status: 'inactive'
        },
        {
          id: '7',
          type: 'Security Events',
          value: 12,
          timestamp: new Date(Date.now() - 1000 * 60 * 8).toISOString(),
          status: 'active'
        },
        {
          id: '8',
          type: 'Backup Status',
          value: 1,
          timestamp: new Date(Date.now() - 1000 * 60 * 10).toISOString(),
          status: 'active'
        }
      ]
    }
    
    setAnalyticsData(mockData)
    setIsLoading(false)
  }, [])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-xl">Loading data analytics...</div>
      </div>
    )
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100'
      case 'inactive': return 'text-gray-600 bg-gray-100'
      case 'error': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return '🟢'
      case 'inactive': return '⚪'
      case 'error': return '🔴'
      default: return '⚪'
    }
  }

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white/95 rounded-2xl shadow-2xl p-8 my-8">
          {/* Header */}
          <div className="text-center pb-8 border-b-4 border-green-600 mb-8">
            <h1 className="text-4xl font-bold text-green-600 mb-4">
              Data Analytics Dashboard
            </h1>
            <p className="text-xl text-gray-600">
              Real-time data streams and analytics insights
            </p>
          </div>

          {/* Overview Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-gradient-to-r from-blue-400 to-blue-600 text-white p-6 rounded-xl text-center">
              <div className="text-3xl font-bold mb-2">
                {analyticsData?.totalRecords.toLocaleString()}
              </div>
              <div className="text-sm opacity-90">Total Records</div>
            </div>
            <div className="bg-gradient-to-r from-green-400 to-green-600 text-white p-6 rounded-xl text-center">
              <div className="text-3xl font-bold mb-2">
                {analyticsData?.activeStreams}
              </div>
              <div className="text-sm opacity-90">Active Streams</div>
            </div>
            <div className="bg-gradient-to-r from-purple-400 to-purple-600 text-white p-6 rounded-xl text-center">
              <div className="text-3xl font-bold mb-2">
                {analyticsData?.dataVolume}
              </div>
              <div className="text-sm opacity-90">Data Volume</div>
            </div>
            <div className="bg-gradient-to-r from-orange-400 to-orange-600 text-white p-6 rounded-xl text-center">
              <div className="text-3xl font-bold mb-2">
                {analyticsData?.streams.filter(s => s.status === 'active').length}
              </div>
              <div className="text-sm opacity-90">Live Streams</div>
            </div>
          </div>

          {/* Data Streams */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Data Streams
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {analyticsData?.streams.map((stream) => (
                <div
                  key={stream.id}
                  className={`bg-white p-6 rounded-xl shadow-lg border-l-4 border-blue-600 cursor-pointer transition-all duration-300 hover:shadow-xl hover:transform hover:-translate-y-1 ${
                    selectedStream === stream.id ? 'ring-2 ring-blue-400' : ''
                  }`}
                  onClick={() => setSelectedStream(selectedStream === stream.id ? null : stream.id)}
                >
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="text-xl font-bold text-gray-800">
                      {stream.type}
                    </h4>
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">{getStatusIcon(stream.status)}</span>
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold capitalize ${getStatusColor(stream.status)}`}>
                        {stream.status}
                      </span>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Value:</span>
                      <span className="font-mono font-bold text-lg text-blue-600">
                        {stream.value.toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Last Update:</span>
                      <span className="text-sm font-mono text-gray-600">
                        {new Date(stream.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Data Visualization */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Data Trends
            </h2>
            <div className="bg-gray-50 rounded-xl p-8 text-center">
              <div className="text-6xl mb-4">📊</div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">
                Real-time Data Visualization
              </h3>
              <p className="text-gray-600 mb-4">
                Interactive charts and graphs showing data trends over time
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white p-4 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600 mb-1">24h</div>
                  <div className="text-sm text-gray-600">Time Range</div>
                </div>
                <div className="bg-white p-4 rounded-lg">
                  <div className="text-2xl font-bold text-green-600 mb-1">1min</div>
                  <div className="text-sm text-gray-600">Update Interval</div>
                </div>
                <div className="bg-white p-4 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600 mb-1">8</div>
                  <div className="text-sm text-gray-600">Active Streams</div>
                </div>
              </div>
            </div>
          </div>

          {/* Data Processing */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Data Processing Pipeline
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-white p-6 rounded-xl shadow-lg text-center border-t-4 border-blue-600">
                <div className="text-4xl mb-2">📥</div>
                <h4 className="text-lg font-bold text-gray-800 mb-2">Ingestion</h4>
                <p className="text-sm text-gray-600">Data collection from multiple sources</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-lg text-center border-t-4 border-green-600">
                <div className="text-4xl mb-2">🔧</div>
                <h4 className="text-lg font-bold text-gray-800 mb-2">Processing</h4>
                <p className="text-sm text-gray-600">Real-time data transformation</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-lg text-center border-t-4 border-purple-600">
                <div className="text-4xl mb-2">💾</div>
                <h4 className="text-lg font-bold text-gray-800 mb-2">Storage</h4>
                <p className="text-sm text-gray-600">Efficient data persistence</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-lg text-center border-t-4 border-orange-600">
                <div className="text-4xl mb-2">📤</div>
                <h4 className="text-lg font-bold text-gray-800 mb-2">Delivery</h4>
                <p className="text-sm text-gray-600">API access and analytics</p>
              </div>
            </div>
          </div>

          {/* Last Update */}
          <div className="text-center">
            <h3 className="text-xl font-bold text-gray-800 mb-4">
              Data Status
            </h3>
            <div className="flex justify-center gap-4 flex-wrap">
              <span className="px-6 py-3 bg-green-100 text-green-800 rounded-full font-semibold text-lg uppercase">
                All Streams Active
              </span>
              <span className="px-6 py-3 bg-blue-100 text-blue-800 rounded-full font-semibold text-lg uppercase">
                Real-time Updates
              </span>
              <span className="px-6 py-3 bg-purple-100 text-purple-800 rounded-full font-semibold text-lg uppercase">
                Analytics Ready
              </span>
            </div>
            <p className="text-gray-600 mt-4">
              Last updated: {analyticsData?.lastUpdate ? new Date(analyticsData.lastUpdate).toLocaleString() : 'N/A'}
            </p>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  )
}



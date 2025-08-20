'use client'

import { useState, useEffect } from 'react'
import Footer from '@/components/Footer'

interface MonitoringData {
  system: {
    cpu: number
    memory: number
    disk: number
    network: number
  }
  performance: {
    responseTime: number
    throughput: number
    errorRate: number
    uptime: number
  }
  alerts: {
    id: string
    level: 'info' | 'warning' | 'critical'
    message: string
    timestamp: string
  }[]
}

export default function MonitoringPage() {
  const [monitoringData, setMonitoringData] = useState<MonitoringData | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate fetching monitoring data
    const mockData: MonitoringData = {
      system: {
        cpu: 23,
        memory: 67,
        disk: 45,
        network: 12
      },
      performance: {
        responseTime: 45,
        throughput: 1200,
        errorRate: 0.1,
        uptime: 99.9
      },
      alerts: [
        {
          id: '1',
          level: 'info',
          message: 'System backup completed successfully',
          timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString()
        },
        {
          id: '2',
          level: 'warning',
          message: 'Memory usage approaching threshold',
          timestamp: new Date(Date.now() - 1000 * 60 * 15).toISOString()
        },
        {
          id: '3',
          level: 'info',
          message: 'Database connection pool optimized',
          timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString()
        }
      ]
    }
    
    setMonitoringData(mockData)
    setIsLoading(false)
  }, [])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-xl">Loading monitoring data...</div>
      </div>
    )
  }

  const getAlertColor = (level: string) => {
    switch (level) {
      case 'info': return 'bg-blue-100 text-blue-800 border-blue-200'
      case 'warning': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'critical': return 'bg-red-100 text-red-800 border-red-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getAlertIcon = (level: string) => {
    switch (level) {
      case 'info': return 'ℹ️'
      case 'warning': return '⚠️'
      case 'critical': return '🚨'
      default: return 'ℹ️'
    }
  }

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white/95 rounded-2xl shadow-2xl p-8 my-8">
          {/* Header */}
          <div className="text-center pb-8 border-b-4 border-purple-600 mb-8">
            <h1 className="text-4xl font-bold text-purple-600 mb-4">
              System Monitoring Dashboard
            </h1>
            <p className="text-xl text-gray-600">
              Real-time system performance and health monitoring
            </p>
          </div>

          {/* System Metrics */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              System Resources
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-xl shadow-lg text-center">
                <div className="text-4xl mb-2">🖥️</div>
                <h3 className="text-lg font-bold text-gray-800 mb-2">CPU Usage</h3>
                <div className="text-3xl font-bold text-blue-600 mb-2">
                  {monitoringData?.system.cpu}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${monitoringData?.system.cpu}%` }}
                  ></div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-lg text-center">
                <div className="text-4xl mb-2">💾</div>
                <h3 className="text-lg font-bold text-gray-800 mb-2">Memory Usage</h3>
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {monitoringData?.system.memory}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${monitoringData?.system.memory}%` }}
                  ></div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-lg text-center">
                <div className="text-4xl mb-2">💿</div>
                <h3 className="text-lg font-bold text-gray-800 mb-2">Disk Usage</h3>
                <div className="text-3xl font-bold text-orange-600 mb-2">
                  {monitoringData?.system.disk}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-orange-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${monitoringData?.system.disk}%` }}
                  ></div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-lg text-center">
                <div className="text-4xl mb-2">🌐</div>
                <h3 className="text-lg font-bold text-gray-800 mb-2">Network</h3>
                <div className="text-3xl font-bold text-purple-600 mb-2">
                  {monitoringData?.system.network}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${monitoringData?.system.network}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Performance Metrics
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-gradient-to-r from-blue-400 to-blue-600 text-white p-6 rounded-xl text-center">
                <div className="text-3xl font-bold mb-2">
                  {monitoringData?.performance.responseTime}ms
                </div>
                <div className="text-sm opacity-90">Response Time</div>
              </div>
              <div className="bg-gradient-to-r from-green-400 to-green-600 text-white p-6 rounded-xl text-center">
                <div className="text-3xl font-bold mb-2">
                  {monitoringData?.performance.throughput}/min
                </div>
                <div className="text-sm opacity-90">Throughput</div>
              </div>
              <div className="bg-gradient-to-r from-red-400 to-red-600 text-white p-6 rounded-xl text-center">
                <div className="text-3xl font-bold mb-2">
                  {monitoringData?.performance.errorRate}%
                </div>
                <div className="text-sm opacity-90">Error Rate</div>
              </div>
              <div className="bg-gradient-to-r from-purple-400 to-purple-600 text-white p-6 rounded-xl text-center">
                <div className="text-3xl font-bold mb-2">
                  {monitoringData?.performance.uptime}%
                </div>
                <div className="text-sm opacity-90">Uptime</div>
              </div>
            </div>
          </div>

          {/* Alerts */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Recent Alerts
            </h2>
            <div className="space-y-4">
              {monitoringData?.alerts.map((alert) => (
                <div
                  key={alert.id}
                  className={`p-4 rounded-xl border-l-4 ${getAlertColor(alert.level)}`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{getAlertIcon(alert.level)}</span>
                    <div className="flex-1">
                      <p className="font-semibold">{alert.message}</p>
                      <p className="text-sm opacity-75">
                        {new Date(alert.timestamp).toLocaleString()}
                      </p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold capitalize ${getAlertColor(alert.level)}`}>
                      {alert.level}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Monitoring Status */}
          <div className="text-center">
            <h3 className="text-xl font-bold text-gray-800 mb-4">
              Monitoring Status
            </h3>
            <div className="flex justify-center gap-4 flex-wrap">
              <span className="px-6 py-3 bg-green-100 text-green-800 rounded-full font-semibold text-lg uppercase">
                All Systems Monitored
              </span>
              <span className="px-6 py-3 bg-blue-100 text-blue-800 rounded-full font-semibold text-lg uppercase">
                Real-time Updates
              </span>
              <span className="px-6 py-3 bg-purple-100 text-purple-800 rounded-full font-semibold text-lg uppercase">
                Alerts Active
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  )
}



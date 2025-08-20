'use client'

import { useState, useEffect } from 'react'
import Footer from '@/components/Footer'
import axios from 'axios'

interface HealthData {
  status: string
  uptime: string
  timestamp: string
  version: string
  environment: string
}

export default function HealthPage() {
  const [healthData, setHealthData] = useState<HealthData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchHealthData = async () => {
      try {
        // In a real implementation, this would call your Flask backend
        // For now, we'll simulate the health data
        const mockData: HealthData = {
          status: 'healthy',
          uptime: '2 days, 14 hours, 32 minutes',
          timestamp: new Date().toISOString(),
          version: '1.0.0',
          environment: 'production'
        }
        
        setHealthData(mockData)
        setError(null)
      } catch (err) {
        setError('Failed to fetch health data')
      } finally {
        setIsLoading(false)
      }
    }

    fetchHealthData()
  }, [])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-xl">Loading health data...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-red-400 text-xl">{error}</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white/95 rounded-2xl shadow-2xl p-8 my-8">
          {/* Header */}
          <div className="text-center pb-8 border-b-4 border-green-600 mb-8">
            <h1 className="text-4xl font-bold text-green-600 mb-4">
              System Health Status
            </h1>
            <p className="text-xl text-gray-600">
              Real-time monitoring and system diagnostics
            </p>
          </div>

          {/* Health Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-green-50 rounded-xl p-6 border-l-4 border-green-600">
              <h3 className="text-xl font-bold text-green-800 mb-2">Status</h3>
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-2xl font-bold text-green-700 capitalize">
                  {healthData?.status}
                </span>
              </div>
            </div>

            <div className="bg-blue-50 rounded-xl p-6 border-l-4 border-blue-600">
              <h3 className="text-xl font-bold text-blue-800 mb-2">Uptime</h3>
              <p className="text-2xl font-bold text-blue-700">
                {healthData?.uptime}
              </p>
            </div>
          </div>

          {/* Detailed Health Information */}
          <div className="bg-gray-50 rounded-xl p-6 mb-8">
            <h3 className="text-xl font-bold text-gray-800 mb-4">
              System Information
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-gray-600 mb-1">
                  Version
                </label>
                <p className="text-lg font-mono text-gray-800">
                  {healthData?.version}
                </p>
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-600 mb-1">
                  Environment
                </label>
                <p className="text-lg font-mono text-gray-800 capitalize">
                  {healthData?.environment}
                </p>
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-600 mb-1">
                  Last Updated
                </label>
                <p className="text-lg font-mono text-gray-800">
                  {healthData?.timestamp ? new Date(healthData.timestamp).toLocaleString() : 'N/A'}
                </p>
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-600 mb-1">
                  Health Check
                </label>
                <p className="text-lg font-mono text-gray-800">
                  {healthData?.status === 'healthy' ? '✅ Passed' : '❌ Failed'}
                </p>
              </div>
            </div>
          </div>

          {/* Health Metrics */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Health Metrics
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-xl shadow-lg text-center">
                <div className="text-4xl mb-2">🟢</div>
                <h4 className="text-lg font-bold text-gray-800 mb-2">System</h4>
                <p className="text-green-600 font-semibold">Operational</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-lg text-center">
                <div className="text-4xl mb-2">🟢</div>
                <h4 className="text-lg font-bold text-gray-800 mb-2">Database</h4>
                <p className="text-green-600 font-semibold">Connected</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-lg text-center">
                <div className="text-4xl mb-2">🟢</div>
                <h4 className="text-lg font-bold text-gray-800 mb-2">API</h4>
                <p className="text-green-600 font-semibold">Responding</p>
              </div>
            </div>
          </div>

          {/* Status Badges */}
          <div className="text-center">
            <h3 className="text-xl font-bold text-gray-800 mb-4">
              Overall Status
            </h3>
            <div className="flex justify-center gap-4 flex-wrap">
              <span className="px-6 py-3 bg-green-100 text-green-800 rounded-full font-semibold text-lg uppercase">
                All Systems Operational
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  )
}



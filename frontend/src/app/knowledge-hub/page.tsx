'use client'

import { useState, useEffect } from 'react'
import Footer from '@/components/Footer'

interface DocumentationItem {
  id: string
  title: string
  description: string
  category: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  tags: string[]
  lastUpdated: string
}

interface KnowledgeData {
  categories: string[]
  totalDocs: number
  lastUpdate: string
  documents: DocumentationItem[]
}

export default function KnowledgeHubPage() {
  const [knowledgeData, setKnowledgeData] = useState<KnowledgeData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    // Simulate fetching knowledge data
    const mockData: KnowledgeData = {
      categories: ['API', 'Deployment', 'Security', 'Monitoring', 'Development'],
      totalDocs: 24,
      lastUpdate: new Date().toISOString(),
      documents: [
        {
          id: '1',
          title: 'Getting Started with Yourl.Cloud API',
          description: 'Complete guide to integrating with Yourl.Cloud services and APIs',
          category: 'API',
          difficulty: 'beginner',
          tags: ['api', 'integration', 'tutorial'],
          lastUpdated: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString()
        },
        {
          id: '2',
          title: 'Deployment Best Practices',
          description: 'Learn the best practices for deploying applications to Google Cloud Run',
          category: 'Deployment',
          difficulty: 'intermediate',
          tags: ['deployment', 'cloud-run', 'best-practices'],
          lastUpdated: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString()
        },
        {
          id: '3',
          title: 'Security Configuration Guide',
          description: 'Comprehensive security setup and configuration for production environments',
          category: 'Security',
          difficulty: 'advanced',
          tags: ['security', 'configuration', 'production'],
          lastUpdated: new Date(Date.now() - 1000 * 60 * 60 * 72).toISOString()
        },
        {
          id: '4',
          title: 'System Monitoring Setup',
          description: 'How to set up comprehensive monitoring and alerting for your infrastructure',
          category: 'Monitoring',
          difficulty: 'intermediate',
          tags: ['monitoring', 'alerting', 'infrastructure'],
          lastUpdated: new Date(Date.now() - 1000 * 60 * 60 * 96).toISOString()
        },
        {
          id: '5',
          title: 'Development Workflow',
          description: 'Streamlined development workflow from local development to production',
          category: 'Development',
          difficulty: 'beginner',
          tags: ['workflow', 'development', 'local'],
          lastUpdated: new Date(Date.now() - 1000 * 60 * 60 * 120).toISOString()
        },
        {
          id: '6',
          title: 'API Authentication Methods',
          description: 'Different authentication methods and their implementation',
          category: 'API',
          difficulty: 'intermediate',
          tags: ['authentication', 'api', 'security'],
          lastUpdated: new Date(Date.now() - 1000 * 60 * 60 * 144).toISOString()
        },
        {
          id: '7',
          title: 'Database Integration Guide',
          description: 'How to integrate and optimize database connections',
          category: 'Development',
          difficulty: 'intermediate',
          tags: ['database', 'integration', 'optimization'],
          lastUpdated: new Date(Date.now() - 1000 * 60 * 60 * 168).toISOString()
        },
        {
          id: '8',
          title: 'Performance Optimization',
          description: 'Advanced techniques for optimizing application performance',
          category: 'Development',
          difficulty: 'advanced',
          tags: ['performance', 'optimization', 'advanced'],
          lastUpdated: new Date(Date.now() - 1000 * 60 * 60 * 192).toISOString()
        }
      ]
    }
    
    setKnowledgeData(mockData)
    setIsLoading(false)
  }, [])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-xl">Loading knowledge hub...</div>
      </div>
    )
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-800'
      case 'intermediate': return 'bg-yellow-100 text-yellow-800'
      case 'advanced': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const filteredDocuments = knowledgeData?.documents.filter(doc => {
    const matchesCategory = selectedCategory === 'all' || doc.category === selectedCategory
    const matchesSearch = doc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         doc.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         doc.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
    return matchesCategory && matchesSearch
  }) || []

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white/95 rounded-2xl shadow-2xl p-8 my-8">
          {/* Header */}
          <div className="text-center pb-8 border-b-4 border-indigo-600 mb-8">
            <h1 className="text-4xl font-bold text-indigo-600 mb-4">
              Knowledge Hub
            </h1>
            <p className="text-xl text-gray-600">
              Comprehensive documentation and learning resources
            </p>
          </div>

          {/* Search and Filter */}
          <div className="mb-8">
            <div className="flex flex-col md:flex-row gap-4 mb-6">
              <div className="flex-1">
                <input
                  type="text"
                  placeholder="Search documentation..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-indigo-600 focus:outline-none transition-colors"
                />
              </div>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-indigo-600 focus:outline-none transition-colors"
              >
                <option value="all">All Categories</option>
                {knowledgeData?.categories.map((category) => (
                  <option key={category} value={category}>{category}</option>
                ))}
              </select>
            </div>
            
            <div className="text-center">
              <span className="text-gray-600">
                Showing {filteredDocuments.length} of {knowledgeData?.totalDocs} documents
              </span>
            </div>
          </div>

          {/* Category Pills */}
          <div className="mb-8">
            <h3 className="text-lg font-bold text-gray-800 mb-4 text-center">
              Browse by Category
            </h3>
            <div className="flex justify-center flex-wrap gap-3">
              <button
                onClick={() => setSelectedCategory('all')}
                className={`px-4 py-2 rounded-full font-semibold transition-all duration-300 ${
                  selectedCategory === 'all'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                All ({knowledgeData?.totalDocs})
              </button>
              {knowledgeData?.categories.map((category) => {
                const count = knowledgeData.documents.filter(doc => doc.category === category).length
                return (
                  <button
                    key={category}
                    onClick={() => setSelectedCategory(category)}
                    className={`px-4 py-2 rounded-full font-semibold transition-all duration-300 ${
                      selectedCategory === category
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    {category} ({count})
                  </button>
                )
              })}
            </div>
          </div>

          {/* Documentation Grid */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Documentation
            </h2>
            {filteredDocuments.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🔍</div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">No documents found</h3>
                <p className="text-gray-600">Try adjusting your search or filter criteria</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredDocuments.map((doc) => (
                  <div
                    key={doc.id}
                    className="bg-white p-6 rounded-xl shadow-lg border-l-4 border-indigo-600 hover:shadow-xl transition-all duration-300 cursor-pointer"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <h4 className="text-xl font-bold text-gray-800 flex-1 mr-3">
                        {doc.title}
                      </h4>
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold capitalize ${getDifficultyColor(doc.difficulty)}`}>
                        {doc.difficulty}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-4 line-clamp-3">
                      {doc.description}
                    </p>
                    <div className="mb-4">
                      <span className="text-sm font-semibold text-indigo-600">
                        {doc.category}
                      </span>
                    </div>
                    <div className="flex flex-wrap gap-2 mb-4">
                      {doc.tags.map((tag, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                    <div className="text-xs text-gray-500">
                      Updated: {new Date(doc.lastUpdated).toLocaleDateString()}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Quick Links */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Quick Links
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gradient-to-r from-blue-400 to-blue-600 text-white p-6 rounded-xl text-center">
                <div className="text-4xl mb-2">📚</div>
                <h3 className="text-lg font-bold mb-2">API Reference</h3>
                <p className="text-sm opacity-90">Complete API documentation</p>
              </div>
              <div className="bg-gradient-to-r from-green-400 to-green-600 text-white p-6 rounded-xl text-center">
                <div className="text-4xl mb-2">🚀</div>
                <h3 className="text-lg font-bold mb-2">Deployment Guide</h3>
                <p className="text-sm opacity-90">Step-by-step deployment</p>
              </div>
              <div className="bg-gradient-to-r from-purple-400 to-purple-600 text-white p-6 rounded-xl text-center">
                <div className="text-4xl mb-2">🛡️</div>
                <h3 className="text-lg font-bold mb-2">Security</h3>
                <p className="text-sm opacity-90">Security best practices</p>
              </div>
            </div>
          </div>

          {/* Knowledge Hub Status */}
          <div className="text-center">
            <h3 className="text-xl font-bold text-gray-800 mb-4">
              Knowledge Hub Status
            </h3>
            <div className="flex justify-center gap-4 flex-wrap">
              <span className="px-6 py-3 bg-green-100 text-green-800 rounded-full font-semibold text-lg uppercase">
                {filteredDocuments.length} Documents Available
              </span>
              <span className="px-6 py-3 bg-blue-100 text-blue-800 rounded-full font-semibold text-lg uppercase">
                {knowledgeData?.categories.length} Categories
              </span>
              <span className="px-6 py-3 bg-purple-100 text-purple-800 rounded-full font-semibold text-lg uppercase">
                Always Updated
              </span>
            </div>
            <p className="text-gray-600 mt-4">
              Last updated: {knowledgeData?.lastUpdate ? new Date(knowledgeData.lastUpdate).toLocaleString() : 'N/A'}
            </p>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  )
}



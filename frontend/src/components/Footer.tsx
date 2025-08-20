'use client'

import Link from 'next/link'

const Footer = () => {
  const navLinks = [
    { href: '/', label: 'Home', description: 'Main landing page' },
    { href: '/health', label: 'Health', description: 'System health status' },
    { href: '/status', label: 'Status', description: 'Application status' },
    { href: '/monitoring', label: 'Monitoring', description: 'System monitoring dashboard' },
    { href: '/data', label: 'Data', description: 'Data stream and analytics' },
    { href: '/knowledge-hub', label: 'Knowledge Hub', description: 'Documentation and resources' },
  ]

  return (
    <footer className="bg-white/95 border-t-2 border-blue-200 mt-12">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Navigation Links */}
        <div className="text-center mb-6">
          <h4 className="text-blue-600 text-xl font-semibold mb-4">
            Navigation
          </h4>
          <div className="flex justify-center flex-wrap gap-3 mb-6">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="inline-block px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-sm font-semibold rounded-full transition-all duration-300 hover:from-blue-700 hover:to-purple-700 hover:transform hover:-translate-y-1 hover:shadow-lg"
                title={link.description}
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>

        {/* Company Info */}
        <div className="border-t border-gray-200 pt-6 text-center">
          <div className="text-gray-600 text-sm">
            <p className="font-semibold text-blue-600 mb-2">Yourl.Cloud Inc.</p>
            <p>Secure Cloud Infrastructure & API Services</p>
            <p className="mt-2 text-xs text-gray-500">
              Professional cloud solutions for modern applications
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer



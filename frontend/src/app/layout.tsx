import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Yourl.Cloud - Secure Cloud Infrastructure & API Services',
  description: 'Professional cloud infrastructure and API services with secure authentication and monitoring capabilities.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-br from-blue-600 to-purple-700">
          {children}
        </div>
      </body>
    </html>
  )
}

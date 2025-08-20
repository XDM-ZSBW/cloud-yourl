import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    // In a real implementation, this would call your Flask backend
    // For now, we'll simulate the password generation logic
    const words = ["CLOUD", "FUTURE", "INNOVATE", "DREAM", "BUILD", "CREATE"]
    const symbols = ["!", "@", "#", "$", "%", "&"]
    
    // Use a consistent seed for demo purposes
    const timestamp = Math.floor(Date.now() / (1000 * 60 * 60 * 24)) // Daily rotation
    const hashNum = timestamp % 1000000
    
    const word = words[hashNum % words.length]
    const symbol = symbols[hashNum % symbols.length]
    const number = (hashNum % 900) + 100
    
    const password = `${word}${number}${symbol}`
    
    return NextResponse.json({ 
      password,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to generate password' },
      { status: 500 }
    )
  }
}



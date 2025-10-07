import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-primary-400">
            Bloomberg Terminal for the Everyman
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
            Institutional-grade market intelligence at retail pricing
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              href="/digest"
              className="bg-primary-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
            >
              View Today's Digest
            </Link>
            <Link
              href="/stocks"
              className="bg-white dark:bg-gray-800 text-primary-600 dark:text-primary-400 px-8 py-3 rounded-lg font-semibold border-2 border-primary-600 hover:bg-primary-50 dark:hover:bg-gray-700 transition-colors"
            >
              Browse Stocks
            </Link>
          </div>
        </div>

        {/* Value Propositions */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg">
            <div className="text-3xl mb-4"></div>
            <h3 className="text-xl font-semibold mb-2">$0-50/month</h3>
            <p className="text-gray-600 dark:text-gray-400">
              vs $24,000/year for Bloomberg Terminal
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg">
            <div className="text-3xl mb-4"></div>
            <h3 className="text-xl font-semibold mb-2">20 Minutes/Day</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Everything you need to know in one daily digest
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg">
            <div className="text-3xl mb-4"></div>
            <h3 className="text-xl font-semibold mb-2">ONE Recommendation</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Confident, actionable insights - not overwhelming data
            </p>
          </div>
        </div>

        {/* Features Overview */}
        <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold mb-6">What You Get Daily</h2>
          <ul className="space-y-4">
            <li className="flex items-start">
              <span className="text-bullish mr-3"></span>
              <div>
                <strong>Market Overnight Summary</strong> - What moved and why
              </div>
            </li>
            <li className="flex items-start">
              <span className="text-bullish mr-3"></span>
              <div>
                <strong>Top Recommendation</strong> - Full reasoning, catalyst, risk/reward, position sizing
              </div>
            </li>
            <li className="flex items-start">
              <span className="text-bullish mr-3"></span>
              <div>
                <strong>Watch List</strong> - 2-3 stocks to monitor
              </div>
            </li>
            <li className="flex items-start">
              <span className="text-bullish mr-3"></span>
              <div>
                <strong>Key Events</strong> - Earnings, Fed speeches, data releases
              </div>
            </li>
            <li className="flex items-start">
              <span className="text-bullish mr-3"></span>
              <div>
                <strong>Attribution Engine</strong> - Understand WHY stocks move, not just WHAT happened
              </div>
            </li>
          </ul>
        </div>

        {/* Status */}
        <div className="mt-16 text-center text-gray-500 dark:text-gray-400">
          <p>Status: Pre-MVP - Development in Progress</p>
          <p className="text-sm mt-2">Built byChristopher C. Parker | Side Project → Post-Grad Focus</p>
        </div>
      </div>
    </main>
  )
}

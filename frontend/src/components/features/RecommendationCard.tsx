/**
 * The main recommendation card - The ONE pick of the day
 */

interface RecommendationCardProps {
  ticker: string
  name: string
  action: string
  price: number
  target: number
  stopLoss: number
  totalScore: number
  reasoning: string
  catalyst: string
  riskReward: number
  positionSize: string
}

export default function RecommendationCard({
  ticker,
  name,
  action,
  price,
  target,
  stopLoss,
  totalScore,
  reasoning,
  catalyst,
  riskReward,
  positionSize,
}: RecommendationCardProps) {
  const upside = ((target - price) / price) * 100
  const downside = ((price - stopLoss) / price) * 100

  const actionColor =
    action === 'BUY' || action === 'STRONG BUY'
      ? 'text-bullish'
      : action === 'SELL'
      ? 'text-bearish'
      : 'text-neutral'

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border-l-4 border-primary-500">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <h2 className="text-3xl font-bold">{ticker}</h2>
          <p className="text-gray-600 dark:text-gray-400">{name}</p>
        </div>
        <div className="text-right">
          <div className={`text-2xl font-bold ${actionColor}`}>{action}</div>
          <div className="text-sm text-gray-500">Score: {totalScore}/10</div>
        </div>
      </div>

      {/* Price Targets */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Current</div>
          <div className="text-2xl font-bold">${price.toFixed(2)}</div>
        </div>
        <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Target</div>
          <div className="text-2xl font-bold text-bullish">${target.toFixed(2)}</div>
          <div className="text-xs text-bullish">+{upside.toFixed(1)}%</div>
        </div>
        <div className="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg">
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Stop Loss</div>
          <div className="text-2xl font-bold text-bearish">${stopLoss.toFixed(2)}</div>
          <div className="text-xs text-bearish">-{downside.toFixed(1)}%</div>
        </div>
      </div>

      {/* Risk/Reward & Position Size */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg">
          <div className="text-sm text-gray-600 dark:text-gray-400">Risk/Reward</div>
          <div className="text-xl font-bold text-primary-600">{riskReward.toFixed(1)}x</div>
        </div>
        <div className="bg-purple-50 dark:bg-purple-900/20 p-3 rounded-lg">
          <div className="text-sm text-gray-600 dark:text-gray-400">Position Size</div>
          <div className="text-xl font-bold text-purple-600">{positionSize}</div>
        </div>
      </div>

      {/* Catalyst */}
      <div className="mb-4">
        <h3 className="font-semibold mb-2 text-sm text-gray-600 dark:text-gray-400">
          CATALYST
        </h3>
        <p className="text-gray-800 dark:text-gray-200 bg-yellow-50 dark:bg-yellow-900/20 p-3 rounded-lg">
          {catalyst}
        </p>
      </div>

      {/* Reasoning */}
      <div>
        <h3 className="font-semibold mb-2 text-sm text-gray-600 dark:text-gray-400">
          REASONING
        </h3>
        <p className="text-gray-800 dark:text-gray-200">{reasoning}</p>
      </div>
    </div>
  )
}

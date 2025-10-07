/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Environment variables exposed to the browser
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },

  // PWA configuration (for mobile-first experience)
  // You'll need to install next-pwa: npm install next-pwa
  // Uncomment when ready to add PWA features:
  // pwa: {
  //   dest: 'public',
  //   disable: process.env.NODE_ENV === 'development',
  // },
}

module.exports = nextConfig

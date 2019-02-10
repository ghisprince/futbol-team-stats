module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        pathRewrite: {
          '^/api': '/futbol/api'
        },
        xfwd: true
      }
    }
  },
  outputDir: 'dist',
  assetsDir: 'static',
  baseUrl: process.env.NODE_ENV === 'production'
    ? '/futbol'
    : '/'
}

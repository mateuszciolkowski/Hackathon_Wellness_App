const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
    //   target: 'https://tg4n8lh6-8000.euw.devtunnels.ms:8000',
        target: 'http://localhost:8001',
      changeOrigin: true,
      secure: false,
      pathRewrite: {
        '^/api': ''
      }
    })
  );
};
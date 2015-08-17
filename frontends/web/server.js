var webpack = require('webpack');
var WebpackDevServer = require('webpack-dev-server');
var config = require('./webpack.config');

new WebpackDevServer(webpack(config), {
  contentBase: 'dist/',
  hot: true,
  publicPath: config.output.publicPath,
  headers: { 'Access-Control-Allow-Origin': '*' }
}).listen(8000, '0.0.0.0', function (err) {
  if (err) {
    console.log(err);
  }

  console.log('Listening at 0.0.0.0:8000');
});

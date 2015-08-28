var path = require('path');
var webpack = require('webpack');
var _ = require('lodash');

var node_modules_dir = path.join(__dirname, 'node_modules');
var build_dir = '../../niimanga/public';

module.exports = function(options) {
  var config = {
    entry: [
    'bootstrap-webpack!./bootstrap.config.js', 
    './app'
    ],
    output: {
      path: options.environment === 'prod' || options.environment === 'dev-end' ? path.resolve(__dirname, build_dir) : path.resolve(__dirname, './dist'),
      filename: 'back-main.js',
      publicPath: options.environment === 'prod' || options.environment === 'dev-end' ? '/static/' : '',
    },
    module: {
      loaders: [
      { test: /\.js$/, include: path.join(__dirname, "app"), loaders: ['babel-loader?stage=0'] },
      { test: /\.jsx$/, exclude: [node_modules_dir], loaders: ['babel-loader?stage=0'] },
      { test: /bootstrap\/js\//, loader: 'imports?jQuery=jquery' },
      { test: /X-editable\/dist\/bootstrap3-editable\/js\/bootstrap-editable\.js$/, loader: 'imports?jQuery=jquery' },
      { test: /bootstrap-table\/dist\//, loader: 'imports?jQuery=jquery' },
      { test: /\.css$/, loader: 'style!css' },
      { test: /\.png$/, loader: "url-loader?limit=100000" },
      { test: /\.gif$/, loader: "url-loader?limit=100000" },
      { test: /\.jpg$/, loader: "url-loader?limit=100000" },
      { test: /\.woff(2)?(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&minetype=application/font-woff" },      
      { test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,    loader: "url?limit=10000&minetype=application/font-woff" },
      { test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,    loader: "file" },
      { test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,    loader: "url?limit=10000&mimetype=image/svg+xml" }
      ]
    },
    plugins: [
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery",
      "root.jQuery": "jquery"
    }),
    ],
    resolve: {
      root: path.join(__dirname, "app"),
      extensions: ['', '.js'],
      alias: {
        'jquery': path.join(__dirname, 'node_modules/jquery/dist/jquery')
      }
    }
  };

  if (options.environment === 'dev') {
    config.devtool = 'source-map';
    Array.prototype.unshift.call(
      config.entry,
      'webpack-dev-server/client?http://0.0.0.0:8000',
      'webpack/hot/only-dev-server'
      );
    config.plugins = [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin()
    ];
    config.module.loaders[0].loaders.unshift('react-hot');
  }

  if (options.environment === 'dev-end') {
    config.devtool = 'source-map';
  }

  if (options.environment === 'prod') {
    config.plugins = [
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.UglifyJsPlugin(),
    new webpack.DefinePlugin({
      'process.env': {NODE_ENV: '"production"'}
    })
    ]
  }

  config.module.loaders.unshift({
    test: require.resolve("react"),
    loader: "expose?React"
  });

  return config;
};

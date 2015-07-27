var path = require('path');
var webpack = require('webpack');

var node_modules_dir = path.join(__dirname, 'node_modules');
var bower_components_dir = path.join(__dirname, 'bower_components');
var _ = require('lodash');

module.exports = function(options) {
  var config = {
    entry: [
    'bootstrap-webpack!./bootstrap.config.js', 
    './app'
    ],
    output: {
      path: options.environment === 'prod' ? path.resolve(__dirname, '../../niimanga/public') : path.resolve(__dirname, './dist'),
      filename: 'main.js',
      publicPath: options.environment === 'prod' ? '/static/' : '',
    },   
    module: {
      loaders: [
        // **IMPORTANT** This is needed so that each bootstrap js file required by
      // bootstrap-sass-loader has access to the jQuery object
      { test: /bootstrap\/js\//, loader: 'imports?jQuery=jquery' },
      { test: /X-editable\/dist\/bootstrap3-editable\/js\/bootstrap-editable\.js$/, loader: 'imports?jQuery=jquery' },
      { test: /bootstrap-table\/dist\//, loader: 'imports?jQuery=jquery' },
      { test: /\.css$/, loader: 'style!css' },
      { test: /\.jsx$/, exclude: [node_modules_dir, bower_components_dir], loader: 'react-hot!babel-loader?stage=0' },
      { test: /\.js$/, include: path.join(__dirname, "app"), loader: 'babel-loader?stage=0' },
      { test: /\.png$/, loader: "url-loader?limit=100000" },
      { test: /\.gif$/, loader: "url-loader?limit=100000" },
      { test: /\.jpg$/, loader: "url-loader?limit=100000" },

      // Needed for the css-loader when [bootstrap-webpack](https://github.com/bline/bootstrap-webpack)
      // loads bootstrap's css.
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
      extensions: ['', '.web.js', '.js', '.jsx'],
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
    // config.module.loaders[0].loaders.unshift('react-hot');
  }

  if (options.environment === 'prod') {
    config.plugins = [
    new webpack.optimize.UglifyJsPlugin(),
    new webpack.optimize.DedupePlugin()
    ]
  }

  // config.module.loaders.unshift({
  //   test: require.resolve("react"),
  //   loader: "expose?React"
  // });

return config;
};

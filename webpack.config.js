module.exports = {
  entry: './components/cub.jsx',
  output: {
    filename: './js/bundle.js'
  },
  module: {
    loaders: [{
      test    : /\.jsx$/,
      loader  : 'jsx-loader',
      exclude : /node_modules/
    }]
  },
  resolve: {
    extensions: ['', '.js', '.jsx']
  }
}

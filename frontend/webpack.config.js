const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
    entry:
        {
            main: path.resolve(__dirname, './src/js/index.js'),
        },
    mode: 'development',
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, './dist'),
    },
    module: {
      rules: [
          {
              test: /\.(scss)$/,
              use: [
                  MiniCssExtractPlugin.loader,
                  'css-loader',
                  'sass-loader'
              ]
          }
      ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '../css/index.scss',
}),
    ]
};

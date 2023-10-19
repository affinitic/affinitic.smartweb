const path = require("path");

const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

const buildPath = path.resolve(__dirname, "dist");

module.exports = {
  devtool: "source-map",
  entry: {
    index: "./src/index.js",
  },
  // resolve: {
  //   alias: {
  //     "@theme": ".",
  //   },
  // },
  output: {
    filename: "[name].[fullhash:20].js",
    path: buildPath,
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: "babel-loader",

        options: {
          presets: ["env"],
        },
      },
      {
        test: /\.(scss|css|sass)$/,
        use: [ 
          {
              loader: MiniCssExtractPlugin.loader
          },
          {
              // translates CSS into CommonJS
              loader: 'css-loader',
              options: {
                  sourceMap: true
              }
          },
          {
              // Runs compiled CSS through postcss for vendor prefixing
              loader: 'postcss-loader',
              options: {
                  sourceMap: true
              }
          },
          {
              // compiles Sass to CSS
              loader: 'sass-loader',
              options: {
                  sassOptions: {
                    outputStyle: "compressed",
                  },
                  sourceMap: true,
              }
          }
        ],
      },
      {
        // Load all images as base64 encoding if they are smaller than 8192 bytes
        test: /\.(png|jpg|gif|svg)$/,
        use: [
          {
            loader: "url-loader",
            options: {
              name: "[name].[fullhash:20].[ext]",
              limit: 8192,
            },
          },
        ],
      },
      {
        test: /\.(ttf|eot|woff|woff2)$/,
        loader: "file-loader",
        options: {
          name: "fonts/[name].[ext]",
        },
      },
    ],
  },
  optimization: {
    minimizer: [
      // For webpack@5 you can use the `...` syntax to extend existing minimizers (i.e. `terser-webpack-plugin`), uncomment the next line
      `...`,
      new CssMinimizerPlugin(),
    ],
  },
  externals: {
    jquery: "jQuery",
  },
  performance: {
    hints: false
  },
  plugins: [
    new CleanWebpackPlugin({ cleanOnceBeforeBuildPatterns: [buildPath] }),
    new MiniCssExtractPlugin({
        filename: "index.css",
    }),
  ],
};

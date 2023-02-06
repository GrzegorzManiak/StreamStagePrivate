const path = require("path");

module.exports = {
    entry: {
        logout: './logout/index.ts',
        authentication: './authentication/index.ts',
        toast: './toasts/index.ts',
    },
    module: {
        rules: [
            {
              test: /\.ts$/,
              exclude: /node_modules/,
              loader: "babel-loader",
            },
          ],
    },
    resolve: {
        extensions: [ '.ts', '.js' ]
    },
    target: "web",
    output: {
        filename: '[name]_bin.js',
        path: path.resolve(__dirname, '../App/static/js'),
    },
};
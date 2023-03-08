const path = require("path");
const TerserPlugin = require("terser-webpack-plugin");

module.exports = {
    mode: "production",
    optimization: { minimizer: [new TerserPlugin()] },
    entry: {
        // settings: './settings/index.ts',
        // authentication: './authentication/index.ts',
        // toast: './toasts/index.ts',
        // click_handler: './click_handler/index.ts',
        // ping_server: './ping_server/index.ts',
        // streamer_apps: './streamer_apps/index.ts',
        // srr_visualizer: './srr_visualizer/index.ts',
        homepage: './homepage/index.ts',
    },
    module: {
        rules: [
            {
              test: /\.ts$/,
              exclude: /node_modules/,
              loader: "babel-loader",
            },

            {
                test: /\.ts$/,
                exclude: /node_modules/,
                loader: "string-replace-loader",
                options: {
                    // -- replace multiple non-indent spaces with a single space
                    search: /[ ]{2,}/,
                    replace: ' ',
                }
            }
        ],
    },
    resolve: {
        extensions: [ '.ts', '.js' ]
    },
    target: "web",
    output: {
        filename: '[name]_bin.js',
        path: path.resolve(__dirname, '../App/staticfiles/js'),
    }
};
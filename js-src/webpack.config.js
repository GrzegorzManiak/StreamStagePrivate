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
                test: /\.tsx?$/,
                loader: 'ts-loader',
                exclude: /node_modules|\.d\.ts$/
            },
            {
                test: /\.d\.ts$/,
                loader: 'ignore-loader'
            },         
            {
                test: /\.m?js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            }  
        ],
    },
    resolve: {
        extensions: [ '.ts', '.js' ]
    },
    output: {
        filename: '[name]_bin.js',
        path: path.resolve(__dirname, '../App/static/js'),
    },
};
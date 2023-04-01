const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');
const HappyPack = require('happypack');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
const BundleTracker = require('webpack-bundle-tracker');
const happyThreadPool = HappyPack.ThreadPool({ size: 6 });

module.exports = {
    mode: 'production',
    entry: {
        settings: './settings/index.ts',
        api: './api/index.ts',
        common: './common/index.ts',
        login: './login/index.ts',
        register: './register/index.ts',
        streamer_apps: './streamer_apps/index.ts',
        srr_visualizer: './srr_visualizer/index.ts',
        homepage: './homepage/index.ts',
        events: './events/index.ts',
        event_edit: './event_edit/index.ts',
        navbar: './elements/navbar.ts',
        profiles: './profiles/index.ts',
        broadcaster_profiles: './broadcaster_profiles/index.ts',
        admin: './admin/index.ts',
    },
    module: {
        rules: [
            {
                test: /\.ts$/,
                use: [
                    {
                        loader: 'happypack/loader?id=babel',
                    },
                ],
            },
            {
                test: /\.ts$/,
                loader: 'string-replace-loader',
                options: {
                    // -- replace multiple non-indent spaces with a single space
                    search: / {2,}/g,
                    replace: ' ',
                },
            }
        ],
    },
    resolve: {
        extensions: ['.ts', '.js'],
        alias: {
            '@': path.resolve(__dirname, 'src'),
        },
    },
    optimization: {
        minimizer: [new TerserPlugin({
            parallel: true,
            terserOptions: {
            compress: {
                defaults: true,
            },
            mangle: true,
        }})],
        splitChunks: {
            chunks: 'all',
            minSize: 0,
            maxAsyncRequests: Infinity,
            maxInitialRequests: Infinity,
            cacheGroups: {
                vendor: {
                    test: /[\\/]node_modules[\\/]/,
                    name(module) {
                        const packageName = module.context.match(/[\\/]node_modules[\\/](.*?)([\\/]|$)/)[1];
                        return `npm.${packageName.replace('@', '')}`;
                    },
                    chunks: 'all',
                    enforce: true,
                },
            },
        },
        runtimeChunk: true,
        removeAvailableModules: false,
        removeEmptyChunks: false,
    },
    plugins: [
        new HappyPack({
            id: 'babel',
            threadPool: happyThreadPool,
            loaders: ['babel-loader?cacheDirectory=true'],
        }),
        new BundleAnalyzerPlugin(),
        new BundleTracker({filename: '../App/webpack-stats.json'}),
    ],
    target: 'web',
    output: {
        filename: '[name]-[fullhash].js',
        path: path.resolve(__dirname, '../App/staticfiles/webpack_bundles'),
    },
};

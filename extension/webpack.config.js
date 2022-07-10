const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
    entry: {
        popup: './src/ts/popup.tsx',
        background: './src/ts/background.ts',
        contentScript: './src/ts/contentScript.ts',
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].js',
    },
    module: {
        rules: [{
            test: /\.(js|jsx|ts|tsx)$/,
            exclude: /node_modules/,
            use: {
                loader: 'babel-loader',
                options: {
                    presets: ['@babel/preset-env', '@babel/preset-react', '@babel/preset-typescript']
                },
            }
        }],
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js'],
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './src/html/popup.html',
            filename: 'popup.html'
        }),
        new CopyPlugin({
            patterns: [
                { from: "public" }
            ],
        }),
        new CopyPlugin({
            patterns: [
                { from: "src/icons", to: "icons/" }
            ]
        }),
    ],
};

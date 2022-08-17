const path = require('path');
const glob = require('glob');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');

const matchedFiles = glob.sync(`./src/**(extension|components)/*(*.tsx|*.ts)`, {
    nodir: true
});

const entry = {}

matchedFiles.forEach(file => {
    const TS_FOLDER = path.join(__dirname, 'src/extension');
    const TSX_FOLDER = path.join(__dirname, 'src/components');
    const ABS_PATH = path.join(__dirname, file);

    const relativeTSFile = path.relative(TS_FOLDER, ABS_PATH);
    const relativeTSXFile = path.relative(TSX_FOLDER, ABS_PATH);

    var fileKey;
    if (relativeTSXFile.includes('.tsx')) {
        fileKey = path.join(path.dirname(relativeTSXFile), path.basename(relativeTSXFile, '.tsx'));
    } else if (relativeTSFile.includes('.ts')) {
        fileKey = path.join(path.dirname(relativeTSFile), path.basename(relativeTSFile, '.ts'));
    }
    if (fileKey != null) {
        entry[fileKey] = file;
    }
});

module.exports = {
    entry,
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'js/[name].js',
    },
    module: {
        rules: [{
            test: /\.(js|jsx|ts|tsx)$/,
            exclude: /node_modules/,
            use: 'ts-loader',
        }],
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js'],
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './src/static/html/index.html',
            filename: 'index.html'
        }),
        new CopyPlugin({
            patterns: [
                { from: "public" },
                { from: "src/static/icons", to: "icons/" },
                { from: "src/static/css/index.css", to: "index.css" }
            ],
        }),
    ],
};

module.exports = {
  presets: ['module:metro-react-native-babel-preset'],
  plugins: [
    [
      'module-resolver',
      {
        root: ['.'],
        extensions: [
          '.ios.ts',
          '.android.ts',
          '.ts',
          '.ios.tsx',
          '.android.tsx',
          '.tsx',
          '.jsx',
          '.js',
          '.json',
        ],
        alias: {
          '@components': './src/components',
          '@ui': './src/ui',
          '@theme': './src/theme',
          '@screens': './src/screens',
          '@navigation': './src/navigation',
          '@assets': './src/assets',
          '@data': './src/data',
          '@utils': './src/utils',
          '@i18n': './src/i18n',
          '~types': './src/types.ts',
        },
      },
    ],
    'react-native-reanimated/plugin',
  ],
};

module.exports = {
  preset: 'react-native',
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
transformIgnorePatterns: [
  'node_modules/(?!(react-native|@react-native|@react-navigation|expo(nent)?|@expo(nent)?/.*|@unimodules/.*|unimodules|react-native-svg|react-redux|@reduxjs/toolkit|@tanstack|immer)/)',
],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
    '^expo-router$': '<rootDir>/__mocks__/expo-router.js',
    '^expo-secure-store$': '<rootDir>/__mocks__/expo-secure-store.js',
  },
};
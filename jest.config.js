module.exports = {
  moduleDirectories: ['src', 'node_modules'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
    '^~/(.*)$': '<rootDir>/$1',
    '^vue$': 'vue/dist/vue.common.js'
  },
  moduleFileExtensions: ['js', 'vue', 'json'],
  transform: {
    '^.+\\.js$': 'babel-jest',
    '.*\\.(vue)$': 'vue-jest'
  },
  collectCoverage: true,
  collectCoverageFrom: [
    '<rootDir>/src/**/*.{js,vue}',
    '!<rootDir>/node_modules/**',
    '!<rootDir>/coverage/**/*.js',
    '!<rootDir>/src/static/sw.js'
  ]
}

const React = require('react');

module.exports = {
  useRouter: () => ({ replace: jest.fn(), push: jest.fn(), back: jest.fn() }),
  useRootNavigationState: () => ({ key: 'test-key' }),
  useLocalSearchParams: () => ({ id: '1' }),
  Redirect: ({ href }) =>
    React.createElement('View', { testID: 'redirect', accessibilityLabel: `redirect:${href}` }),
  Stack: { Screen: () => null },
};
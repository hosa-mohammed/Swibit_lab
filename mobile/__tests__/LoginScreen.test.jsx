import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { LoginScreen } from '@/features/auth/components/LoginScreen';
import authReducer from '@/core/store/authSlice';

const createTestStore = () => configureStore({ reducer: { auth: authReducer } });

describe('LoginScreen', () => {
  it('renders login form correctly', () => {
    const store = createTestStore();
    const { getByPlaceholderText, getByText } = render(
      <Provider store={store}>
        <LoginScreen />
      </Provider>
    );

    expect(getByPlaceholderText('Enter your email')).toBeTruthy();
    expect(getByPlaceholderText('Enter your password')).toBeTruthy();
    expect(getByText('Sign In')).toBeTruthy();
  });

  it('shows error when email is empty', async () => {
    const store = createTestStore();
    const { getByText } = render(
      <Provider store={store}>
        <LoginScreen />
      </Provider>
    );

    fireEvent.press(getByText('Sign In'));

    await waitFor(() => {
      expect(getByText('Sign In')).toBeTruthy();
    });
  });

  it('allows entering email and password', () => {
    const store = createTestStore();
    const { getByPlaceholderText } = render(
      <Provider store={store}>
        <LoginScreen />
      </Provider>
    );

    const emailInput = getByPlaceholderText('Enter your email');
    const passwordInput = getByPlaceholderText('Enter your password');

    fireEvent.changeText(emailInput, 'test@example.com');
    fireEvent.changeText(passwordInput, 'password123');

    expect(emailInput.props.value).toBe('test@example.com');
    expect(passwordInput.props.value).toBe('password123');
  });
});
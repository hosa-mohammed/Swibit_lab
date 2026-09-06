import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import { tokenStore } from '../auth/tokenStore';
import { setToken } from './authSlice';

export const store = configureStore({
  reducer: { auth: authReducer },
});

export async function restoreSession() {
  const token = await tokenStore.get();
  if (token) store.dispatch(setToken(token));
}
import { tokenStore } from '../auth/tokenStore';
import { store } from '../store';
import { logout } from '../store/authSlice';
import { API_BASE_URL } from './config';

export async function apiFetch(path, init = {}) {
  const token = await tokenStore.get();
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init.headers,
    },
  });

  if (res.status === 401) {
    await tokenStore.clear();
    store.dispatch(logout());
  }

  return res;
}
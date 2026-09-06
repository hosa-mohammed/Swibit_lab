import { store } from '../store';
import { logout } from '../store/authSlice';
import { tokenStore } from './tokenStore';

export function signOut() {
  void tokenStore.clear();
  store.dispatch(logout());
}
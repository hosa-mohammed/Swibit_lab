import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

const KEY = 'auth.token';

const web = {
  get: async () => localStorage.getItem(KEY),
  set: async (token) => { localStorage.setItem(KEY, token); },
  clear: async () => { localStorage.removeItem(KEY); },
};

const native = {
  get: () => SecureStore.getItemAsync(KEY),
  set: (token) => SecureStore.setItemAsync(KEY, token),
  clear: () => SecureStore.deleteItemAsync(KEY),
};

export const tokenStore = Platform.OS === 'web' ? web : native;
import '../global.css';
import { useEffect, useState } from 'react';
import { Stack } from 'expo-router';
import { Provider } from 'react-redux';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { restoreSession, store } from '@/core/store';
import LoadingSpinner from '@/shared/components/LoadingSpinner';

const queryClient = new QueryClient();

export default function RootLayout() {
  const [restored, setRestored] = useState(false);

  useEffect(() => {
    restoreSession().finally(() => setRestored(true));
  }, []);

  if (!restored) return <LoadingSpinner />;

  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <Stack>
          <Stack.Screen name="index" options={{ headerShown: false }} />
          <Stack.Screen name="auth/login" options={{ headerShown: false }} />
          <Stack.Screen name="(app)" options={{ headerShown: false }} />
        </Stack>
      </QueryClientProvider>
    </Provider>
  );
}
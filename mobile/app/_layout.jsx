import { Stack } from 'expo-router';
import { Provider } from 'react-redux';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { store } from '../store/store';

const queryClient = new QueryClient();

export default function RootLayout() {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <Stack>
          <Stack.Screen name="index" options={{ title: 'Swibit' }} />
          <Stack.Screen name="login" options={{ title: 'Login' }} />
          <Stack.Screen name="tasks" options={{ title: 'My Tasks' }} />
        </Stack>
      </QueryClientProvider>
    </Provider>
  );
}
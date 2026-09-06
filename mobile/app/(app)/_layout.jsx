import { Redirect, Stack } from 'expo-router';
import { useSelector } from 'react-redux';

export default function AppLayout() {
  const { token } = useSelector((state) => state.auth);

  if (!token) return <Redirect href="/auth/login" />;

  return (
    <Stack>
      <Stack.Screen name="tasks" options={{ headerShown: false }} />
      <Stack.Screen name="task/[id]" options={{ title: 'Edit Task' }} />
      <Stack.Screen name="create-task" options={{ title: 'New Task', presentation: 'modal', headerShown: false }} />
      <Stack.Screen name="assistant" options={{ headerShown: false }} />
    </Stack>
  );
}
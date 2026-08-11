import { useEffect } from 'react';
import { View, ActivityIndicator } from 'react-native';
import { useSelector } from 'react-redux';
import { useRouter, useRootNavigationState } from 'expo-router';

export default function Index() {
  const router = useRouter();
  const navigationState = useRootNavigationState();
  const { token } = useSelector((state) => state.auth);

  useEffect(() => {
    if (!navigationState?.key) return;
    
    if (token) {
      router.replace('/tasks');
    } else {
      router.replace('/login');
    }
  }, [token, navigationState?.key]);

  return (
    <View className="flex-1 justify-center items-center">
      <ActivityIndicator size="large" />
    </View>
  );
}
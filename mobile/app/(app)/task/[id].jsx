import { Text, View } from 'react-native';
import { useLocalSearchParams } from 'expo-router';

export default function TaskDetailRoute() {
  const { id } = useLocalSearchParams();
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#F3F4F6' }}>
      <Text style={{ color: '#6B7280' }}>Task #{id} — Edit screen coming next</Text>
    </View>
  );
}
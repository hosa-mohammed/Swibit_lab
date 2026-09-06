import { Alert, FlatList, Platform, RefreshControl, Text, TouchableOpacity, View } from 'react-native';
import { useRouter } from 'expo-router';
import { useDeleteTask, useTasks } from '../api';
import TaskCard from './TaskCard';
import LoadingSpinner from '@/shared/components/LoadingSpinner';
import { signOut } from '@/core/auth/session';

export function TasksScreen() {
  const router = useRouter();
  const { data: items, isLoading, isFetching, error, refetch } = useTasks();
  const deleteTask = useDeleteTask();

  const handleDeleteTask = async (taskId) => {
    const confirmDelete = () => {
      if (Platform.OS === 'web') {
        return window.confirm('Are you sure you want to delete this task?');
      }
      return new Promise((resolve) => {
        Alert.alert(
          'Delete Task',
          'Are you sure you want to delete this task?',
          [
            { text: 'Cancel', onPress: () => resolve(false), style: 'cancel' },
            { text: 'Delete', onPress: () => resolve(true), style: 'destructive' },
          ]
        );
      });
    };

    const confirmed = await confirmDelete();
    if (!confirmed) return;

    deleteTask.mutate(taskId);
  };

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#F3F4F6' }}>
        <Text style={{ color: '#EF4444' }}>{error.message}</Text>
        <TouchableOpacity onPress={() => refetch()} style={{ marginTop: 16 }}>
          <Text style={{ color: '#2563EB', fontWeight: '600' }}>Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={{ flex: 1, backgroundColor: '#F3F4F6' }}>
      <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 16, backgroundColor: 'white', borderBottomWidth: 1, borderBottomColor: '#E5E7EB' }}>
        <Text style={{ fontSize: 20, fontWeight: 'bold', color: '#111827' }}>My Tasks</Text>
        <View style={{ flexDirection: 'row', alignItems: 'center' }}>
          <TouchableOpacity
            onPress={() => router.push('/assistant')}
            style={{ backgroundColor: '#2563EB', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 9999, marginRight: 12 }}
          >
            <Text style={{ color: 'white', fontWeight: '600', fontSize: 12 }}>AI Assistant</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={() => router.push('/create-task')} style={{ marginRight: 16 }}>
            <Text style={{ color: '#2563EB', fontWeight: '600', fontSize: 24 }}>+</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={signOut}>
            <Text style={{ color: '#EF4444', fontWeight: '600' }}>Logout</Text>
          </TouchableOpacity>
        </View>
      </View>

      <FlatList
        data={items ?? []}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <TaskCard
            task={item}
            onPress={() => router.push(`/task/${item.id}`)}
            onDelete={() => handleDeleteTask(item.id)}
          />
        )}
        refreshControl={
          <RefreshControl refreshing={isFetching} onRefresh={() => refetch()} />
        }
        contentContainerStyle={{ padding: 16 }}
        ListEmptyComponent={
          <View style={{ alignItems: 'center', marginTop: 100 }}>
            <Text style={{ fontSize: 18, color: '#6B7280', marginBottom: 8 }}>No tasks yet</Text>
            <Text style={{ color: '#9CA3AF' }}>Pull down to refresh or add a new task</Text>
          </View>
        }
      />
    </View>
  );
}
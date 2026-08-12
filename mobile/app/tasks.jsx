import { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, ActivityIndicator, RefreshControl } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { useRouter } from 'expo-router';
import { fetchTasks } from '../store/slices/taskSlice';
import { logout } from '../store/slices/authSlice';
import TaskCard from '../components/TaskCard';

export default function TasksScreen() {
  const dispatch = useDispatch();
  const router = useRouter();
  const [isReady, setIsReady] = useState(false);
  
  const tasksState = useSelector((state) => state.tasks) || { items: [], isLoading: false, error: null };
  const { items, isLoading, error } = tasksState;
  
  const { token } = useSelector((state) => state.auth);

  useEffect(() => {
   
    const timer = setTimeout(() => {
      setIsReady(true);
    }, 100);

    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (!isReady) return;
    
    if (!token) {
      router.replace('/login');
      return;
    }
    dispatch(fetchTasks());
  }, [token, isReady]);

  const handleLogout = () => {
    dispatch(logout());
    router.replace('/login');
  };

  if (!isReady || isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#F3F4F6' }}>
        <ActivityIndicator size="large" color="#2563EB" />
      </View>
    );
  }

  if (error) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#F3F4F6' }}>
        <Text style={{ color: '#EF4444' }}>{error}</Text>
        <TouchableOpacity onPress={() => dispatch(fetchTasks())} style={{ marginTop: 16 }}>
          <Text style={{ color: '#2563EB', fontWeight: '600' }}>Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={{ flex: 1, backgroundColor: '#F3F4F6' }}>
      <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 16, backgroundColor: 'white', borderBottomWidth: 1, borderBottomColor: '#E5E7EB' }}>
        <Text style={{ fontSize: 20, fontWeight: 'bold', color: '#111827' }}>My Tasks</Text>
        <TouchableOpacity onPress={handleLogout}>
          <Text style={{ color: '#EF4444', fontWeight: '600' }}>Logout</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={items}
        keyExtractor={(item) => item.id?.toString() || Math.random().toString()}
        renderItem={({ item }) => <TaskCard task={item} />}
        refreshControl={
          <RefreshControl refreshing={isLoading} onRefresh={() => dispatch(fetchTasks())} />
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
import { useEffect } from 'react';
import { View, Text, FlatList, TouchableOpacity, ActivityIndicator, RefreshControl } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { useRouter } from 'expo-router';
import { fetchTasks } from '../store/slices/taskSlice';
import { logout } from '../store/slices/authSlice';
import TaskCard from '../components/TaskCard';

export default function TasksScreen() {
  const dispatch = useDispatch();
  const router = useRouter();
  const { items, isLoading, error } = useSelector((state) => state.tasks);
  const { token } = useSelector((state) => state.auth);

  useEffect(() => {
    if (!token) {
      router.replace('/login');
      return;
    }
    dispatch(fetchTasks());
  }, [token]);

  const handleLogout = () => {
    dispatch(logout());
    router.replace('/login');
  };

  if (error) {
    return (
      <View className="flex-1 justify-center items-center">
        <Text className="text-red-500">{error}</Text>
        <TouchableOpacity onPress={() => dispatch(fetchTasks())}>
          <Text className="text-blue-600 mt-4 font-semibold">Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View className="flex-1 bg-gray-100">
      <View className="flex-row justify-between items-center p-4 bg-white border-b border-gray-200">
        <Text className="text-xl font-bold text-gray-900">My Tasks</Text>
        <TouchableOpacity onPress={handleLogout}>
          <Text className="text-red-500 font-semibold">Logout</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={items}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => <TaskCard task={item} />}
        refreshControl={
          <RefreshControl refreshing={isLoading} onRefresh={() => dispatch(fetchTasks())} />
        }
        contentContainerClassName="p-4"
      />
    </View>
  );
}
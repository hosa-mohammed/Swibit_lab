import { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { useDispatch, useSelector } from 'react-redux';
import { createTask } from '../store/slices/taskSlice';

export default function CreateTaskScreen() {
  const router = useRouter();
  const dispatch = useDispatch();
  const { isLoading, error } = useSelector((state) => state.tasks);
  
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('medium');
  const [localError, setLocalError] = useState('');

  const priorities = [
    { label: 'Low', value: 'low', color: '#10B981' },
    { label: 'Medium', value: 'medium', color: '#F59E0B' },
    { label: 'High', value: 'high', color: '#EF4444' },
  ];

  const handleCreate = async () => {
    if (!title.trim()) {
      setLocalError('Title is required');
      return;
    }

    setLocalError('');
    
    const result = await dispatch(createTask({ title, description, priority }));
    
    if (result.meta.requestStatus === 'fulfilled') {
      router.back();
    }
  };

  return (
    <View style={{ flex: 1, backgroundColor: '#F3F4F6', padding: 16 }}>
      <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#111827', marginBottom: 24 }}>
        New Task
      </Text>

      {(error || localError) && (
        <View style={{ backgroundColor: '#FEF2F2', borderRadius: 8, padding: 12, marginBottom: 16 }}>
          <Text style={{ color: '#DC2626' }}>{error || localError}</Text>
        </View>
      )}

      <View style={{ marginBottom: 16 }}>
        <Text style={{ color: '#374151', fontWeight: '500', marginBottom: 8 }}>Title *</Text>
        <TextInput
          style={{ borderWidth: 1, borderColor: '#D1D5DB', borderRadius: 8, paddingHorizontal: 16, paddingVertical: 12, backgroundColor: 'white', color: '#111827' }}
          placeholder="Enter task title"
          placeholderTextColor="#9CA3AF"
          value={title}
          onChangeText={setTitle}
        />
      </View>

      <View style={{ marginBottom: 16 }}>
        <Text style={{ color: '#374151', fontWeight: '500', marginBottom: 8 }}>Description</Text>
        <TextInput
          style={{ borderWidth: 1, borderColor: '#D1D5DB', borderRadius: 8, paddingHorizontal: 16, paddingVertical: 12, backgroundColor: 'white', color: '#111827', height: 100, textAlignVertical: 'top' }}
          placeholder="Enter description (optional)"
          placeholderTextColor="#9CA3AF"
          value={description}
          onChangeText={setDescription}
          multiline
        />
      </View>

      <View style={{ marginBottom: 24 }}>
        <Text style={{ color: '#374151', fontWeight: '500', marginBottom: 8 }}>Priority</Text>
        <View style={{ flexDirection: 'row' }}>
          {priorities.map((p) => (
            <TouchableOpacity
              key={p.value}
              onPress={() => setPriority(p.value)}
              style={{
                flex: 1,
                paddingVertical: 12,
                paddingHorizontal: 8,
                borderRadius: 8,
                marginRight: 8,
                backgroundColor: priority === p.value ? p.color : '#E5E7EB',
              }}
            >
              <Text style={{ color: priority === p.value ? 'white' : '#374151', textAlign: 'center', fontWeight: '600' }}>
                {p.label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <TouchableOpacity
        onPress={handleCreate}
        disabled={isLoading}
        style={{
          backgroundColor: isLoading ? '#93C5FD' : '#2563EB',
          borderRadius: 8,
          paddingVertical: 14,
          alignItems: 'center',
        }}
      >
        {isLoading ? (
          <ActivityIndicator color="white" />
        ) : (
          <Text style={{ color: 'white', fontWeight: '600', fontSize: 16 }}>Create Task</Text>
        )}
      </TouchableOpacity>

      <TouchableOpacity
        onPress={() => router.back()}
        style={{ marginTop: 12, alignItems: 'center' }}
      >
        <Text style={{ color: '#6B7280' }}>Cancel</Text>
      </TouchableOpacity>
    </View>
  );
}
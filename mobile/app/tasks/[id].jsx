import { useEffect, useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ActivityIndicator, Switch } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_BASE_URL } from '../../lib/api';

export default function EditTaskScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams();
  const [task, setTask] = useState(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('medium');
  const [isComplete, setIsComplete] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');

  const priorities = [
    { label: 'Low', value: 'low', color: '#10B981' },
    { label: 'Medium', value: 'medium', color: '#F59E0B' },
    { label: 'High', value: 'high', color: '#EF4444' },
  ];

  useEffect(() => {
    fetchTask();
  }, [id]);

  const fetchTask = async () => {
    try {
      const token = await AsyncStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/tasks/`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      
      if (!response.ok) throw new Error('Failed to fetch');
      
      const tasks = await response.json();
      const found = tasks.find(t => t.id === parseInt(id));
      
      if (!found) throw new Error('Task not found');
      
      setTask(found);
      setTitle(found.title);
      setDescription(found.description || '');
      setPriority(found.priority);
      setIsComplete(found.is_complete);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdate = async () => {
    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    setIsSaving(true);
    setError('');

    try {
      const token = await AsyncStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          title,
          description,
          priority,
          is_complete: isComplete,
        }),
      });

      if (!response.ok) throw new Error('Failed to update');
      router.back();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#F3F4F6' }}>
        <ActivityIndicator size="large" color="#2563EB" />
      </View>
    );
  }

  return (
    <View style={{ flex: 1, backgroundColor: '#F3F4F6', padding: 16 }}>
      <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#111827', marginBottom: 24 }}>
        Edit Task
      </Text>

      {error && (
        <View style={{ backgroundColor: '#FEF2F2', borderRadius: 8, padding: 12, marginBottom: 16 }}>
          <Text style={{ color: '#DC2626' }}>{error}</Text>
        </View>
      )}

      <View style={{ marginBottom: 16 }}>
        <Text style={{ color: '#374151', fontWeight: '500', marginBottom: 8 }}>Title *</Text>
        <TextInput
          style={{ borderWidth: 1, borderColor: '#D1D5DB', borderRadius: 8, paddingHorizontal: 16, paddingVertical: 12, backgroundColor: 'white', color: '#111827' }}
          value={title}
          onChangeText={setTitle}
        />
      </View>

      <View style={{ marginBottom: 16 }}>
        <Text style={{ color: '#374151', fontWeight: '500', marginBottom: 8 }}>Description</Text>
        <TextInput
          style={{ borderWidth: 1, borderColor: '#D1D5DB', borderRadius: 8, paddingHorizontal: 16, paddingVertical: 12, backgroundColor: 'white', color: '#111827', height: 100, textAlignVertical: 'top' }}
          value={description}
          onChangeText={setDescription}
          multiline
        />
      </View>

      <View style={{ marginBottom: 16 }}>
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

      <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 24 }}>
        <Text style={{ color: '#374151', fontWeight: '500', flex: 1 }}>Completed</Text>
        <Switch
          value={isComplete}
          onValueChange={setIsComplete}
          trackColor={{ false: '#D1D5DB', true: '#10B981' }}
        />
      </View>

      <TouchableOpacity
        onPress={handleUpdate}
        disabled={isSaving}
        style={{
          backgroundColor: isSaving ? '#93C5FD' : '#2563EB',
          borderRadius: 8,
          paddingVertical: 14,
          alignItems: 'center',
        }}
      >
        {isSaving ? (
          <ActivityIndicator color="white" />
        ) : (
          <Text style={{ color: 'white', fontWeight: '600', fontSize: 16 }}>Save Changes</Text>
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
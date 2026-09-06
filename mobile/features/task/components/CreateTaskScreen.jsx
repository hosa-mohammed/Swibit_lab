import { useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { Field } from '@/shared/components/Field';
import { SubmitButton } from '@/shared/components/SubmitButton';
import { useCreateTask } from '../api';
import { PRIORITIES } from '../priority';

export function CreateTaskScreen() {
  const router = useRouter();
  const createTask = useCreateTask();

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('medium');
  const [localError, setLocalError] = useState('');

  const handleCreate = () => {
    if (!title.trim()) {
      setLocalError('Title is required');
      return;
    }
    setLocalError('');
    createTask.mutate(
      { title, description, priority },
      { onSuccess: () => router.back() },
    );
  };

  const errorMessage = localError || createTask.error?.message;

  return (
    <View style={{ flex: 1, backgroundColor: '#F3F4F6', padding: 16 }}>
      <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#111827', marginBottom: 24 }}>
        New Task
      </Text>

      {errorMessage ? (
        <View style={{ backgroundColor: '#FEF2F2', borderRadius: 8, padding: 12, marginBottom: 16 }}>
          <Text style={{ color: '#DC2626' }}>{errorMessage}</Text>
        </View>
      ) : null}

      <Field label="Title *" placeholder="Enter task title" value={title} onChangeText={setTitle} />
      <Field
        label="Description"
        placeholder="Enter description (optional)"
        value={description}
        onChangeText={setDescription}
        multiline
        style={{ height: 100, textAlignVertical: 'top' }}
      />

      <View style={{ marginBottom: 24 }}>
        <Text style={{ color: '#374151', fontWeight: '500', marginBottom: 8 }}>Priority</Text>
        <View style={{ flexDirection: 'row' }}>
          {PRIORITIES.map((p) => (
            <TouchableOpacity
              key={p.value}
              onPress={() => setPriority(p.value)}
              style={{
                flex: 1,
                paddingVertical: 12,
                paddingHorizontal: 8,
                borderRadius: 8,
                marginRight: 8,
                backgroundColor: priority === p.value ? p.solid : '#E5E7EB',
              }}
            >
              <Text style={{ color: priority === p.value ? 'white' : '#374151', textAlign: 'center', fontWeight: '600' }}>
                {p.label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <SubmitButton label="Create Task" loading={createTask.isPending} onPress={handleCreate} />

      <TouchableOpacity onPress={() => router.back()} style={{ marginTop: 12, alignItems: 'center' }}>
        <Text style={{ color: '#6B7280' }}>Cancel</Text>
      </TouchableOpacity>
    </View>
  );
}
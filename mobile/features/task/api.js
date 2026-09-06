import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiFetch } from '@/core/api/client';

export async function fetchTasks() {
  const res = await apiFetch('/tasks/');
  if (!res.ok) throw new Error('Failed to fetch');
  return res.json();
}

export async function createTask(input) {
  const res = await apiFetch('/tasks/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || 'Failed to create task');
  }
  return res.json();
}

export async function deleteTask(taskId) {
  const res = await apiFetch(`/tasks/${taskId}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete');
}

export function useTasks() {
  return useQuery({ queryKey: ['tasks'], queryFn: fetchTasks });
}

export function useCreateTask() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: createTask,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['tasks'] }),
  });
}

export function useDeleteTask() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: deleteTask,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['tasks'] }),
  });
}
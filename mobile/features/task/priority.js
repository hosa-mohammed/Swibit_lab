export const PRIORITIES = [
  { value: 'low',    label: 'Low',    solid: '#10B981', badge: { bg: '#D1FAE5', text: '#059669' } },
  { value: 'medium', label: 'Medium', solid: '#F59E0B', badge: { bg: '#FEF3C7', text: '#D97706' } },
  { value: 'high',   label: 'High',   solid: '#EF4444', badge: { bg: '#FEE2E2', text: '#DC2626' } },
];

export function priorityOf(priority) {
  return PRIORITIES.find((p) => p.value === priority) ?? PRIORITIES[1];
}
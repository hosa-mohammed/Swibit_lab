import { View, Text, TouchableOpacity } from 'react-native';

export default function TaskCard({ task, onPress, onDelete }) {
  const priorityColors = {
    high: { bg: '#FEE2E2', text: '#DC2626' },
    medium: { bg: '#FEF3C7', text: '#D97706' },
    low: { bg: '#D1FAE5', text: '#059669' },
  };

  const colors = priorityColors[task.priority] || priorityColors.medium;

  return (
    <View style={{ backgroundColor: 'white', borderRadius: 12, padding: 16, marginBottom: 12, shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.1, shadowRadius: 2, elevation: 2 }}>
      <TouchableOpacity onPress={onPress}>
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Text style={{ fontSize: 16, fontWeight: '600', color: task.is_complete ? '#9CA3AF' : '#111827', flex: 1, textDecorationLine: task.is_complete ? 'line-through' : 'none' }}>
            {task.title}
          </Text>
          <View style={{ backgroundColor: colors.bg, paddingHorizontal: 8, paddingVertical: 4, borderRadius: 12, marginLeft: 8 }}>
            <Text style={{ color: colors.text, fontSize: 12, fontWeight: '500' }}>
              {task.priority}
            </Text>
          </View>
        </View>
        
        {task.description && (
          <Text style={{ color: '#6B7280', marginTop: 8, fontSize: 14 }}>
            {task.description}
          </Text>
        )}
      </TouchableOpacity>
      
      {/* زر Delete خارج TouchableOpacity */}
      <View style={{ flexDirection: 'row', justifyContent: 'flex-end', marginTop: 12 }}>
        <TouchableOpacity onPress={onDelete} style={{ padding: 8 }}>
          <Text style={{ color: '#EF4444', fontSize: 14 }}>Delete</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
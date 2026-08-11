import { View, Text } from 'react-native';

export default function TaskCard({ task }) {
  const priorityColors = {
    high: 'bg-red-100 text-red-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800',
  };

  const getPriorityStyle = () => {
    return priorityColors[task.priority] || priorityColors.medium;
  };

  return (
    <View className="bg-white rounded-xl p-4 mb-3 shadow-sm">
      <View className="flex-row justify-between items-start">
        <Text className={`text-lg font-semibold flex-1 mr-2 ${task.is_complete ? 'line-through text-gray-400' : 'text-gray-900'}`}>
          {task.title}
        </Text>
        <View className={`px-2 py-1 rounded-full ${getPriorityStyle().split(' ')[0]}`}>
          <Text className={`text-xs font-medium ${getPriorityStyle().split(' ')[1]}`}>
            {task.priority}
          </Text>
        </View>
      </View>
      {task.description && (
        <Text className="text-gray-600 mt-2 text-sm">{task.description}</Text>
      )}
    </View>
  );
}
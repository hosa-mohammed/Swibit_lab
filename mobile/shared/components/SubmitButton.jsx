import { ActivityIndicator, Text, TouchableOpacity } from 'react-native';

export function SubmitButton({ label, loading, disabled, style, ...pressableProps }) {
  return (
    <TouchableOpacity
      disabled={disabled || loading}
      style={[
        {
          borderRadius: 8,
          paddingVertical: 14,
          alignItems: 'center',
          backgroundColor: loading || disabled ? '#93C5FD' : '#2563EB',
        },
        style,
      ]}
      {...pressableProps}
    >
      {loading ? (
        <ActivityIndicator color="white" />
      ) : (
        <Text style={{ color: 'white', fontWeight: '600', fontSize: 16 }}>{label}</Text>
      )}
    </TouchableOpacity>
  );
}
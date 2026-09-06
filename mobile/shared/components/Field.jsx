import { Text, TextInput, View } from 'react-native';

export function Field({ label, style, ...inputProps }) {
  return (
    <View style={{ marginBottom: 16 }}>
      <Text style={{ color: '#374151', fontWeight: '500', marginBottom: 8 }}>{label}</Text>
      <TextInput
        style={[
          {
            borderWidth: 1,
            borderColor: '#D1D5DB',
            borderRadius: 8,
            paddingHorizontal: 16,
            paddingVertical: 12,
            backgroundColor: 'white',
            color: '#111827',
          },
          style,
        ]}
        placeholderTextColor="#9CA3AF"
        {...inputProps}
      />
    </View>
  );
}
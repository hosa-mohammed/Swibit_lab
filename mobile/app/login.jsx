import { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { useRouter } from 'expo-router';
import { loginUser } from '../store/slices/authSlice';

export default function LoginScreen() {
  const dispatch = useDispatch();
  const router = useRouter();
  const { isLoading, error } = useSelector((state) => state.auth);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    const result = await dispatch(loginUser({ email, password }));
    if (result.meta.requestStatus === 'fulfilled') {
      router.replace('/tasks');
    }
  };

  return (
    <View style={{ flex: 1, backgroundColor: '#F3F4F6', justifyContent: 'center', paddingHorizontal: 24 }}>
      <View style={{ backgroundColor: 'white', borderRadius: 16, padding: 32, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4, elevation: 3 }}>
        <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#111827', textAlign: 'center', marginBottom: 8 }}>
          Swibit Login
        </Text>
        <Text style={{ color: '#6B7280', textAlign: 'center', marginBottom: 24 }}>
          Sign in to your account
        </Text>

        {error && (
          <View style={{ backgroundColor: '#FEF2F2', borderColor: '#FECACA', borderWidth: 1, borderRadius: 8, padding: 12, marginBottom: 16 }}>
            <Text style={{ color: '#DC2626', fontSize: 14, textAlign: 'center' }}>{error}</Text>
          </View>
        )}

        <View style={{ marginBottom: 16 }}>
          <Text style={{ color: '#374151', fontWeight: '500', marginBottom: 8 }}>Email</Text>
          <TextInput
            style={{ borderWidth: 1, borderColor: '#D1D5DB', borderRadius: 8, paddingHorizontal: 16, paddingVertical: 12, color: '#111827', backgroundColor: '#F9FAFB' }}
            placeholder="Enter your email"
            placeholderTextColor="#9CA3AF"
            value={email}
            onChangeText={setEmail}
            autoCapitalize="none"
            keyboardType="email-address"
          />
        </View>

        <View style={{ marginBottom: 24 }}>
          <Text style={{ color: '#374151', fontWeight: '500', marginBottom: 8 }}>Password</Text>
          <TextInput
            style={{ borderWidth: 1, borderColor: '#D1D5DB', borderRadius: 8, paddingHorizontal: 16, paddingVertical: 12, color: '#111827', backgroundColor: '#F9FAFB' }}
            placeholder="Enter your password"
            placeholderTextColor="#9CA3AF"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />
        </View>

        <TouchableOpacity
          onPress={handleLogin}
          disabled={isLoading}
          style={{ borderRadius: 8, paddingVertical: 12, paddingHorizontal: 16, backgroundColor: isLoading ? '#60A5FA' : '#2563EB' }}
        >
          {isLoading ? (
            <ActivityIndicator color="white" />
          ) : (
            <Text style={{ color: 'white', textAlign: 'center', fontWeight: '600', fontSize: 18 }}>
              Sign In
            </Text>
          )}
        </TouchableOpacity>
      </View>
    </View>
  );
}
import { useState } from 'react';
import { View, Text } from 'react-native';
import { Redirect } from 'expo-router';
import { useDispatch, useSelector } from 'react-redux';
import { loginUser } from '@/core/store/authSlice';
import { Field } from '@/shared/components/Field';
import { SubmitButton } from '@/shared/components/SubmitButton';

export function LoginScreen() {
  const dispatch = useDispatch();
  const { token, isLoading, error } = useSelector((state) => state.auth);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  if (token) return <Redirect href="/tasks" />;

  const handleLogin = () => {
    dispatch(loginUser({ email, password }));
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

        {error ? (
          <View style={{ backgroundColor: '#FEF2F2', borderColor: '#FECACA', borderWidth: 1, borderRadius: 8, padding: 12, marginBottom: 16 }}>
            <Text style={{ color: '#DC2626', fontSize: 14, textAlign: 'center' }}>{error}</Text>
          </View>
        ) : null}

        <Field
          label="Email"
          placeholder="Enter your email"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
        />
        <Field
          label="Password"
          placeholder="Enter your password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <SubmitButton label="Sign In" loading={isLoading} onPress={handleLogin} />
      </View>
    </View>
  );
}
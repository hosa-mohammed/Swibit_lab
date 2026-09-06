import { Redirect } from 'expo-router';
import { useSelector } from 'react-redux';

export default function Index() {
  const { token } = useSelector((state) => state.auth);
  return <Redirect href={token ? '/tasks' : '/auth/login'} />;
}
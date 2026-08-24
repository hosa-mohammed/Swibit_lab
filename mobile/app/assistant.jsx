import { useState, useRef } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  ScrollView, 
  KeyboardAvoidingView, 
  Platform 
} from 'react-native';
import { useSelector } from 'react-redux';
import { useRouter } from 'expo-router';

export default function AssistantScreen() {
  const router = useRouter();
  const { token } = useSelector((state) => state.auth);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    {
      id: '1',
      text: 'Hello! I am your AI assistant. Ask me about company policies or your tasks.',
      sender: 'bot',
    },
  ]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = {
      id: Date.now().toString(),
      text: input.trim(),
      sender: 'user',
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://192.168.1.100:8000/assistant/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ text: userMsg.text }),
      });

      const data = await response.json();

      const botMsg = {
        id: (Date.now() + 1).toString(),
        text: data.answer || 'Sorry, I did not understand.',
        sender: 'bot',
        citations: data.citations,
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      const errorMsg = {
        id: (Date.now() + 1).toString(),
        text: 'Error: Cannot connect to server.',
        sender: 'bot',
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={{ flex: 1, backgroundColor: '#F3F4F6' }}
    >
      <View style={{ backgroundColor: '#2563EB', padding: 16, paddingTop: 48, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
        <Text style={{ color: 'white', fontSize: 18, fontWeight: 'bold' }}>AI Assistant</Text>
        <TouchableOpacity onPress={() => router.back()}>
          <Text style={{ color: 'white', fontSize: 14 }}>Close</Text>
        </TouchableOpacity>
      </View>

      <ScrollView
        ref={scrollRef}
        style={{ flex: 1, padding: 16 }}
        onContentSizeChange={() => scrollRef.current?.scrollToEnd({ animated: true })}
      >
        {messages.map((msg) => (
          <View
            key={msg.id}
            style={{
              marginBottom: 12,
              maxWidth: '80%',
              alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
            }}
          >
            <View
              style={{
                padding: 12,
                borderRadius: 16,
                backgroundColor: msg.sender === 'user' ? '#2563EB' : 'white',
                borderWidth: msg.sender === 'user' ? 0 : 1,
                borderColor: '#E5E7EB',
              }}
            >
              <Text style={{ color: msg.sender === 'user' ? 'white' : '#1F2937' }}>
                {msg.text}
              </Text>
            </View>
            
            {msg.citations && msg.citations.length > 0 && (
              <Text style={{ fontSize: 12, color: '#6B7280', marginTop: 4 }}>
                Source: {msg.citations.join(', ')}
              </Text>
            )}
          </View>
        ))}
        
        {loading && (
          <View style={{ alignSelf: 'flex-start', backgroundColor: '#E5E7EB', padding: 12, borderRadius: 16, marginBottom: 12 }}>
            <Text style={{ color: '#6B7280' }}>Thinking...</Text>
          </View>
        )}
      </ScrollView>

      <View style={{ backgroundColor: 'white', padding: 16, borderTopWidth: 1, borderTopColor: '#E5E7EB', flexDirection: 'row', alignItems: 'center' }}>
        <TextInput
          style={{ flex: 1, backgroundColor: '#F3F4F6', padding: 12, borderRadius: 9999, marginRight: 8 }}
          placeholder="Ask me anything..."
          value={input}
          onChangeText={setInput}
          onSubmitEditing={sendMessage}
        />
        <TouchableOpacity
          onPress={sendMessage}
          style={{ backgroundColor: '#2563EB', padding: 12, borderRadius: 9999 }}
          disabled={loading}
        >
          <Text style={{ color: 'white', fontWeight: 'bold' }}>Send</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}
import React, { useState, useEffect, useRef } from 'react';

export function ChatWindow({ conversationId, userId }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const ws = useRef(null);

    useEffect(() => {
        // Mock websocket connection
        ws.current = new WebSocket(`ws://localhost:8000/ws/chat/${conversationId}/`);
        
        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessages(prev => [...prev, data]);
        };

        return () => ws.current.close();
    }, [conversationId]);

    const sendMessage = () => {
        if (!input.trim()) return;
        ws.current.send(JSON.stringify({
            message: input,
            user_id: userId,
            type: 'text'
        }));
        setInput('');
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '400px', background: '#111A16', borderRadius: '12px', overflow: 'hidden', fontFamily: 'Inter' }}>
            <div style={{ background: '#0B1210', padding: '16px', borderBottom: '1px solid #222', color: '#FFF' }}>
                Chat (Conversation #{conversationId})
            </div>
            <div style={{ flex: 1, padding: '16px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {messages.map((m, i) => (
                    <div key={i} style={{ 
                        alignSelf: m.user_id === userId ? 'flex-end' : 'flex-start',
                        background: m.user_id === userId ? '#22C55E' : '#333',
                        color: '#FFF', padding: '10px 14px', borderRadius: '16px', maxWidth: '70%'
                    }}>
                        {m.message}
                    </div>
                ))}
            </div>
            <div style={{ padding: '16px', borderTop: '1px solid #222', display: 'flex', gap: '8px', background: '#0B1210' }}>
                <input 
                    value={input} onChange={e => setInput(e.target.value)} 
                    onKeyPress={e => e.key === 'Enter' && sendMessage()}
                    style={{ flex: 1, padding: '10px', borderRadius: '20px', border: 'none', background: '#222', color: '#FFF' }}
                    placeholder="Type a message..."
                />
                <button onClick={sendMessage} style={{ background: '#38BDF8', color: '#000', border: 'none', borderRadius: '20px', padding: '10px 20px', cursor: 'pointer', fontWeight: 'bold' }}>
                    Send
                </button>
            </div>
        </div>
    );
}

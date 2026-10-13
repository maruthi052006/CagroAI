import os

src_dir = "c:/Users/Sathiyabhama/OneDrive/Desktop/digital twin project/frontend/src"
comp_dir = f"{src_dir}/components"
os.makedirs(f"{comp_dir}/ui", exist_ok=True)
os.makedirs(f"{comp_dir}/messaging", exist_ok=True)
os.makedirs(f"{comp_dir}/coordination", exist_ok=True)

# 1. CropSelector.jsx
crop_selector = """import React, { useState, useEffect } from 'react';
import axios from 'axios';

export function CropSelector({ onSelect, selectedCrop }) {
    const [crops, setCrops] = useState([]);
    const [search, setSearch] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get('/api/crop-registry/')
            .then(res => {
                setCrops(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch crop registry", err);
                setLoading(false);
            });
    }, []);

    if (loading) return <div>Loading crops...</div>;

    const filtered = crops.filter(c => c.displayName.toLowerCase().includes(search.toLowerCase()));
    
    // Group by archetype
    const grouped = filtered.reduce((acc, crop) => {
        const cat = crop.archetype.replace('Archetype', '');
        if (!acc[cat]) acc[cat] = [];
        acc[cat].push(crop);
        return acc;
    }, {});

    return (
        <div style={{ background: '#111A16', color: '#F4F6F5', padding: '16px', borderRadius: '12px', fontFamily: 'Inter' }}>
            <h3 style={{ fontFamily: 'Sora', margin: '0 0 12px 0' }}>Select Crop</h3>
            <input 
                type="text" 
                placeholder="Search crops..." 
                value={search} 
                onChange={e => setSearch(e.target.value)} 
                style={{ width: '100%', padding: '8px', marginBottom: '16px', borderRadius: '6px', border: '1px solid #333', background: '#0B1210', color: '#FFF' }}
            />
            
            <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
                {Object.keys(grouped).map(category => (
                    <div key={category} style={{ marginBottom: '16px' }}>
                        <div style={{ fontSize: '12px', textTransform: 'uppercase', color: '#38BDF8', marginBottom: '8px' }}>{category}</div>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))', gap: '8px' }}>
                            {grouped[category].map(crop => (
                                <div 
                                    key={crop.id}
                                    onClick={() => onSelect(crop.id)}
                                    style={{ 
                                        padding: '12px', 
                                        border: selectedCrop === crop.id ? '2px solid #4ADE80' : '1px solid #333',
                                        borderRadius: '8px',
                                        cursor: 'pointer',
                                        background: selectedCrop === crop.id ? 'rgba(74, 222, 128, 0.1)' : 'transparent',
                                        textAlign: 'center'
                                    }}
                                >
                                    <div>{crop.icon}</div>
                                    <div style={{ fontSize: '14px', marginTop: '4px' }}>{crop.displayName}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
"""
with open(f"{comp_dir}/ui/CropSelector.jsx", "w", encoding="utf-8") as f:
    f.write(crop_selector)

# 2. ChatWindow.jsx
chat_window = """import React, { useState, useEffect, useRef } from 'react';

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
"""
with open(f"{comp_dir}/messaging/ChatWindow.jsx", "w", encoding="utf-8") as f:
    f.write(chat_window)

# 3. AgentCard.jsx
agent_card = """import React from 'react';

export function AgentCard({ agentName, icon, data, status }) {
    const isError = status === 'error';
    
    return (
        <div style={{ 
            background: 'rgba(255,255,255,0.02)', border: isError ? '1px solid #F59E0B' : '1px solid #333', 
            borderRadius: '12px', padding: '16px', color: '#F4F6F5', fontFamily: 'Inter' 
        }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                <span style={{ fontSize: '20px' }}>{icon}</span>
                <h4 style={{ margin: 0, fontFamily: 'Sora' }}>{agentName}</h4>
            </div>
            {isError ? (
                <div style={{ color: '#F59E0B', fontSize: '14px' }}>Agent failed to load data.</div>
            ) : (
                <div style={{ fontSize: '14px', opacity: 0.9 }}>
                    {Object.entries(data).map(([key, value]) => (
                        <div key={key} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                            <span style={{ opacity: 0.7 }}>{key.replace(/_/g, ' ')}</span>
                            <strong>{typeof value === 'number' ? value.toFixed(1) : value}</strong>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
"""
with open(f"{comp_dir}/coordination/AgentCard.jsx", "w", encoding="utf-8") as f:
    f.write(agent_card)

print("UI components created successfully.")

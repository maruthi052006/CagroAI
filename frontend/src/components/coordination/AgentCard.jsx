import React from 'react';

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

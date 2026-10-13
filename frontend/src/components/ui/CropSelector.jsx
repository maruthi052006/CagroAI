import React, { useState, useEffect } from 'react';
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

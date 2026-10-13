import React, { useState } from 'react';

export function TrustScoreBadge({ score, label, breakdown }) {
    const [hover, setHover] = useState(false);
    
    let numericScore = 70;
    let displayLabel = label || 'MODERATE';
    let displayBreakdown = breakdown || null;

    if (score && typeof score === 'object') {
        numericScore = Number(score.trust_score ?? score.score ?? 70);
        displayLabel = score.trust_label ?? score.label ?? displayLabel;
        displayBreakdown = score.breakdown ?? score.trust_breakdown ?? displayBreakdown;
    } else if (typeof score === 'number' || !isNaN(Number(score))) {
        numericScore = Math.round(Number(score));
    }

    const color = numericScore >= 75 ? '#4ADE80' : numericScore >= 50 ? '#F59E0B' : '#EF4444';

    return (
        <div 
            style={{ position: 'relative', cursor: 'pointer' }}
            onMouseEnter={() => setHover(true)}
            onMouseLeave={() => setHover(false)}
        >
            <div style={{ 
                width: '60px', height: '60px', borderRadius: '50%', border: `4px solid ${color}`,
                display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold',
                fontSize: '18px', background: 'rgba(255,255,255,0.05)', color: color
            }}>
                {numericScore}
            </div>

            {hover && displayBreakdown && (
                <div style={{ 
                    position: 'absolute', top: '70px', right: 0, width: '220px', zIndex: 10,
                    background: '#16261E', padding: '12px', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.5)',
                    border: '1px solid rgba(255,255,255,0.1)', fontSize: '13px', color: '#F4F6F5'
                }}>
                    <div style={{ fontWeight: 'bold', marginBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '4px' }}>
                        Trust Score: {displayLabel}
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                        <span>Agreement:</span> <span>{displayBreakdown.agreement ?? 80}/100</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                        <span>Recency:</span> <span>{displayBreakdown.recency ?? 85}/100</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span>History:</span> <span>{displayBreakdown.historical ?? 75}/100</span>
                    </div>
                </div>
            )}
        </div>
    );
}


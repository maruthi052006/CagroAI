import React from 'react';
import { TrustScoreBadge } from '../ui/TrustScoreBadge';
import { ExplainabilityTrace } from './ExplainabilityTrace';

export function CoordinationPanel({ coordinationResult }) {
    if (!coordinationResult) return <div>Loading coordination...</div>;

    const { final_recommendation, trust_score, trust_breakdown, trust_label, reasoning_trace, risk_flags } = coordinationResult;

    return (
        <div style={{ background: '#111A16', borderRadius: '12px', padding: '20px', color: '#F4F6F5', fontFamily: 'Inter' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <h3 style={{ fontFamily: 'Sora', margin: '0 0 16px 0' }}>Cognitive Coordination</h3>
                <TrustScoreBadge score={trust_score} label={trust_label} breakdown={trust_breakdown} />
            </div>
            
            <div style={{ background: '#0B1210', padding: '16px', borderRadius: '8px', borderLeft: '4px solid #4ADE80', marginBottom: '16px' }}>
                <strong>Recommendation:</strong> {final_recommendation}
            </div>

            {risk_flags && risk_flags.length > 0 && (
                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '16px' }}>
                    {risk_flags.map((flag, idx) => (
                        <span key={typeof flag === 'string' ? flag : idx} style={{ background: 'rgba(245,158,11,0.2)', color: '#F59E0B', padding: '4px 8px', borderRadius: '4px', fontSize: '12px' }}>
                            ⚠️ {typeof flag === 'string' ? flag : JSON.stringify(flag)}
                        </span>
                    ))}
                </div>
            )}


            <ExplainabilityTrace trace={reasoning_trace} />
        </div>
    );
}

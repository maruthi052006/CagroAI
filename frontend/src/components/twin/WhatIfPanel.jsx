import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

export function WhatIfPanel({ onSimulationUpdate, baselineYield }) {
    const [irrigation, setIrrigation] = useState(0);
    const [harvestDelay, setHarvestDelay] = useState(0);
    const [fertilizer, setFertilizer] = useState(0);
    const [warning, setWarning] = useState(null);
    const [simulatedYield, setSimulatedYield] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const timeoutId = setTimeout(() => {
            // Mocking API call to /api/simulate/what-if/
            setLoading(true);
            
            // Simple mock logic reflecting backend
            let newYield = baselineYield * (1 + (irrigation * 0.1 / 50) + (fertilizer * 0.1 / 50));
            let warn = null;
            if (harvestDelay > 20) {
                newYield *= 0.9;
                warn = "Harvest delay beyond 20 days increases pest exposure risk.";
            }
            
            setTimeout(() => {
                setSimulatedYield(newYield);
                setWarning(warn);
                setLoading(false);
                
                // Bubble up state to update 3D Twin growth stage
                onSimulationUpdate({
                    irrigation, harvestDelay, fertilizer
                });
            }, 300);
            
        }, 300); // 300ms debounce
        
        return () => clearTimeout(timeoutId);
    }, [irrigation, harvestDelay, fertilizer, baselineYield]);

    const deltaPct = simulatedYield ? ((simulatedYield - baselineYield) / baselineYield) * 100 : 0;

    return (
        <div style={{ background: '#111A16', padding: '20px', borderRadius: '12px', color: '#F4F6F5', fontFamily: 'Inter' }}>
            <h3 style={{ fontFamily: 'Sora', margin: '0 0 16px 0' }}>What-If Simulation</h3>
            
            <div style={{ marginBottom: '16px' }}>
                <label>Irrigation (-50% to +100%): {irrigation}%</label>
                <input type="range" min="-50" max="100" value={irrigation} onChange={(e) => setIrrigation(Number(e.target.value))} style={{ width: '100%' }} />
            </div>
            
            <div style={{ marginBottom: '16px' }}>
                <label>Harvest Timing (-10 to +30 days): {harvestDelay > 0 ? '+' : ''}{harvestDelay} days</label>
                <input type="range" min="-10" max="30" value={harvestDelay} onChange={(e) => setHarvestDelay(Number(e.target.value))} style={{ width: '100%' }} />
            </div>

            <div style={{ marginBottom: '16px' }}>
                <label>Fertilizer (-50% to +100%): {fertilizer}%</label>
                <input type="range" min="-50" max="100" value={fertilizer} onChange={(e) => setFertilizer(Number(e.target.value))} style={{ width: '100%' }} />
            </div>

            {loading ? (
                <div style={{ opacity: 0.7 }}>Recalculating...</div>
            ) : (
                <div>
                    <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                        Simulated Yield: {simulatedYield?.toFixed(0)} kg 
                        <span style={{ color: deltaPct >= 0 ? '#4ADE80' : '#F59E0B', marginLeft: '12px', fontSize: '14px' }}>
                            {deltaPct >= 0 ? '+' : ''}{deltaPct.toFixed(1)}% vs plan
                        </span>
                    </div>
                </div>
            )}
            
            {warning && (
                <div style={{ color: '#F59E0B', marginTop: '12px', fontSize: '14px', background: 'rgba(245, 158, 11, 0.1)', padding: '8px', borderRadius: '4px' }}>
                    ⚠️ {warning}
                </div>
            )}
        </div>
    );
}

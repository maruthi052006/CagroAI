import os

src_dir = "c:/Users/Sathiyabhama/OneDrive/Desktop/digital twin project/frontend/src"
twin_dir = f"{src_dir}/components/twin"
coord_dir = f"{src_dir}/components/coordination"
os.makedirs(twin_dir, exist_ok=True)
os.makedirs(coord_dir, exist_ok=True)

# WhatIfPanel.jsx
what_if = """import React, { useState, useEffect } from 'react';
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
"""
with open(f"{twin_dir}/WhatIfPanel.jsx", "w", encoding="utf-8") as f:
    f.write(what_if)

# ExplainabilityTrace.jsx
trace = """import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export function ExplainabilityTrace({ trace }) {
    const [expanded, setExpanded] = useState(false);

    if (!trace || trace.length === 0) return null;

    return (
        <div style={{ marginTop: '16px', fontFamily: 'Inter', fontSize: '14px' }}>
            <button 
                onClick={() => setExpanded(!expanded)} 
                style={{ background: 'transparent', border: 'none', color: '#38BDF8', cursor: 'pointer', padding: 0 }}
            >
                {expanded ? 'Hide reasoning' : 'Show reasoning'}
            </button>
            
            <AnimatePresence>
                {expanded && (
                    <motion.div 
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        style={{ overflow: 'hidden', marginTop: '12px' }}
                    >
                        {trace.map((step, idx) => (
                            <motion.div 
                                key={idx}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: idx * 0.08 }}
                                style={{ 
                                    display: 'flex', 
                                    gap: '12px', 
                                    marginBottom: '12px',
                                    position: 'relative'
                                }}
                            >
                                {/* Vertical line connector */}
                                {idx < trace.length - 1 && (
                                    <div style={{ position: 'absolute', left: '6px', top: '20px', width: '2px', height: '100%', background: step.conflict ? '#F59E0B' : '#333' }} />
                                )}
                                
                                <div style={{ 
                                    width: '14px', height: '14px', borderRadius: '50%', 
                                    background: step.conflict ? '#F59E0B' : step.final ? '#4ADE80' : '#444',
                                    marginTop: '4px', zIndex: 1
                                }} />
                                
                                <div>
                                    <div style={{ fontWeight: 'bold', color: step.conflict ? '#F59E0B' : step.final ? '#4ADE80' : '#ccc' }}>
                                        {step.actor} {step.confidence && <span style={{ opacity: 0.5, fontSize: '12px' }}>({Math.round(step.confidence * 100)}%)</span>}
                                    </div>
                                    <div style={{ color: '#F4F6F5', opacity: 0.9 }}>{step.statement}</div>
                                </div>
                            </motion.div>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
"""
with open(f"{coord_dir}/ExplainabilityTrace.jsx", "w", encoding="utf-8") as f:
    f.write(trace)

print("Phase 2.6 UI components written.")

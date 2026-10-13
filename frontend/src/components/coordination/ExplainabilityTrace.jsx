import React, { useState } from 'react';
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

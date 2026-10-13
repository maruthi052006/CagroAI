import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

export function YieldDistributionChart({ baseline, simulated }) {
    const mean = Number(baseline?.yield_mean || baseline?.mean || 4500);
    const simMean = simulated ? Number(simulated?.yield_mean || simulated?.mean || mean) : null;
    const p10 = Number(baseline?.yield_p10 || baseline?.p10 || (mean - 550));
    const p90 = Number(baseline?.yield_p90 || baseline?.p90 || (mean + 550));

    // Mock data generation for Recharts area
    const data = [];
    const minRange = Math.max(1000, Math.floor((mean - 2000) / 500) * 500);
    const maxRange = Math.min(15000, Math.ceil((mean + 2000) / 500) * 500);
    const step = Math.max(100, Math.round((maxRange - minRange) / 25));

    for (let i = minRange; i <= maxRange; i += step) {
        const baseVal = Math.exp(-Math.pow(i - mean, 2) / (2 * Math.pow(500, 2)));
        const simVal = simMean ? Math.exp(-Math.pow(i - simMean, 2) / (2 * Math.pow(500, 2))) : 0;
        data.push({ yield: i, baseDensity: Number(baseVal.toFixed(4)), simDensity: Number(simVal.toFixed(4)) });
    }

    return (
        <div style={{ height: '300px', width: '100%', fontFamily: 'Inter', color: '#F4F6F5' }}>
            <ResponsiveContainer>
                <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <XAxis dataKey="yield" stroke="#ccc" />
                    <YAxis hide />
                    <Tooltip contentStyle={{ backgroundColor: '#111A16', borderColor: '#333' }} />
                    <Area type="monotone" dataKey="baseDensity" stroke="#4ADE80" fill="#4ADE80" fillOpacity={0.3} />
                    {simulated && (
                        <Area type="monotone" dataKey="simDensity" stroke="#38BDF8" fill="none" strokeDasharray="5 5" />
                    )}
                    <ReferenceLine x={p10} stroke="#F59E0B" strokeDasharray="3 3" label={{ value: 'p10', fill: '#F59E0B' }} />
                    <ReferenceLine x={p90} stroke="#F59E0B" strokeDasharray="3 3" label={{ value: 'p90', fill: '#F59E0B' }} />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
}

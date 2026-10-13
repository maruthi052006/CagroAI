import os

src_dir = "c:/Users/Sathiyabhama/OneDrive/Desktop/digital twin project/frontend/src"
pages_dir = f"{src_dir}/pages"
components_dir = f"{src_dir}/components"
utils_dir = f"{src_dir}/utils"

os.makedirs(f"{pages_dir}/farmer", exist_ok=True)
os.makedirs(f"{pages_dir}/officer", exist_ok=True)
os.makedirs(f"{pages_dir}/auth", exist_ok=True)
os.makedirs(f"{components_dir}/charts", exist_ok=True)
os.makedirs(f"{components_dir}/ui", exist_ok=True)
os.makedirs(f"{components_dir}/auth", exist_ok=True)
os.makedirs(utils_dir, exist_ok=True)

def write_comp(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# 1. Axios Interceptor (utils/api.js)
api_js = """import axios from 'axios';

const api = axios.create({
    baseURL: '/api/',
});

api.interceptors.request.use(config => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const refreshToken = localStorage.getItem('refresh_token');
                const res = await axios.post('/api/auth/refresh/', { refresh: refreshToken });
                localStorage.setItem('access_token', res.data.access);
                api.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`;
                return api(originalRequest);
            } catch (refreshError) {
                // Logout if refresh fails
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
);

export default api;
"""
write_comp(f"{utils_dir}/api.js", api_js)

# 2. RoleGuard (components/auth/RoleGuard.jsx)
role_guard = """import React from 'react';
import { Navigate } from 'react-router-dom';

export function RoleGuard({ children, allowedRoles }) {
    const role = localStorage.getItem('user_role'); // In a real app, use Zustand/Context
    const isAuthenticated = !!localStorage.getItem('access_token');

    if (!isAuthenticated) return <Navigate to="/login" replace />;
    if (allowedRoles && !allowedRoles.includes(role)) return <Navigate to="/unauthorized" replace />;

    return children;
}
"""
write_comp(f"{components_dir}/auth/RoleGuard.jsx", role_guard)

# 3. YieldDistributionChart.jsx
yield_chart = """import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

export function YieldDistributionChart({ baseline, simulated }) {
    // Mock data generation for Recharts area
    const data = [];
    for (let i = 2000; i <= 7000; i += 200) {
        // Simple mock normal distribution curve
        const baseVal = Math.exp(-Math.pow(i - baseline.yield_mean, 2) / (2 * Math.pow(500, 2)));
        const simVal = simulated ? Math.exp(-Math.pow(i - simulated.yield_mean, 2) / (2 * Math.pow(500, 2))) : 0;
        data.push({ yield: i, baseDensity: baseVal, simDensity: simVal });
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
                    <ReferenceLine x={baseline.p10} stroke="#F59E0B" strokeDasharray="3 3" label={{ value: 'p10', fill: '#F59E0B' }} />
                    <ReferenceLine x={baseline.p90} stroke="#F59E0B" strokeDasharray="3 3" label={{ value: 'p90', fill: '#F59E0B' }} />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
}
"""
write_comp(f"{components_dir}/charts/YieldDistributionChart.jsx", yield_chart)

# 4. CoordinationPanel.jsx
coordination_panel = """import React from 'react';
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
                    {risk_flags.map(flag => (
                        <span key={flag} style={{ background: 'rgba(245,158,11,0.2)', color: '#F59E0B', padding: '4px 8px', borderRadius: '4px', fontSize: '12px' }}>
                            ⚠️ {flag}
                        </span>
                    ))}
                </div>
            )}

            <ExplainabilityTrace trace={reasoning_trace} />
        </div>
    );
}
"""
write_comp(f"{components_dir}/coordination/CoordinationPanel.jsx", coordination_panel)

# 5. TrustScoreBadge.jsx
trust_badge = """import React, { useState } from 'react';

export function TrustScoreBadge({ score, label, breakdown }) {
    const [hover, setHover] = useState(false);
    
    const color = score >= 75 ? '#4ADE80' : score >= 50 ? '#F59E0B' : '#EF4444';

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
                {score}
            </div>

            {hover && breakdown && (
                <div style={{ 
                    position: 'absolute', top: '70px', right: 0, width: '220px', zIndex: 10,
                    background: '#222', padding: '12px', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.5)',
                    fontSize: '13px'
                }}>
                    <div style={{ fontWeight: 'bold', marginBottom: '8px', borderBottom: '1px solid #444', paddingBottom: '4px' }}>
                        Trust Score: {label}
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}><span>Agreement:</span> <span>{breakdown.agreement}/100</span></div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}><span>Recency:</span> <span>{breakdown.recency}/100</span></div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}><span>History:</span> <span>{breakdown.historical}/100</span></div>
                </div>
            )}
        </div>
    );
}
"""
write_comp(f"{components_dir}/ui/TrustScoreBadge.jsx", trust_badge)

print("Remaining frontend UI and API utils written.")

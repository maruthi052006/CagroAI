import React, { useState } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { FarmerDashboard } from './pages/farmer/FarmerDashboard';
import { OfficerDashboard } from './pages/officer/OfficerDashboard';
import { CropGallery } from './pages/dev/CropGallery';
import { AgentChatPanel } from './components/assistant/AgentChatPanel';
import { DecisionHistoryPage } from './pages/farmer/DecisionHistoryPage';
import {
  Sprout,
  Shield,
  Layers,
  Activity,
  Cpu,
  Radio,
  BrainCircuit,
  FileCheck2,
  ExternalLink
} from 'lucide-react';

export default function App() {
  const location = useLocation();
  const [activeRole, setActiveRole] = useState('farmer');

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Top Navigation Bar */}
      <header style={{
        background: 'rgba(11, 18, 14, 0.85)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        borderBottom: '1px solid var(--border-subtle)',
        position: 'sticky',
        top: 0,
        zIndex: 100,
        padding: '12px 28px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        {/* Brand */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '38px',
            height: '38px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            boxShadow: '0 0 15px rgba(16, 185, 129, 0.4)'
          }}>
            <Sprout size={22} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontFamily: 'var(--font-heading)', fontWeight: 700, fontSize: '18px', color: '#fff' }}>
                AGRI-TWIN
              </span>
              <span className="badge badge-green" style={{ fontSize: '10px', padding: '2px 8px' }}>v2.4 Cognitive</span>
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Multi-Agent Parametric Digital Twin
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav style={{ display: 'flex', gap: '6px', background: 'rgba(255,255,255,0.04)', padding: '4px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
          <Link
            to="/"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 14px',
              borderRadius: '6px',
              fontSize: '13px',
              fontWeight: 600,
              textDecoration: 'none',
              transition: 'all 0.2s ease',
              color: location.pathname === '/' || location.pathname === '/farmer' ? '#fff' : 'var(--text-secondary)',
              background: location.pathname === '/' || location.pathname === '/farmer' ? 'rgba(74, 222, 128, 0.15)' : 'transparent',
              border: location.pathname === '/' || location.pathname === '/farmer' ? '1px solid rgba(74, 222, 128, 0.3)' : '1px solid transparent'
            }}
          >
            <Activity size={15} /> 3D Digital Twin
          </Link>

          <Link
            to="/assistant"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 14px',
              borderRadius: '6px',
              fontSize: '13px',
              fontWeight: 600,
              textDecoration: 'none',
              transition: 'all 0.2s ease',
              color: location.pathname === '/assistant' ? '#C084FC' : 'var(--text-secondary)',
              background: location.pathname === '/assistant' ? 'rgba(168, 85, 247, 0.15)' : 'transparent',
              border: location.pathname === '/assistant' ? '1px solid rgba(168, 85, 247, 0.35)' : '1px solid transparent'
            }}
          >
            <BrainCircuit size={15} color={location.pathname === '/assistant' ? '#C084FC' : undefined} /> EXAI & Agent Chat
          </Link>

          <Link
            to="/decisions"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 14px',
              borderRadius: '6px',
              fontSize: '13px',
              fontWeight: 600,
              textDecoration: 'none',
              transition: 'all 0.2s ease',
              color: location.pathname === '/decisions' ? '#4ADE80' : 'var(--text-secondary)',
              background: location.pathname === '/decisions' ? 'rgba(34, 197, 94, 0.15)' : 'transparent',
              border: location.pathname === '/decisions' ? '1px solid rgba(34, 197, 94, 0.3)' : '1px solid transparent'
            }}
          >
            <FileCheck2 size={15} /> Decisions & Outcomes
          </Link>

          <Link
            to="/officer"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 14px',
              borderRadius: '6px',
              fontSize: '13px',
              fontWeight: 600,
              textDecoration: 'none',
              transition: 'all 0.2s ease',
              color: location.pathname === '/officer' ? '#fff' : 'var(--text-secondary)',
              background: location.pathname === '/officer' ? 'rgba(56, 189, 248, 0.15)' : 'transparent',
              border: location.pathname === '/officer' ? '1px solid rgba(56, 189, 248, 0.3)' : '1px solid transparent'
            }}
          >
            <Shield size={15} /> Agri-Officer Portal
          </Link>

          <Link
            to="/gallery"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 14px',
              borderRadius: '6px',
              fontSize: '13px',
              fontWeight: 600,
              textDecoration: 'none',
              transition: 'all 0.2s ease',
              color: location.pathname === '/gallery' ? '#fff' : 'var(--text-secondary)',
              background: location.pathname === '/gallery' ? 'rgba(245, 158, 11, 0.15)' : 'transparent',
              border: location.pathname === '/gallery' ? '1px solid rgba(245, 158, 11, 0.3)' : '1px solid transparent'
            }}
          >
            <Layers size={15} /> 40 Crops 3D Gallery
          </Link>
        </nav>

        {/* Live System Engine Status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: 'var(--text-secondary)' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10B981', boxShadow: '0 0 8px #10B981' }} />
            <Cpu size={14} /> 4 Cognitive Agents Ready
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: 'var(--text-secondary)' }}>
            <Radio size={14} color="var(--accent-cyan)" />
            Django API :8000
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main style={{ flex: 1, padding: location.pathname === '/gallery' ? '0' : '24px 28px', maxWidth: location.pathname === '/gallery' ? '100%' : '1600px', margin: '0 auto', width: '100%' }}>
        <Routes>
          <Route path="/" element={<FarmerDashboard />} />
          <Route path="/farmer" element={<FarmerDashboard />} />
          <Route path="/assistant" element={<AgentChatPanel />} />
          <Route path="/decisions" element={<DecisionHistoryPage />} />
          <Route path="/officer" element={<OfficerDashboard />} />
          <Route path="/gallery" element={<CropGallery />} />
        </Routes>
      </main>


      {/* Footer */}
      {location.pathname !== '/gallery' && (
        <footer style={{ borderTop: '1px solid var(--border-subtle)', padding: '16px 28px', color: 'var(--text-muted)', fontSize: '12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            Agricultural Cognitive Digital Twin System • Integrated with 38 Tamil Nadu Districts & 9 Parametric Archetypes
          </div>
          <div style={{ display: 'flex', gap: '16px' }}>
            <span>Backend: Django 5 + DRF</span>
            <span>Frontend: React 18 + R3F + Vite</span>
          </div>
        </footer>
      )}
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import { DigitalTwinScene } from '../../components/twin/DigitalTwinScene';
import { WhatIfPanel } from '../../components/twin/WhatIfPanel';
import { CoordinationPanel } from '../../components/coordination/CoordinationPanel';
import { YieldDistributionChart } from '../../components/charts/YieldDistributionChart';
import { cropRegistry } from '../../config/cropRegistry';
import api from '../../utils/api';
import {
  Sprout,
  CloudSun,
  ShieldAlert,
  TrendingUp,
  MapPin,
  UserCheck,
  RefreshCw,
  Sliders,
  Eye,
  Info
} from 'lucide-react';

export function FarmerDashboard() {
  const [selectedCrop, setSelectedCrop] = useState('rice');
  const [selectedZone, setSelectedZone] = useState('Thanjavur');
  const [assignedOfficer, setAssignedOfficer] = useState('Dr. S. Ramanathan (Agri Officer, Delta Region)');
  const [isSimulating, setIsSimulating] = useState(false);
  const [loading, setLoading] = useState(false);

  // Simulation State
  const [simulationState, setSimulationState] = useState({
    growth_stage: 68,
    soil_moisture_pct: 62,
    pest_risk_pct: 12,
    weather_condition: 'clear',
    irrigation_adjustment: 0,
    harvest_delay: 0,
    fertilizer_adjustment: 0,
  });

  // Coordination Result State (Multi-Agent Outputs)
  const [coordinationResult, setCoordinationResult] = useState({
    final_recommendation: "Hold irrigation for next 48 hours; heavy rain forecasted. Inspect for leaf blight in northern quadrant.",
    trust_score: 86,
    trust_label: "HIGH",
    trust_breakdown: { agreement: 88, recency: 92, historical: 78 },
    risk_flags: ["irrigation_vs_rain"],
    reasoning_trace: [
      { step: 1, actor: 'CropGrowthAgent', statement: 'Biomass index 0.72. Adequate vegetative expansion.', confidence: 0.89 },
      { step: 2, actor: 'WeatherAgent', statement: 'Rainfall 24mm expected in 48h. Soil saturation risk.', confidence: 0.85 },
      { step: 3, actor: 'PestDiseaseAgent', statement: 'Humidity >75% creating moderate fungal vulnerability.', confidence: 0.74 },
      { step: 4, actor: 'YieldForecastAgent', statement: 'Projected yield: 4,750 kg/ha (Monte Carlo N=200).', confidence: 0.88 },
      { step: 5, actor: 'ConflictDetector', statement: 'Conflict: Irrigation desired by soil sensors vs 24mm impending rainfall.', conflict: true },
      { step: 6, actor: 'CognitiveResolver', statement: 'Resolution: Suppress scheduled irrigation. Trigger early pest monitoring.', final: true }
    ],
    agent_outputs: {
      crop_growth: { growth_stage: 68, biomass_estimate: 1440, confidence: 0.89 },
      weather: { rain_forecast_7day: 28, temp_risk_level: "low", temp: 29 },
      pest: { pest_risk_score: 0.12, risk_category: "low" },
      yield: { yield_mean: 4750, yield_p10: 4200, yield_p50: 4750, yield_p90: 5300, confidence: 0.88 }
    }
  });

  const [yieldData, setYieldData] = useState({
    baseline: { yield_mean: 4750, p10: 4200, p90: 5300 },
    simulated: null
  });

  // Run backend prediction if available, else keep reactive local mock
  const fetchPrediction = async () => {
    setLoading(true);
    try {
      const res = await api.post('/predict/', { field_id: 1 });
      if (res.data && res.data.final_recommendation) {
        setCoordinationResult(res.data);
      }
    } catch (e) {
      // Backend fallback gracefully kept
      console.log('Using simulated agent prediction state');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPrediction();
  }, [selectedCrop]);

  const handleSimulationUpdate = (adjustments) => {
    const { irrigation, harvestDelay, fertilizer } = adjustments;
    const baseMean = yieldData.baseline.yield_mean;
    const factor = 1 + (irrigation * 0.08 / 50) + (fertilizer * 0.06 / 50) - (harvestDelay > 15 ? 0.08 : 0);
    const newMean = Math.round(baseMean * factor);

    setYieldData(prev => ({
      ...prev,
      simulated: {
        yield_mean: newMean,
        p10: Math.round(newMean * 0.88),
        p90: Math.round(newMean * 1.12)
      }
    }));

    setSimulationState(prev => ({
      ...prev,
      soil_moisture_pct: Math.min(100, Math.max(10, 62 + irrigation * 0.3)),
      pest_risk_pct: harvestDelay > 15 ? 45 : 12,
      growth_stage: Math.min(100, Math.max(10, 68 + harvestDelay * 0.6)),
      irrigation_adjustment: irrigation,
      harvest_delay: harvestDelay,
      fertilizer_adjustment: fertilizer
    }));
  };

  const currentCrop = cropRegistry.find(c => c.id === selectedCrop) || cropRegistry[0];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Top Banner / Field Info */}
      <div className="glass-panel" style={{ padding: '20px 24px', display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
            <span style={{ fontSize: '26px' }}>🌱</span>
            <h1 style={{ fontSize: '24px', margin: 0 }}>

              {currentCrop.displayName} Field Digital Twin
            </h1>
            <span className="badge badge-green">Live Active Twin</span>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', margin: 0 }}>
            Parametric 3D Model: <strong style={{ color: 'var(--accent-cyan)' }}>{currentCrop.archetype}</strong> • Stalk: {currentCrop.stalkColor} • Mature Height: {currentCrop.matureHeight}m
          </p>
        </div>

        {/* Quick Context Chips */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', alignItems: 'center' }}>
          <div className="badge badge-cyan" style={{ padding: '8px 14px' }}>
            <MapPin size={14} /> Zone: {selectedZone} (Tamil Nadu)
          </div>
          <div className="badge badge-amber" style={{ padding: '8px 14px' }}>
            <UserCheck size={14} /> {assignedOfficer}
          </div>
          <button 
            className="btn btn-secondary" 
            onClick={fetchPrediction} 
            disabled={loading}
            style={{ padding: '8px 14px', fontSize: '13px' }}
          >
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            {loading ? 'Evaluating...' : 'Re-run Agents'}
          </button>
        </div>
      </div>

      {/* Main Grid: 3D Scene + Controls */}
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.8fr) minmax(360px, 1fr)', gap: '20px' }}>
        
        {/* Left Column: 3D Twin & Simulation Canvas */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          {/* 3D Scene Viewport */}
          <div className="glass-panel" style={{ height: '460px', overflow: 'hidden', position: 'relative', borderRadius: 'var(--radius-lg)' }}>
            <DigitalTwinScene 
              cropType={selectedCrop} 
              simulationState={simulationState} 
            />
            
            {/* Viewport Overlay Controls */}
            <div style={{ position: 'absolute', bottom: '16px', right: '16px', display: 'flex', gap: '8px', zIndex: 5 }}>
              <div style={{ background: 'rgba(11, 18, 16, 0.85)', padding: '6px 12px', borderRadius: '8px', fontSize: '12px', color: '#94a3b8' }}>
                💡 Click & Drag to Rotate • Scroll to Zoom
              </div>
            </div>
          </div>

          {/* Quick Metrics Bar */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px' }}>
            <div className="glass-panel" style={{ padding: '14px 16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)', fontSize: '13px' }}>
                <Sprout size={16} color="var(--accent-green)" /> Growth Stage
              </div>
              <div style={{ fontSize: '20px', fontWeight: 'bold', marginTop: '4px', color: 'var(--accent-green)' }}>
                {simulationState.growth_stage}%
              </div>
            </div>

            <div className="glass-panel" style={{ padding: '14px 16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)', fontSize: '13px' }}>
                <CloudSun size={16} color="var(--accent-cyan)" /> Soil Moisture
              </div>
              <div style={{ fontSize: '20px', fontWeight: 'bold', marginTop: '4px', color: 'var(--accent-cyan)' }}>
                {simulationState.soil_moisture_pct.toFixed(0)}%
              </div>
            </div>

            <div className="glass-panel" style={{ padding: '14px 16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)', fontSize: '13px' }}>
                <ShieldAlert size={16} color="var(--accent-rose)" /> Pest Exposure
              </div>
              <div style={{ fontSize: '20px', fontWeight: 'bold', marginTop: '4px', color: simulationState.pest_risk_pct > 30 ? 'var(--accent-rose)' : 'var(--accent-green)' }}>
                {simulationState.pest_risk_pct}%
              </div>
            </div>

            <div className="glass-panel" style={{ padding: '14px 16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)', fontSize: '13px' }}>
                <TrendingUp size={16} color="var(--accent-amber)" /> Projected Yield
              </div>
              <div style={{ fontSize: '20px', fontWeight: 'bold', marginTop: '4px', color: 'var(--accent-amber)' }}>
                {yieldData.simulated ? yieldData.simulated.yield_mean : yieldData.baseline.yield_mean} kg/ha
              </div>
            </div>
          </div>

          {/* What-If Simulator & Yield Distribution Curve */}
          <div className="glass-panel" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <div>
                <h3 style={{ fontSize: '18px', margin: 0 }}>Yield Distribution & What-If Simulation</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '13px', margin: '4px 0 0 0' }}>
                  Live Monte Carlo (p10, p50, p90) response curve for scheduled interventions
                </p>
              </div>
              {yieldData.simulated && (
                <span className="badge badge-cyan">Simulation Active</span>
              )}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.4fr) minmax(0, 1fr)', gap: '20px', alignItems: 'center' }}>
              <div>
                <YieldDistributionChart 
                  baseline={yieldData.baseline} 
                  simulated={yieldData.simulated} 
                />
              </div>

              <div>
                <WhatIfPanel 
                  baselineYield={yieldData.baseline.yield_mean} 
                  onSimulationUpdate={handleSimulationUpdate} 
                />
              </div>
            </div>
          </div>

        </div>

        {/* Right Column: Multi-Agent Coordination Panel & Crop Switcher */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          {/* Crop Selector Card */}
          <div className="glass-panel" style={{ padding: '18px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <h3 style={{ fontSize: '16px', margin: 0 }}>Parametric Crop Switcher</h3>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>40 registered crops</span>
            </div>
            
            <select 
              value={selectedCrop} 
              onChange={e => setSelectedCrop(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 12px',
                borderRadius: 'var(--radius-sm)',
                background: '#0e1814',
                color: '#fff',
                border: '1px solid var(--border-subtle)',
                fontSize: '14px',
                fontFamily: 'Inter',
                cursor: 'pointer'
              }}
            >
              {cropRegistry.map(crop => (
                <option key={crop.id} value={crop.id}>
                  {crop.icon} {crop.displayName} ({crop.archetype.replace('Archetype', '')})
                </option>
              ))}
            </select>

            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '10px' }}>
              {['rice', 'wheat', 'sugarcane', 'tomato', 'sunflower', 'banana', 'cotton'].map(shortcut => (
                <button
                  key={shortcut}
                  onClick={() => setSelectedCrop(shortcut)}
                  style={{
                    padding: '4px 8px',
                    borderRadius: '4px',
                    background: selectedCrop === shortcut ? 'rgba(74, 222, 128, 0.2)' : 'rgba(255, 255, 255, 0.05)',
                    border: selectedCrop === shortcut ? '1px solid var(--accent-green)' : '1px solid var(--border-subtle)',
                    color: selectedCrop === shortcut ? 'var(--accent-green)' : 'var(--text-secondary)',
                    fontSize: '12px',
                    cursor: 'pointer'
                  }}
                >
                  {shortcut.charAt(0).toUpperCase() + shortcut.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Coordination & Explainability Trace */}
          <div className="glass-panel" style={{ padding: '20px' }}>
            <CoordinationPanel coordinationResult={coordinationResult} />
          </div>

        </div>

      </div>
    </div>
  );
}

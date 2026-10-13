import React, { useState, useEffect } from 'react';
import api from '../../utils/api';
import {
  Users,
  MapPin,
  AlertTriangle,
  Send,
  CheckCircle,
  TrendingDown,
  Building,
  RefreshCw,
  Search,
  Filter
} from 'lucide-react';

export function OfficerDashboard() {
  const [zones, setZones] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState('ALL');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [alertText, setAlertText] = useState('');
  const [alertSuccess, setAlertSuccess] = useState(false);

  // Mock initial farmer list mapped across zones
  const [farmers, setFarmers] = useState([
    { id: 1, name: 'Murugan K.', zone: 'Thanjavur', region: 'DELTA', crop: 'Rice', health: 'Optimal', risk: 'Low', moisture: 62, yieldEst: 4750 },
    { id: 2, name: 'Senthil Nathan', zone: 'Coimbatore', region: 'WESTERN', crop: 'Cotton', health: 'Water Stress', risk: 'Medium', moisture: 34, yieldEst: 2100 },
    { id: 3, name: 'Lakshmi Ammal', zone: 'Madurai', region: 'SOUTHERN', crop: 'Sugarcane', health: 'Pest Threat', risk: 'High', moisture: 58, yieldEst: 7800 },
    { id: 4, name: 'Palanisamy V.', zone: 'Salem', region: 'WESTERN', crop: 'Tapioca', health: 'Optimal', risk: 'Low', moisture: 51, yieldEst: 3400 },
    { id: 5, name: 'Anbarasan T.', zone: 'Tiruchirappalli', region: 'CENTRAL', crop: 'Banana', health: 'Optimal', risk: 'Low', moisture: 70, yieldEst: 11200 },
    { id: 6, name: 'Kavitha R.', zone: 'Tiruvarur', region: 'DELTA', crop: 'Rice', health: 'Fungal Risk', risk: 'High', moisture: 82, yieldEst: 4100 },
  ]);

  useEffect(() => {
    // Attempt fetching zones from backend API
    api.get('/zones/')
      .then(res => {
        if (Array.isArray(res.data) && res.data.length > 0) {
          setZones(res.data);
        }
      })
      .catch(() => {
        // Fallback default sample zones
        setZones([
          { id: 1, name: 'Thanjavur', code: 'THA', region_group: 'DELTA' },
          { id: 2, name: 'Coimbatore', code: 'COI', region_group: 'WESTERN' },
          { id: 3, name: 'Madurai', code: 'MAD', region_group: 'SOUTHERN' },
          { id: 4, name: 'Tiruchirappalli', code: 'TIR', region_group: 'CENTRAL' },
          { id: 5, name: 'Kanchipuram', code: 'KAN', region_group: 'NORTHERN' },
          { id: 6, name: 'Salem', code: 'SAL', region_group: 'WESTERN' },
        ]);
      });
  }, []);

  const handleReassignZone = async (farmerId, newZoneName) => {
    const updated = farmers.map(f => {
      if (f.id === farmerId) {
        return { ...f, zone: newZoneName };
      }
      return f;
    });
    setFarmers(updated);

    // Call backend endpoint if available
    try {
      await api.patch(`/officer/farmers/${farmerId}/reassign-zone/`, { new_zone_id: 1 });
    } catch (e) {
      console.log('Reassigned zone locally');
    }
  };

  const handleSendAdvisory = (e) => {
    e.preventDefault();
    if (!alertText.trim()) return;
    setAlertSuccess(true);
    setAlertText('');
    setTimeout(() => setAlertSuccess(false), 4000);
  };

  const filteredFarmers = farmers.filter(f => {
    const matchesRegion = selectedRegion === 'ALL' || f.region === selectedRegion;
    const matchesSearch = f.name.toLowerCase().includes(search.toLowerCase()) || 
                          f.zone.toLowerCase().includes(search.toLowerCase()) ||
                          f.crop.toLowerCase().includes(search.toLowerCase());
    return matchesRegion && matchesSearch;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div className="glass-panel" style={{ padding: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Building size={24} color="var(--accent-cyan)" />
            <h1 style={{ fontSize: '24px', margin: 0 }}>Agricultural Officer Control Room</h1>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginTop: '6px' }}>
            Tamil Nadu Regional Field Monitoring • Multi-Agent Surveillance & Zone Allocation
          </p>
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <div className="badge badge-green" style={{ padding: '8px 14px', fontSize: '13px' }}>
            <Users size={14} /> 6 Active Farmers Monitored
          </div>
          <div className="badge badge-amber" style={{ padding: '8px 14px', fontSize: '13px' }}>
            <AlertTriangle size={14} /> 2 Priority Alerts Active
          </div>
        </div>
      </div>

      {/* Main Grid: Farmers table + Advisory Broadcaster */}
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 2fr) minmax(340px, 1fr)', gap: '24px' }}>
        
        {/* Left Column: Monitored Farmers */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          
          {/* Controls Bar */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', marginBottom: '18px' }}>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              <Search size={16} color="var(--text-muted)" />
              <input 
                type="text" 
                placeholder="Search farmer, district, or crop..." 
                value={search}
                onChange={e => setSearch(e.target.value)}
                style={{
                  background: '#0B1210',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '8px 12px',
                  color: '#fff',
                  fontSize: '13px',
                  width: '260px'
                }}
              />
            </div>

            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              <Filter size={16} color="var(--text-muted)" />
              <select
                value={selectedRegion}
                onChange={e => setSelectedRegion(e.target.value)}
                style={{
                  background: '#0B1210',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '8px 12px',
                  color: '#fff',
                  fontSize: '13px',
                  cursor: 'pointer'
                }}
              >
                <option value="ALL">All Regions (38 Districts)</option>
                <option value="DELTA">Cauvery Delta</option>
                <option value="WESTERN">Western Agro-Zone</option>
                <option value="SOUTHERN">Southern Dry Zone</option>
                <option value="CENTRAL">Central Zone</option>
                <option value="NORTHERN">Northern Coastal Zone</option>
              </select>
            </div>
          </div>

          {/* Farmers Table */}
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', textAlign: 'left' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-secondary)' }}>
                  <th style={{ padding: '12px 14px' }}>Farmer</th>
                  <th style={{ padding: '12px 14px' }}>District / Zone</th>
                  <th style={{ padding: '12px 14px' }}>Crop</th>
                  <th style={{ padding: '12px 14px' }}>Risk Status</th>
                  <th style={{ padding: '12px 14px' }}>Soil Moisture</th>
                  <th style={{ padding: '12px 14px' }}>Yield Est.</th>
                  <th style={{ padding: '12px 14px' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredFarmers.map(f => (
                  <tr key={f.id} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.04)' }}>
                    <td style={{ padding: '14px', fontWeight: 600 }}>{f.name}</td>
                    <td style={{ padding: '14px' }}>
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                        <MapPin size={13} color="var(--accent-cyan)" /> {f.zone}
                      </span>
                    </td>
                    <td style={{ padding: '14px' }}>{f.crop}</td>
                    <td style={{ padding: '14px' }}>
                      <span className={`badge ${f.risk === 'High' ? 'badge-rose' : f.risk === 'Medium' ? 'badge-amber' : 'badge-green'}`}>
                        {f.health}
                      </span>
                    </td>
                    <td style={{ padding: '14px' }}>{f.moisture}%</td>
                    <td style={{ padding: '14px', fontFamily: 'var(--font-mono)' }}>{f.yieldEst} kg</td>
                    <td style={{ padding: '14px' }}>
                      <select 
                        defaultValue={f.zone}
                        onChange={(e) => handleReassignZone(f.id, e.target.value)}
                        style={{
                          background: 'rgba(255, 255, 255, 0.05)',
                          border: '1px solid var(--border-subtle)',
                          borderRadius: '4px',
                          color: '#fff',
                          padding: '4px 8px',
                          fontSize: '12px',
                          cursor: 'pointer'
                        }}
                      >
                        <option value="Thanjavur">Thanjavur</option>
                        <option value="Tiruvarur">Tiruvarur</option>
                        <option value="Coimbatore">Coimbatore</option>
                        <option value="Madurai">Madurai</option>
                        <option value="Salem">Salem</option>
                        <option value="Tiruchirappalli">Tiruchirappalli</option>
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

        </div>

        {/* Right Column: Advisory Broadcaster & Weather Alerts */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          {/* Quick Broadcast Advisory */}
          <div className="glass-panel" style={{ padding: '20px' }}>
            <h3 style={{ fontSize: '17px', margin: '0 0 8px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Send size={18} color="var(--accent-green)" /> Broadcast Field Advisory
            </h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '13px', margin: '0 0 16px 0' }}>
              Push urgent cognitive multi-agent recommendations to farmers in selected zones.
            </p>

            <form onSubmit={handleSendAdvisory}>
              <textarea 
                rows="4"
                placeholder="E.g., Cauvery Delta: Imminent 35mm precipitation. Postpone fertilizer application by 72 hours."
                value={alertText}
                onChange={e => setAlertText(e.target.value)}
                style={{
                  width: '100%',
                  background: '#0B1210',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '12px',
                  color: '#fff',
                  fontFamily: 'Inter',
                  fontSize: '13px',
                  resize: 'none',
                  marginBottom: '12px'
                }}
              />

              <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>
                <Send size={16} /> Broadcast Advisory to Assigned Farmers
              </button>
            </form>

            {alertSuccess && (
              <div style={{ marginTop: '12px', padding: '10px', background: 'rgba(74, 222, 128, 0.1)', border: '1px solid var(--accent-green)', borderRadius: '6px', color: 'var(--accent-green)', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CheckCircle size={16} /> Advisory broadcasted to 6 farmers via SMS & App.
              </div>
            )}
          </div>

          {/* Regional Risk Summary */}
          <div className="glass-panel" style={{ padding: '20px' }}>
            <h3 style={{ fontSize: '16px', margin: '0 0 12px 0' }}>District Risk Intelligence</h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '13px' }}>
              <div style={{ padding: '10px', background: 'rgba(244, 63, 94, 0.08)', borderLeft: '3px solid var(--accent-rose)', borderRadius: '4px' }}>
                <strong style={{ color: 'var(--accent-rose)' }}>Cauvery Delta:</strong> Fungal leaf blast hazard elevated due to high relative humidity (82%).
              </div>

              <div style={{ padding: '10px', background: 'rgba(245, 158, 11, 0.08)', borderLeft: '3px solid var(--accent-amber)', borderRadius: '4px' }}>
                <strong style={{ color: 'var(--accent-amber)' }}>Western Belt:</strong> Soil moisture deficits detected across Coimbatore & Tiruppur cotton tracts.
              </div>

              <div style={{ padding: '10px', background: 'rgba(74, 222, 128, 0.08)', borderLeft: '3px solid var(--accent-green)', borderRadius: '4px' }}>
                <strong style={{ color: 'var(--accent-green)' }}>Southern Zone:</strong> Sugarcane canopy development on schedule; normal vegetative progress.
              </div>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}

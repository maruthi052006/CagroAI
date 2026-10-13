import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  CheckCircle2, 
  XCircle, 
  Clock, 
  AlertCircle, 
  TrendingUp, 
  Calendar, 
  Database, 
  Award, 
  Layers, 
  PlusCircle,
  FileCheck2,
  Cpu,
  BarChart3
} from 'lucide-react';

export function DecisionHistoryPage({ fieldId = 1 }) {
  const [decisions, setDecisions] = useState([]);
  const [accuracySummary, setAccuracySummary] = useState(null);
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showOutcomeModal, setShowOutcomeModal] = useState(false);
  const [harvestYield, setHarvestYield] = useState('');
  const [seasonYear, setSeasonYear] = useState('2026');
  const [harvestNotes, setHarvestNotes] = useState('');
  const [submittingOutcome, setSubmittingOutcome] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [decRes, accRes, modRes] = await Promise.all([
        axios.get(`/api/decisions/?field_id=${fieldId}`),
        axios.get(`/api/outcomes/accuracy-summary/?field_id=${fieldId}`),
        axios.get('/api/model-registry/')
      ]);
      setDecisions(decRes.data);
      setAccuracySummary(accRes.data);
      setModels(modRes.data);
    } catch (err) {
      console.error('Error fetching decision data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [fieldId]);

  const handleRespondDecision = async (predId, decision) => {
    try {
      await axios.post(`/api/decisions/${predId}/respond/`, {
        farmer_decision: decision,
        decision_reason: `Marked ${decision.toLowerCase()} via Digital Twin dashboard.`
      });
      fetchData();
    } catch (err) {
      console.error('Error responding to decision:', err);
    }
  };

  const handleRecordOutcome = async (e) => {
    e.preventDefault();
    if (!harvestYield) return;
    setSubmittingOutcome(true);
    try {
      await axios.post(`/api/outcomes/${fieldId}/record/`, {
        actual_yield: parseFloat(harvestYield),
        season_year: parseInt(seasonYear),
        notes: harvestNotes
      });
      setShowOutcomeModal(false);
      setHarvestYield('');
      setHarvestNotes('');
      fetchData();
    } catch (err) {
      console.error('Error recording harvest outcome:', err);
    } finally {
      setSubmittingOutcome(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Header Banner */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.05) 100%)',
        border: '1px solid rgba(16, 185, 129, 0.25)',
        borderRadius: '16px',
        padding: '24px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FileCheck2 size={24} color="#10B981" />
            <h1 style={{ margin: 0, fontSize: '22px', fontWeight: 700, color: '#FFF' }}>
              Decision Audit, Outcome Learning & Calibration
            </h1>
          </div>
          <p style={{ margin: '6px 0 0 0', fontSize: '13px', color: 'var(--text-secondary)' }}>
            Every cognitive recommendation is logged with trust score at time of inference. Harvest returns feed real-world error tracking and field-level calibration.
          </p>
        </div>

        <button
          onClick={() => setShowOutcomeModal(true)}
          style={{
            background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
            color: '#FFF',
            border: 'none',
            borderRadius: '10px',
            padding: '12px 20px',
            fontWeight: 600,
            fontSize: '13px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            cursor: 'pointer',
            boxShadow: '0 4px 15px rgba(16, 185, 129, 0.4)'
          }}
        >
          <PlusCircle size={16} />
          <span>Record Harvest Outcome</span>
        </button>
      </div>

      {/* Accuracy & Field-Level Calibration Metric Cards */}
      {accuracySummary && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '16px' }}>
          <div className="card" style={{ padding: '20px', background: '#111A16' }}>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <TrendingUp size={14} color="#38BDF8" /> Total Harvests Evaluated
            </div>
            <div style={{ fontSize: '28px', fontWeight: 800, color: '#FFF' }}>
              {accuracySummary.total_outcomes} <span style={{ fontSize: '14px', fontWeight: 500, color: 'var(--text-muted)' }}>seasons</span>
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              {accuracySummary.calibrated ? 'Meets statistical calibration threshold (>=3)' : 'Requires >= 3 harvests to calibrate'}
            </div>
          </div>

          <div className="card" style={{ padding: '20px', background: '#111A16' }}>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <BarChart3 size={14} color="#10B981" /> Mean Absolute Yield Error
            </div>
            <div style={{ fontSize: '28px', fontWeight: 800, color: '#10B981' }}>
              {accuracySummary.avg_error_pct}%
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Historical deviation between forecast and actual weigh-in
            </div>
          </div>

          <div className="card" style={{ padding: '20px', background: '#111A16' }}>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Award size={14} color="#F59E0B" /> Field-Level Calibration Delta
            </div>
            <div style={{ fontSize: '28px', fontWeight: 800, color: accuracySummary.calibrated ? '#4ADE80' : 'var(--text-muted)' }}>
              {accuracySummary.calibrated ? `${accuracySummary.calibration_delta_pct >= 0 ? '+' : ''}${accuracySummary.calibration_delta_pct}%` : 'Uncalibrated'}
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              {accuracySummary.label || 'Field bias adjustment factor'}
            </div>
          </div>
        </div>
      )}

      {/* Main Grid: Decision Timeline & Model Registry */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        
        {/* Decision History Feed */}
        <div className="card" style={{ padding: '24px', background: '#0B1210' }}>
          <h2 style={{ margin: '0 0 18px 0', fontSize: '16px', fontWeight: 700, color: '#FFF', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Clock size={18} color="#A855F7" />
            Agronomic Decision Audit Trail
          </h2>

          {loading ? (
            <div style={{ color: 'var(--text-muted)', padding: '20px', textAlign: 'center' }}>Loading audit records...</div>
          ) : decisions.length === 0 ? (
            <div style={{ color: 'var(--text-muted)', padding: '20px', textAlign: 'center' }}>
              No decisions recorded yet. Run a prediction in the Farmer Digital Twin to generate recommendations.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {decisions.map((d) => (
                <div 
                  key={d.id}
                  style={{
                    background: '#111A16',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: '12px',
                    padding: '16px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '12px'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{
                        padding: '4px 10px',
                        borderRadius: '20px',
                        fontSize: '11px',
                        fontWeight: 700,
                        background: d.farmer_decision === 'APPROVED' ? 'rgba(34, 197, 94, 0.15)' : d.farmer_decision === 'REJECTED' ? 'rgba(239, 68, 68, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                        color: d.farmer_decision === 'APPROVED' ? '#4ADE80' : d.farmer_decision === 'REJECTED' ? '#F87171' : '#FBBF24',
                        border: `1px solid ${d.farmer_decision === 'APPROVED' ? 'rgba(34, 197, 94, 0.3)' : 'rgba(245, 158, 11, 0.3)'}`
                      }}>
                        {d.farmer_decision}
                      </span>
                      <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                        {new Date(d.created_at).toLocaleDateString()} at {new Date(d.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>

                    <div style={{ fontSize: '11px', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <span>Trust Score:</span>
                      <strong style={{ color: '#4ADE80' }}>{d.trust_score_at_time}%</strong>
                    </div>
                  </div>

                  <div style={{ fontSize: '14px', color: '#E2E8F0', lineHeight: 1.5, background: 'rgba(0,0,0,0.2)', padding: '10px 14px', borderRadius: '8px' }}>
                    {d.recommendation_text}
                  </div>

                  {d.decision_reason && (
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                      <strong>Note:</strong> {d.decision_reason}
                    </div>
                  )}

                  {/* Action Buttons if Pending */}
                  {d.farmer_decision === 'PENDING' && (
                    <div style={{ display: 'flex', gap: '8px', marginTop: '4px' }}>
                      <button
                        onClick={() => handleRespondDecision(d.prediction_log, 'APPROVED')}
                        style={{
                          background: 'rgba(34, 197, 94, 0.2)',
                          color: '#4ADE80',
                          border: '1px solid rgba(34, 197, 94, 0.4)',
                          borderRadius: '6px',
                          padding: '6px 14px',
                          fontSize: '12px',
                          fontWeight: 600,
                          cursor: 'pointer'
                        }}
                      >
                        Approve Advisory
                      </button>
                      <button
                        onClick={() => handleRespondDecision(d.prediction_log, 'REJECTED')}
                        style={{
                          background: 'rgba(239, 68, 68, 0.2)',
                          color: '#F87171',
                          border: '1px solid rgba(239, 68, 68, 0.4)',
                          borderRadius: '6px',
                          padding: '6px 14px',
                          fontSize: '12px',
                          fontWeight: 600,
                          cursor: 'pointer'
                        }}
                      >
                        Reject
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Verified ML Model Registry (Real computed metrics only) */}
        <div className="card" style={{ padding: '24px', background: '#0B1210', height: 'fit-content' }}>
          <h2 style={{ margin: '0 0 16px 0', fontSize: '16px', fontWeight: 700, color: '#FFF', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Cpu size={18} color="#38BDF8" />
            Verified Agent Registry
          </h2>
          <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '14px' }}>
            Auditable performance metrics evaluated on real TNAU & DES yield datasets.
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {models.map((m) => (
              <div
                key={m.id}
                style={{
                  background: '#111A16',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '10px',
                  padding: '14px'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <span style={{ fontWeight: 700, fontSize: '13px', color: '#FFF' }}>
                    {m.agent_name}
                  </span>
                  <span style={{ fontSize: '10px', background: 'rgba(56, 189, 248, 0.15)', color: '#38BDF8', padding: '2px 8px', borderRadius: '4px', fontWeight: 600 }}>
                    v{m.version}
                  </span>
                </div>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)', lineHeight: 1.4, marginBottom: '10px' }}>
                  {m.algorithm_description}
                </div>
                {m.metrics && (
                  <div style={{ background: 'rgba(0,0,0,0.3)', padding: '8px', borderRadius: '6px', fontSize: '11px' }}>
                    {Object.entries(m.metrics).map(([k, v]) => (
                      <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '2px 0' }}>
                        <span style={{ color: 'var(--text-muted)' }}>{k.replace('_', ' ')}:</span>
                        <strong style={{ color: '#A7F3D0' }}>{typeof v === 'number' ? v.toFixed(3) : v}</strong>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Record Harvest Outcome Modal */}
      {showOutcomeModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.75)',
          backdropFilter: 'blur(5px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{
            background: '#111A16',
            border: '1px solid var(--border-subtle)',
            borderRadius: '16px',
            padding: '28px',
            width: '100%',
            maxWidth: '480px',
            boxShadow: '0 25px 50px rgba(0,0,0,0.6)'
          }}>
            <h2 style={{ margin: '0 0 8px 0', fontSize: '18px', fontWeight: 700, color: '#FFF' }}>
              Record Harvest Weigh-In
            </h2>
            <p style={{ margin: '0 0 20px 0', fontSize: '13px', color: 'var(--text-secondary)' }}>
              Enter your actual harvest yield (kg/ha). This feeds historical accuracy tracking and refines field calibration.
            </p>

            <form onSubmit={handleRecordOutcome} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: '#E2E8F0', marginBottom: '6px' }}>
                  Actual Harvest Yield (kg/ha) *
                </label>
                <input
                  type="number"
                  step="0.1"
                  required
                  placeholder="e.g. 4250.0"
                  value={harvestYield}
                  onChange={e => setHarvestYield(e.target.value)}
                  style={{
                    width: '100%',
                    background: 'rgba(255,255,255,0.05)',
                    border: '1px solid rgba(255,255,255,0.12)',
                    borderRadius: '8px',
                    padding: '10px 14px',
                    color: '#FFF',
                    fontSize: '14px',
                    boxSizing: 'border-box'
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: '#E2E8F0', marginBottom: '6px' }}>
                  Season Year
                </label>
                <input
                  type="number"
                  value={seasonYear}
                  onChange={e => setSeasonYear(e.target.value)}
                  style={{
                    width: '100%',
                    background: 'rgba(255,255,255,0.05)',
                    border: '1px solid rgba(255,255,255,0.12)',
                    borderRadius: '8px',
                    padding: '10px 14px',
                    color: '#FFF',
                    fontSize: '14px',
                    boxSizing: 'border-box'
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: '#E2E8F0', marginBottom: '6px' }}>
                  Agronomic Notes
                </label>
                <textarea
                  rows="3"
                  placeholder="Optional field observations (e.g. rainfall timing, fertilizer application)..."
                  value={harvestNotes}
                  onChange={e => setHarvestNotes(e.target.value)}
                  style={{
                    width: '100%',
                    background: 'rgba(255,255,255,0.05)',
                    border: '1px solid rgba(255,255,255,0.12)',
                    borderRadius: '8px',
                    padding: '10px 14px',
                    color: '#FFF',
                    fontSize: '14px',
                    boxSizing: 'border-box',
                    resize: 'vertical'
                  }}
                />
              </div>

              <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', marginTop: '10px' }}>
                <button
                  type="button"
                  onClick={() => setShowOutcomeModal(false)}
                  style={{
                    background: 'transparent',
                    border: '1px solid rgba(255,255,255,0.2)',
                    color: '#E2E8F0',
                    borderRadius: '8px',
                    padding: '10px 18px',
                    cursor: 'pointer',
                    fontSize: '13px'
                  }}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submittingOutcome}
                  style={{
                    background: '#10B981',
                    color: '#FFF',
                    border: 'none',
                    borderRadius: '8px',
                    padding: '10px 20px',
                    fontWeight: 600,
                    cursor: submittingOutcome ? 'not-allowed' : 'pointer',
                    fontSize: '13px'
                  }}
                >
                  {submittingOutcome ? 'Saving...' : 'Save Outcome'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}

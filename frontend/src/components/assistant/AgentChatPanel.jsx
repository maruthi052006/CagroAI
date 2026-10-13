import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  Bot, 
  BrainCircuit, 
  CloudSun, 
  Bug, 
  TrendingUp, 
  Send, 
  ShieldCheck, 
  Database, 
  CheckCircle2, 
  HelpCircle, 
  Sparkles,
  Info,
  ChevronRight
} from 'lucide-react';

const PERSONAS = [
  {
    id: 'EXAI',
    name: 'EXAI Synthesizer',
    role: 'Explainable AI Orchestrator',
    icon: BrainCircuit,
    color: '#A855F7',
    bg: 'rgba(168, 85, 247, 0.15)',
    border: 'rgba(168, 85, 247, 0.35)',
    description: 'Synthesizes all 4 agents, arbitrates conflicts, walks decision trees, and explains farm health index.',
    suggestions: [
      'Why this recommendation?',
      'How confident are you in this forecast?',
      'What conflicts were detected?',
      'Explain my farm health score'
    ]
  },
  {
    id: 'CROP',
    name: 'Crop Growth Agent',
    role: 'Biophysical Growth Specialist',
    icon: Bot,
    color: '#22C55E',
    bg: 'rgba(34, 197, 94, 0.15)',
    border: 'rgba(34, 197, 94, 0.35)',
    description: 'Tracks biophysical phenology, Gaussian thermal suitability, and water stress accumulation.',
    suggestions: [
      'What is my crop growth stage?',
      'What is current biomass estimate?',
      'How confident is the growth model?'
    ]
  },
  {
    id: 'WEATHER',
    name: 'Weather Agent',
    role: 'Agrometeorological Specialist',
    icon: CloudSun,
    color: '#38BDF8',
    bg: 'rgba(56, 189, 248, 0.15)',
    border: 'rgba(56, 189, 248, 0.35)',
    description: 'Analyzes NASA POWER agroclimatology, precipitation anomaly, and extreme thermal risks.',
    suggestions: [
      'Will it rain this week?',
      'What is the extreme temperature risk?',
      'Show 7-day weather outlook'
    ]
  },
  {
    id: 'PEST',
    name: 'Pest & Disease Agent',
    role: 'Epidemiological Forecaster',
    icon: Bug,
    color: '#F59E0B',
    bg: 'rgba(245, 158, 11, 0.15)',
    border: 'rgba(245, 158, 11, 0.35)',
    description: 'Evaluates relative humidity thresholds, pathogen vectors, and pest proliferation risks.',
    suggestions: [
      'What is the current pest outbreak risk?',
      'Why is pest risk elevated?',
      'What pests threaten this crop?'
    ]
  },
  {
    id: 'YIELD',
    name: 'Yield Forecast Agent',
    role: 'Stochastic Yield Modeler',
    icon: TrendingUp,
    color: '#EC4899',
    bg: 'rgba(236, 72, 153, 0.15)',
    border: 'rgba(236, 72, 153, 0.35)',
    description: 'Runs 1,000-sample Monte Carlo probabilistic yield distributions with confidence bands.',
    suggestions: [
      'What is the forecasted yield?',
      'Show yield uncertainty distribution',
      'What are the p10 and p90 bounds?'
    ]
  }
];

export function AgentChatPanel({ fieldId = 1, currentCrop = 'rice' }) {
  const [selectedPersona, setSelectedPersona] = useState('EXAI');
  const [messages, setMessages] = useState({});
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const activePersonaObj = PERSONAS.find(p => p.id === selectedPersona);

  // Initialize greeting messages per persona
  useEffect(() => {
    const initialMsgs = {};
    PERSONAS.forEach(p => {
      initialMsgs[p.id] = [
        {
          id: 'welcome-' + p.id,
          sender: 'AGENT',
          text: p.id === 'EXAI' 
            ? `Greetings! I am EXAI, the Explainable AI synthesis engine for your field. I synthesize data from all 4 cognitive agents to explain every advisory, conflict arbitration, and farm health metric with 100% auditable provenance.`
            : `Hello! I am your ${p.name}. I monitor real ${p.id.toLowerCase()} telemetry and calibrated ag-models for your ${currentCrop} field. Ask me anything about ${p.role.toLowerCase()} observations.`,
          data_sources_used: ['TNAU Agronomic Baseline', 'Digital Twin State Engine'],
          intent_detected: 'GENERAL_GREETING'
        }
      ];
    });
    setMessages(initialMsgs);
  }, [currentCrop]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, selectedPersona]);

  const handleSend = async (messageText) => {
    const textToSend = messageText || input;
    if (!textToSend.trim() || loading) return;

    const userMsg = {
      id: 'usr-' + Date.now(),
      sender: 'USER',
      text: textToSend,
      created_at: new Date().toISOString()
    };

    setMessages(prev => ({
      ...prev,
      [selectedPersona]: [...(prev[selectedPersona] || []), userMsg]
    }));
    setInput('');
    setLoading(true);

    try {
      const res = await axios.post(`/api/agent-chat/${selectedPersona}/message/`, {
        field_id: fieldId,
        text: textToSend
      });

      const agentReply = {
        id: 'agent-' + Date.now(),
        sender: 'AGENT',
        text: res.data.text,
        data_sources_used: res.data.data_sources_used || [],
        intent_detected: res.data.intent_detected,
        clarification: res.data.intent_detected === 'CLARIFICATION'
      };

      setMessages(prev => ({
        ...prev,
        [selectedPersona]: [...(prev[selectedPersona] || []), agentReply]
      }));
    } catch (err) {
      console.error('Chat error:', err);
      const fallbackReply = {
        id: 'agent-' + Date.now(),
        sender: 'AGENT',
        text: "I was unable to retrieve live telemetry for this query right now. Please verify your field selection or try asking one of the recommended domain questions.",
        data_sources_used: ['Local Fallback Rulebase'],
        intent_detected: 'CLARIFICATION',
        clarification: true
      };
      setMessages(prev => ({
        ...prev,
        [selectedPersona]: [...(prev[selectedPersona] || []), fallbackReply]
      }));
    } finally {
      setLoading(false);
    }
  };

  const currentMessages = messages[selectedPersona] || [];

  return (
    <div style={{
      background: '#0B1210',
      border: '1px solid var(--border-subtle)',
      borderRadius: '16px',
      overflow: 'hidden',
      display: 'flex',
      flexDirection: 'column',
      height: '740px',
      boxShadow: '0 20px 40px rgba(0,0,0,0.5)'
    }}>
      {/* Header with Security & Zero External LLM Guardrail Badge */}
      <div style={{
        padding: '16px 20px',
        background: 'linear-gradient(90deg, #111A16 0%, #17241E 100%)',
        borderBottom: '1px solid var(--border-subtle)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: '10px',
            background: activePersonaObj.bg,
            border: `1px solid ${activePersonaObj.border}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: activePersonaObj.color
          }}>
            <activePersonaObj.icon size={22} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontWeight: 700, fontSize: '16px', color: '#FFF' }}>
                {activePersonaObj.name}
              </span>
              <span style={{
                fontSize: '11px',
                padding: '2px 8px',
                borderRadius: '6px',
                background: activePersonaObj.bg,
                color: activePersonaObj.color,
                border: `1px solid ${activePersonaObj.border}`,
                fontWeight: 600
              }}>
                {activePersonaObj.role}
              </span>
            </div>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '2px' }}>
              {activePersonaObj.description}
            </div>
          </div>
        </div>

        {/* Non-negotiable Audit Badge */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          background: 'rgba(34, 197, 94, 0.1)',
          border: '1px solid rgba(34, 197, 94, 0.25)',
          padding: '6px 12px',
          borderRadius: '20px',
          fontSize: '11px',
          color: '#4ADE80',
          fontWeight: 600
        }}>
          <ShieldCheck size={14} />
          <span>Zero External LLM • 100% Grounded Local Inference</span>
        </div>
      </div>

      {/* 5-Persona Tabs */}
      <div style={{
        display: 'flex',
        background: '#0E1713',
        borderBottom: '1px solid var(--border-subtle)',
        padding: '6px 12px',
        gap: '8px'
      }}>
        {PERSONAS.map(p => {
          const isSelected = selectedPersona === p.id;
          const Icon = p.icon;
          return (
            <button
              key={p.id}
              onClick={() => setSelectedPersona(p.id)}
              style={{
                flex: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                padding: '8px 12px',
                borderRadius: '8px',
                border: isSelected ? `1px solid ${p.border}` : '1px solid transparent',
                background: isSelected ? p.bg : 'transparent',
                color: isSelected ? p.color : 'var(--text-secondary)',
                fontWeight: isSelected ? 700 : 500,
                fontSize: '13px',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              <Icon size={16} />
              <span>{p.id}</span>
            </button>
          );
        })}
      </div>

      {/* Chat Messages Body */}
      <div style={{
        flex: 1,
        padding: '20px',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
        background: 'radial-gradient(circle at 50% 0%, rgba(168, 85, 247, 0.03) 0%, transparent 70%)'
      }}>
        {currentMessages.map((m) => {
          const isUser = m.sender === 'USER';
          return (
            <div
              key={m.id}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: isUser ? 'flex-end' : 'flex-start',
                maxWidth: '85%',
                alignSelf: isUser ? 'flex-end' : 'flex-start'
              }}
            >
              {/* Bubble */}
              <div style={{
                background: isUser ? '#10B981' : '#14201B',
                color: '#FFF',
                padding: '14px 18px',
                borderRadius: isUser ? '16px 16px 2px 16px' : '16px 16px 16px 2px',
                border: isUser ? 'none' : '1px solid rgba(168, 85, 247, 0.2)',
                fontSize: '14px',
                lineHeight: '1.6',
                boxShadow: isUser 
                  ? '0 4px 15px rgba(16, 185, 129, 0.3)' 
                  : '0 4px 15px rgba(0, 0, 0, 0.3)'
              }}>
                {m.text}

                {/* Clarification Help Box */}
                {m.clarification && (
                  <div style={{
                    marginTop: '12px',
                    padding: '10px 14px',
                    background: 'rgba(168, 85, 247, 0.1)',
                    borderRadius: '8px',
                    border: '1px solid rgba(168, 85, 247, 0.2)',
                    fontSize: '12px'
                  }}>
                    <div style={{ fontWeight: 600, color: '#C084FC', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <HelpCircle size={14} /> Recommended queries I can answer:
                    </div>
                    <ul style={{ margin: 0, paddingLeft: '18px', color: 'var(--text-secondary)' }}>
                      {activePersonaObj.suggestions.map((s, idx) => (
                        <li key={idx} style={{ cursor: 'pointer', padding: '2px 0' }} onClick={() => handleSend(s)}>
                          <span style={{ color: '#E9D5FF', textDecoration: 'underline' }}>{s}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Provenance Grounding Footer for Agent Bubbles */}
              {!isUser && m.data_sources_used && m.data_sources_used.length > 0 && (
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  flexWrap: 'wrap',
                  gap: '6px',
                  marginTop: '6px',
                  paddingLeft: '4px'
                }}>
                  <span style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Database size={11} /> Grounded in:
                  </span>
                  {m.data_sources_used.map((src, i) => (
                    <span
                      key={i}
                      style={{
                        fontSize: '10px',
                        background: 'rgba(255, 255, 255, 0.05)',
                        border: '1px solid rgba(255, 255, 255, 0.12)',
                        color: '#A7F3D0',
                        padding: '2px 8px',
                        borderRadius: '10px',
                        fontWeight: 500
                      }}
                    >
                      {src}
                    </span>
                  ))}
                </div>
              )}
            </div>
          );
        })}

        {loading && (
          <div style={{
            alignSelf: 'flex-start',
            background: '#14201B',
            border: '1px solid rgba(168, 85, 247, 0.2)',
            padding: '12px 18px',
            borderRadius: '16px 16px 16px 2px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            color: '#C084FC',
            fontSize: '13px'
          }}>
            <Sparkles size={16} className="animate-spin" />
            <span>Consulting cognitive agent knowledge base & reasoning trace...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Quick-Replies */}
      <div style={{
        padding: '10px 16px',
        background: '#0E1713',
        borderTop: '1px solid var(--border-subtle)',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        overflowX: 'auto',
        whiteSpace: 'nowrap'
      }}>
        <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 600 }}>
          Suggested:
        </span>
        {activePersonaObj.suggestions.map((s, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(s)}
            style={{
              background: 'rgba(255, 255, 255, 0.04)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              color: '#E2E8F0',
              padding: '4px 12px',
              borderRadius: '14px',
              fontSize: '12px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              transition: 'all 0.15s ease'
            }}
            onMouseEnter={e => {
              e.currentTarget.style.background = activePersonaObj.bg;
              e.currentTarget.style.borderColor = activePersonaObj.border;
              e.currentTarget.style.color = activePersonaObj.color;
            }}
            onMouseLeave={e => {
              e.currentTarget.style.background = 'rgba(255, 255, 255, 0.04)';
              e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)';
              e.currentTarget.style.color = '#E2E8F0';
            }}
          >
            <span>{s}</span>
            <ChevronRight size={12} />
          </button>
        ))}
      </div>

      {/* Message Input Box */}
      <div style={{
        padding: '16px 20px',
        background: '#111A16',
        borderTop: '1px solid var(--border-subtle)',
        display: 'flex',
        gap: '12px',
        alignItems: 'center'
      }}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          placeholder={`Ask ${activePersonaObj.name} about your field...`}
          style={{
            flex: 1,
            background: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid rgba(255, 255, 255, 0.12)',
            borderRadius: '10px',
            padding: '12px 16px',
            color: '#FFF',
            fontSize: '14px',
            outline: 'none'
          }}
        />
        <button
          onClick={() => handleSend()}
          disabled={!input.trim() || loading}
          style={{
            background: input.trim() && !loading ? activePersonaObj.color : '#334155',
            color: '#FFF',
            border: 'none',
            borderRadius: '10px',
            padding: '12px 20px',
            cursor: input.trim() && !loading ? 'pointer' : 'not-allowed',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            transition: 'all 0.2s ease'
          }}
        >
          <span>Send</span>
          <Send size={16} />
        </button>
      </div>
    </div>
  );
}

import React, { useMemo } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Html, Environment } from '@react-three/drei';
import { cropRegistry } from '../../config/cropRegistry';
import * as Archetypes from './archetypes';

// The main 3D scene
export function DigitalTwinScene({ cropType, simulationState }) {
    const { growth_stage, soil_moisture_pct, pest_risk_pct, weather_condition } = simulationState;
    
    const cropConfig = useMemo(() => {
        return cropRegistry.find(c => c.id === cropType) || cropRegistry[0];
    }, [cropType]);

    const ArchetypeComponent = Archetypes[cropConfig.archetype] || Archetypes.GrassStalkArchetype;

    
    // Grid parameters
    const gridSize = 10;
    const spacing = cropConfig.density === 'high' ? 0.3 : cropConfig.density === 'medium' ? 0.6 : 1.0;
    const offset = (gridSize * spacing) / 2;

    const groundColor = soil_moisture_pct > 60 ? '#3d2817' : soil_moisture_pct > 30 ? '#593e26' : '#73573c';

    return (
        <div style={{ width: '100%', height: '100%', position: 'relative', background: '#0B1210' }}>
            <Canvas camera={{ position: [5, 5, 5], fov: 50 }}>
                <React.Suspense fallback={null}>
                    <ambientLight intensity={weather_condition === 'clear' ? 1.0 : 0.6} />
                    <directionalLight position={[10, 10, 5]} intensity={1.5} />
                    
                    {/* Terrain */}
                    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]}>
                        <planeGeometry args={[20, 20]} />
                        <meshStandardMaterial color={groundColor} roughness={0.9} />
                    </mesh>

                    {/* Plants Grid */}
                    <group position={[-offset, 0, -offset]}>
                        {[...Array(gridSize)].map((_, x) => 
                            [...Array(gridSize)].map((_, z) => {
                                // Jitter to make it look natural
                                const jitterX = ((x * 17 + z * 31) % 10 - 5) * 0.01;
                                const jitterZ = ((x * 23 + z * 13) % 10 - 5) * 0.01;
                                const hasPest = ((x * 7 + z * 11) % 100) < pest_risk_pct;
                                
                                return (
                                    <group key={`${x}-${z}`} position={[x * spacing + jitterX, 0, z * spacing + jitterZ]}>
                                        <ArchetypeComponent 
                                            growthStage={growth_stage / 100} 
                                            {...cropConfig} 
                                        />
                                        {/* Pest Indicator */}
                                        {hasPest && (
                                            <mesh position={[0, cropConfig.matureHeight || 1, 0]}>
                                                <sphereGeometry args={[0.05]} />
                                                <meshBasicMaterial color="#EF4444" />
                                            </mesh>
                                        )}
                                    </group>
                                );
                            })
                        )}
                    </group>

                    <OrbitControls makeDefault maxPolarAngle={Math.PI / 2 - 0.05} minDistance={2} maxDistance={20} />
                    <Environment preset="forest" />
                </React.Suspense>
            </Canvas>

            {/* HUD */}
            <div style={{ position: 'absolute', top: 20, left: 20, color: '#F4F6F5', background: 'rgba(11, 18, 16, 0.7)', padding: '12px', borderRadius: '12px' }}>
                <h3 style={{ margin: '0 0 8px 0', fontFamily: 'Sora' }}>{cropConfig.displayName} Field</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', fontSize: '14px', fontFamily: 'Inter' }}>
                    <span>Growth: {growth_stage}%</span>
                    <span>Soil Moisture: {soil_moisture_pct}%</span>
                    <span>Pest Risk: {pest_risk_pct}%</span>
                    <span>Weather: {weather_condition}</span>
                </div>
            </div>
        </div>
    );
}

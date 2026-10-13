import os

src_dir = "c:/Users/Sathiyabhama/OneDrive/Desktop/digital twin project/frontend/src"
twin_dir = f"{src_dir}/components/twin"
os.makedirs(twin_dir, exist_ok=True)

digital_twin_scene = """import React, { useMemo } from 'react';
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

    const ArchetypeComponent = Archetypes[cropConfig.archetype];
    
    // Grid parameters
    const gridSize = 10;
    const spacing = cropConfig.density === 'high' ? 0.3 : cropConfig.density === 'medium' ? 0.6 : 1.0;
    const offset = (gridSize * spacing) / 2;

    const groundColor = soil_moisture_pct > 60 ? '#3d2817' : soil_moisture_pct > 30 ? '#593e26' : '#73573c';

    return (
        <div style={{ width: '100%', height: '100%', position: 'relative', background: '#0B1210' }}>
            <Canvas camera={{ position: [5, 5, 5], fov: 50 }}>
                <ambientLight intensity={weather_condition === 'clear' ? 1.0 : 0.6} />
                <directionalLight position={[10, 10, 5]} intensity={1.5} />
                
                {/* Terrain */}
                <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]}>
                    <planeGeometry args={[20, 20]} />
                    <meshStandardMaterial color={groundColor} />
                </mesh>

                {/* Plants Grid */}
                <group position={[-offset, 0, -offset]}>
                    {[...Array(gridSize)].map((_, x) => 
                        [...Array(gridSize)].map((_, z) => {
                            // Jitter to make it look natural
                            const jitterX = (Math.random() - 0.5) * 0.1;
                            const jitterZ = (Math.random() - 0.5) * 0.1;
                            const hasPest = Math.random() < (pest_risk_pct / 100);
                            
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
                                            <meshBasicMaterial color="red" />
                                        </mesh>
                                    )}
                                </group>
                            );
                        })
                    )}
                </group>

                {/* Weather overlays could go here (e.g. rain particles) */}
                
                <OrbitControls />
                <Environment preset="forest" />
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
"""

with open(f"{twin_dir}/DigitalTwinScene.jsx", "w") as f:
    f.write(digital_twin_scene)

# Export all archetypes from archetypes/index.js
archetypes_index = """export { GrassStalkArchetype } from './GrassStalkArchetype';
export { BulbArchetype } from './BulbArchetype';
export { RootLeafArchetype } from './RootLeafArchetype';
export { FlowerHeadArchetype } from './FlowerHeadArchetype';
export { BushFruitArchetype } from './BushFruitArchetype';
export { LegumeBushArchetype } from './LegumeBushArchetype';
export { VineArchetype } from './VineArchetype';
export { PseudostemArchetype } from './PseudostemArchetype';
export { FiberStalkArchetype } from './FiberStalkArchetype';
"""

with open(f"{twin_dir}/archetypes/index.js", "w") as f:
    f.write(archetypes_index)

print("DigitalTwinScene and Archetype exports written.")

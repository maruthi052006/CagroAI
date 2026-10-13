import React, { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import { cropRegistry } from '../../config/cropRegistry';
import * as Archetypes from '../../components/twin/archetypes';

export function CropGallery() {
    const [growthStage, setGrowthStage] = useState(1.0); // Fully mature by default

    // Create a 8x5 grid (40 crops)
    const columns = 8;
    const spacing = 1.5;

    return (
        <div style={{ width: '100vw', height: '100vh', background: '#0B1210', position: 'relative', color: '#F4F6F5', fontFamily: 'Inter' }}>
            
            <div style={{ position: 'absolute', top: 20, left: 20, zIndex: 10, background: 'rgba(0,0,0,0.7)', padding: '16px', borderRadius: '12px' }}>
                <h2 style={{ margin: '0 0 12px 0', fontFamily: 'Sora' }}>Dev Crop Gallery (All 40 Crops)</h2>
                <div>
                    <label style={{ display: 'block', marginBottom: '8px' }}>Global Growth Stage: {Math.round(growthStage * 100)}%</label>
                    <input 
                        type="range" 
                        min="0.01" 
                        max="1.0" 
                        step="0.01" 
                        value={growthStage} 
                        onChange={(e) => setGrowthStage(parseFloat(e.target.value))} 
                        style={{ width: '100%' }}
                    />
                </div>
            </div>

            <Canvas camera={{ position: [0, 8, 12], fov: 45 }}>
                <React.Suspense fallback={null}>
                    <ambientLight intensity={0.7} />
                    <directionalLight position={[10, 10, 5]} intensity={1.5} />
                    
                    <group position={[-((columns - 1) * spacing) / 2, 0, -3]}>
                        {cropRegistry.map((crop, index) => {
                            const ArchetypeComponent = Archetypes[crop.archetype];
                            const x = index % columns;
                            const z = Math.floor(index / columns);

                            if (!ArchetypeComponent) return null; // Fallback for safety

                            return (
                                <group key={crop.id} position={[x * spacing, 0, z * spacing]}>
                                    {/* Platform per crop */}
                                    <mesh position={[0, -0.05, 0]}>
                                        <cylinderGeometry args={[0.5, 0.5, 0.1, 16]} />
                                        <meshStandardMaterial color="#222" />
                                    </mesh>

                                    <ArchetypeComponent 
                                        growthStage={growthStage} 
                                        {...crop} 
                                    />
                                </group>
                            );
                        })}
                    </group>

                    <OrbitControls makeDefault />
                    <Environment preset="forest" />
                </React.Suspense>
            </Canvas>
        </div>
    );
}

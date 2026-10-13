import os

project_dir = "c:/Users/Sathiyabhama/OneDrive/Desktop/digital twin project/frontend"
src_dir = f"{project_dir}/src"
arch_dir = f"{src_dir}/components/twin/archetypes"
os.makedirs(arch_dir, exist_ok=True)

def write_comp(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# Common import for archetypes
common_imports = """import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useSpring, animated } from '@react-spring/three';
import * as THREE from 'three';
"""

# 1. GrassStalkArchetype.jsx
grass = common_imports + """
export function GrassStalkArchetype({ growthStage, stalkColor, headColor, matureHeight = 1 }) {
    const { scale } = useSpring({ scale: Math.max(0.01, growthStage), config: { mass: 1, tension: 170, friction: 26 } });
    return (
        <animated.group scale={scale}>
            {/* Stalk */}
            <mesh position={[0, matureHeight / 2, 0]}>
                <cylinderGeometry args={[0.02, 0.05, matureHeight, 8]} />
                <meshStandardMaterial color={stalkColor} />
            </mesh>
            {/* Spike/Panicle Head */}
            {growthStage > 0.6 && (
                <mesh position={[0, matureHeight + 0.1, 0]}>
                    <coneGeometry args={[0.06, 0.2, 8]} />
                    <meshStandardMaterial color={headColor} />
                </mesh>
            )}
        </animated.group>
    );
}
"""
write_comp(f"{arch_dir}/GrassStalkArchetype.jsx", grass)

# 2. BulbArchetype.jsx
bulb = common_imports + """
export function BulbArchetype({ growthStage, stalkColor, headColor, matureHeight = 0.4 }) {
    const { scale } = useSpring({ scale: Math.max(0.01, growthStage) });
    return (
        <animated.group scale={scale}>
            {/* Base Bulb */}
            <mesh position={[0, 0.05, 0]}>
                <sphereGeometry args={[0.1, 16, 16]} />
                <meshStandardMaterial color={headColor} />
            </mesh>
            {/* Tubular Leaves */}
            {[...Array(5)].map((_, i) => (
                <mesh key={i} position={[0, matureHeight / 2, 0]} rotation={[0, 0, (i - 2) * 0.2]}>
                    <cylinderGeometry args={[0.01, 0.02, matureHeight, 8]} />
                    <meshStandardMaterial color={stalkColor} />
                </mesh>
            ))}
        </animated.group>
    );
}
"""
write_comp(f"{arch_dir}/BulbArchetype.jsx", bulb)

# 3. RootLeafArchetype.jsx
root = common_imports + """
export function RootLeafArchetype({ growthStage, leafColor, headColor, matureHeight = 0.3 }) {
    const { scale } = useSpring({ scale: Math.max(0.01, growthStage) });
    return (
        <animated.group scale={scale}>
            {/* Root (partially below ground) */}
            <mesh position={[0, -0.1, 0]}>
                <coneGeometry args={[0.1, 0.3, 16]} rotation={[Math.PI, 0, 0]} />
                <meshStandardMaterial color={headColor} />
            </mesh>
            {/* Broad Leaves */}
            <mesh position={[0, matureHeight / 2, 0]}>
                <sphereGeometry args={[0.2, 8, 8]} scale={[1, 0.2, 1]} />
                <meshStandardMaterial color={leafColor} />
            </mesh>
        </animated.group>
    );
}
"""
write_comp(f"{arch_dir}/RootLeafArchetype.jsx", root)

# 4. FlowerHeadArchetype.jsx
flower = common_imports + """
export function FlowerHeadArchetype({ growthStage, stalkColor, headColor, matureHeight = 1.2 }) {
    const { scale } = useSpring({ scale: Math.max(0.01, growthStage) });
    return (
        <animated.group scale={scale}>
            <mesh position={[0, matureHeight / 2, 0]}>
                <cylinderGeometry args={[0.03, 0.05, matureHeight, 8]} />
                <meshStandardMaterial color={stalkColor} />
            </mesh>
            {growthStage > 0.5 && (
                <mesh position={[0, matureHeight, 0]} rotation={[0.2, 0, 0]}>
                    <cylinderGeometry args={[0.2, 0.2, 0.05, 16]} />
                    <meshStandardMaterial color={headColor} />
                </mesh>
            )}
        </animated.group>
    );
}
"""
write_comp(f"{arch_dir}/FlowerHeadArchetype.jsx", flower)

# 5. BushFruitArchetype.jsx
bush = common_imports + """
export function BushFruitArchetype({ growthStage, stalkColor, leafColor, headColor, matureHeight = 0.8 }) {
    const { scale } = useSpring({ scale: Math.max(0.01, growthStage) });
    return (
        <animated.group scale={scale}>
            {/* Bush Trunk */}
            <mesh position={[0, matureHeight / 2, 0]}>
                <cylinderGeometry args={[0.04, 0.08, matureHeight, 8]} />
                <meshStandardMaterial color={stalkColor} />
            </mesh>
            {/* Foliage */}
            <mesh position={[0, matureHeight * 0.8, 0]}>
                <sphereGeometry args={[0.3, 16, 16]} />
                <meshStandardMaterial color={leafColor} transparent opacity={0.9} />
            </mesh>
            {/* Fruits */}
            {growthStage > 0.7 && [...Array(6)].map((_, i) => (
                <mesh key={i} position={[
                    Math.sin(i) * 0.25, 
                    matureHeight * 0.7 + Math.cos(i) * 0.2, 
                    Math.cos(i * 2) * 0.25
                ]}>
                    <sphereGeometry args={[0.05, 8, 8]} />
                    <meshStandardMaterial color={headColor} />
                </mesh>
            ))}
        </animated.group>
    );
}
"""
write_comp(f"{arch_dir}/BushFruitArchetype.jsx", bush)

# 6. LegumeBushArchetype.jsx
legume = common_imports + """
export function LegumeBushArchetype({ growthStage, stalkColor, leafColor, headColor, matureHeight = 0.5 }) {
    const { scale } = useSpring({ scale: Math.max(0.01, growthStage) });
    return (
        <animated.group scale={scale}>
            <mesh position={[0, matureHeight / 2, 0]}>
                <cylinderGeometry args={[0.1, 0.05, matureHeight, 8]} />
                <meshStandardMaterial color={leafColor} />
            </mesh>
            {growthStage > 0.6 && (
                <mesh position={[0.1, matureHeight * 0.6, 0.1]}>
                    <capsuleGeometry args={[0.02, 0.1, 4, 8]} />
                    <meshStandardMaterial color={headColor} />
                </mesh>
            )}
        </animated.group>
    );
}
"""
write_comp(f"{arch_dir}/LegumeBushArchetype.jsx", legume)

# 7. VineArchetype.jsx
vine = common_imports + """
export function VineArchetype({ growthStage, leafColor, headColor, matureHeight = 1 }) {
    const { scale } = useSpring({ scale: Math.max(0.01, growthStage) });
    return (
        <animated.group scale={scale}>
            {/* Trellis / main vine */}
            <mesh position={[0, matureHeight / 2, 0]}>
                <cylinderGeometry args={[0.02, 0.02, matureHeight, 8]} />
                <meshStandardMaterial color={'#4a3c31'} />
            </mesh>
            <mesh position={[0, matureHeight * 0.6, 0]} rotation={[0, 0, Math.PI/4]}>
                <cylinderGeometry args={[0.01, 0.01, 0.5, 8]} />
                <meshStandardMaterial color={leafColor} />
            </mesh>
            {growthStage > 0.5 && (
                <mesh position={[0.2, matureHeight * 0.4, 0]}>
                    <sphereGeometry args={[0.1, 16, 16]} scale={[1, 1.5, 1]} />
                    <meshStandardMaterial color={headColor} />
                </mesh>
            )}
        </animated.group>
    );
}
"""
write_comp(f"{arch_dir}/VineArchetype.jsx", vine)

# 8. PseudostemArchetype.jsx (Banana)
banana = common_imports + """
export function PseudostemArchetype({ growthStage, stalkColor, leafColor, headColor, matureHeight = 2.0 }) {
    const { scale } = useSpring({ scale: Math.max(0.01, growthStage) });
    return (
        <animated.group scale={scale}>
            {/* Pseudostem */}
            <mesh position={[0, matureHeight / 2, 0]}>
                <cylinderGeometry args={[0.15, 0.25, matureHeight, 16]} />
                <meshStandardMaterial color={stalkColor} />
            </mesh>
            {/* Giant Leaves */}
            {[...Array(4)].map((_, i) => (
                <mesh key={i} position={[0, matureHeight, 0]} rotation={[0, i * Math.PI/2, Math.PI/3]}>
                    <planeGeometry args={[0.4, 1.2]} />
                    <meshStandardMaterial color={leafColor} side={THREE.DoubleSide} />
                </mesh>
            ))}
            {/* Fruit Bunch */}
            {growthStage > 0.8 && (
                <mesh position={[0.2, matureHeight * 0.8, 0]} rotation={[0, 0, -Math.PI/6]}>
                    <cylinderGeometry args={[0.05, 0.1, 0.4, 8]} />
                    <meshStandardMaterial color={headColor} />
                </mesh>
            )}
        </animated.group>
    );
}
"""
write_comp(f"{arch_dir}/PseudostemArchetype.jsx", banana)

# 9. FiberStalkArchetype.jsx (Jute, Sesame)
fiber = common_imports + """
export function FiberStalkArchetype({ growthStage, stalkColor, leafColor, matureHeight = 1.5 }) {
    const { scale } = useSpring({ scale: Math.max(0.01, growthStage) });
    return (
        <animated.group scale={scale}>
            <mesh position={[0, matureHeight / 2, 0]}>
                <cylinderGeometry args={[0.015, 0.03, matureHeight, 8]} />
                <meshStandardMaterial color={stalkColor} />
            </mesh>
            {/* Sparse leaves */}
            {[...Array(6)].map((_, i) => (
                <mesh key={i} position={[0, (matureHeight / 6) * i + 0.2, 0]} rotation={[0.2, i, 0]}>
                    <planeGeometry args={[0.05, 0.15]} />
                    <meshStandardMaterial color={leafColor} side={THREE.DoubleSide} />
                </mesh>
            ))}
        </animated.group>
    );
}
"""
write_comp(f"{arch_dir}/FiberStalkArchetype.jsx", fiber)

print("Archetypes built.")

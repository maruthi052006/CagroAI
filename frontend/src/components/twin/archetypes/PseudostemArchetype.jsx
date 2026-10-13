import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useSpring, animated } from '@react-spring/three';
import * as THREE from 'three';

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

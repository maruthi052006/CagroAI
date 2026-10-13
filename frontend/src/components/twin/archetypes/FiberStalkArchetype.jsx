import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useSpring, animated } from '@react-spring/three';
import * as THREE from 'three';

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

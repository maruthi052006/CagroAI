import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useSpring, animated } from '@react-spring/three';
import * as THREE from 'three';

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

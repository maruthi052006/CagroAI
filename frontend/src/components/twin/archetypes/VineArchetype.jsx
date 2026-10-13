import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useSpring, animated } from '@react-spring/three';
import * as THREE from 'three';

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

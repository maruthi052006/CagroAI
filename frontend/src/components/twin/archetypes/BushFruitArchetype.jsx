import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useSpring, animated } from '@react-spring/three';
import * as THREE from 'three';

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

import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useSpring, animated } from '@react-spring/three';
import * as THREE from 'three';

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

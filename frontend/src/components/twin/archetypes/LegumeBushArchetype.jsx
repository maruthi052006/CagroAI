import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useSpring, animated } from '@react-spring/three';
import * as THREE from 'three';

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

import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useSpring, animated } from '@react-spring/three';
import * as THREE from 'three';

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

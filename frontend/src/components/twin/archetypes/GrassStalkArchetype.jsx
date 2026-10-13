import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useSpring, animated } from '@react-spring/three';
import * as THREE from 'three';

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

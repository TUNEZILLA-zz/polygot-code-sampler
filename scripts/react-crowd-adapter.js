/**
 * React Crowd Adapter - Complete WebSocket Handler
 * 
 * Drop this into your CodeSampler component to handle all crowd messages:
 * - nudge (delta changes)
 * - set (absolute values) 
 * - gov (governor cap override)
 * - kick (intensity burst)
 * - run (execute code)
 */

import { useEffect, useState } from 'react';

export function useCrowdControl({ 
  setHue, 
  setFxIntensity, 
  run, 
  code,
  useParticlesGovernor 
}) {
  const [ws, setWs] = useState(null);
  const [connected, setConnected] = useState(false);
  const [govCap, setGovCap] = useState(null); // null = auto, number 0..1 = forced

  // Enhanced governor with override support
  const { cap, fps } = useParticlesGovernor(govCap);

  useEffect(() => {
    const wsUrl = 'ws://localhost:8765';
    const websocket = new WebSocket(wsUrl);

    websocket.onopen = () => {
      console.log('🎭 Crowd Control connected');
      setConnected(true);
      setWs(websocket);
    };

    websocket.onclose = () => {
      console.log('🔌 Crowd Control disconnected');
      setConnected(false);
      setWs(null);
    };

    websocket.onmessage = (ev) => {
      try {
        const msg = JSON.parse(ev.data);

        // Delta nudges (existing behavior)
        if (msg.type === "nudge") {
          if (typeof msg.deltaIntensity === "number") {
            setFxIntensity(v => clamp(v + msg.deltaIntensity, 0, 1));
          }
          if (typeof msg.deltaHue === "number") {
            setHue(h => (h + msg.deltaHue + 360) % 360);
          }
        }

        // Absolute set (new scene presets)
        if (msg.type === "set") {
          if (Number.isFinite(msg.hue)) {
            setHue(((msg.hue % 360) + 360) % 360);
          }
          if (Number.isFinite(msg.intensity)) {
            setFxIntensity(clamp(msg.intensity, 0, 1));
          }
        }

        // Governor cap override (new FPS management)
        if (msg.type === "gov") {
          if (Number.isFinite(msg.cap)) {
            setGovCap(clamp(msg.cap, 0, 1));
            console.log(`🎛️ Governor cap set to ${(msg.cap * 100).toFixed(0)}%`);
          }
        }

        // Kick burst (existing)
        if (msg.type === "kick") {
          setFxIntensity(v => Math.min(1, v + 0.25));
          console.log('👟 Crowd kick!');
        }

        // Run code (existing)
        if (msg.type === "run") {
          if (run && code) {
            run(code);
            console.log('▶️ Crowd triggered code run');
          }
        }

      } catch (err) {
        console.warn('Invalid crowd message:', err);
      }
    };

    return () => {
      websocket.close();
    };
  }, [setHue, setFxIntensity, run, code]);

  return {
    connected,
    cap,
    fps,
    govCap,
    setGovCap
  };
}

// Helper function
function clamp(v, a, b) {
  return Math.max(a, Math.min(b, v));
}

/**
 * Usage in your component:
 * 
 * const { connected, cap, fps, govCap } = useCrowdControl({
 *   setHue,
 *   setFxIntensity, 
 *   run,
 *   code,
 *   useParticlesGovernor
 * });
 * 
 * // Display connection status
 * {connected ? '🎭' : '🔌'} Crowd Control
 * 
 * // Show FPS and cap info
 * FPS: {fps} | Cap: {cap} | Gov: {govCap ? `${(govCap*100).toFixed(0)}%` : 'auto'}
 */

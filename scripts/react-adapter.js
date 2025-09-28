/**
 * React Adapter for CodeSampler Live
 * Usage in your component:
 *   import { useSandboxAdapter, FlashOverlay } from "../scripts/react-adapter";
 *   const { bindResult } = useSandboxAdapter({ setHue, setFxIntensity });
 *   useEffect(() => bindResult(lastResult), [lastResult]);
 *   <FlashOverlay ref={flashRef} />
 */

import { useEffect, useRef } from "react";

export function useSandboxAdapter({ setHue, setFxIntensity }) {
  const flashRef = useRef(0);

  // fade loop for flash overlay
  useEffect(() => {
    let raf;
    const step = () => {
      if (flashRef.current > 0) {
        flashRef.current = Math.max(0, flashRef.current - 0.04);
      }
      raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, []);

  // bind sandbox result → visual params
  const bindResult = (out) => {
    if (!out || typeof out !== "object") return;
    const { fx, burst } = out;

    if (fx) {
      if (Number.isFinite(fx.hue)) setHue(((fx.hue % 360) + 360) % 360);
      if (Number.isFinite(fx.intensity)) {
        setFxIntensity((v) => clamp(fx.intensity, 0, 1));
      }
      if (Number.isFinite(fx.flash)) {
        flashRef.current = Math.max(flashRef.current, clamp(fx.flash, 0, 1));
      }
    }

    if (burst && Number.isInteger(burst.count)) {
      // mild "energy kick"; your particle governor keeps this safe
      setFxIntensity((v) => Math.min(1, v + Math.min(0.35, burst.count / 300)));
      flashRef.current = Math.max(flashRef.current, 0.4);
    }
  };

  return { bindResult, flashRef };
}

export const FlashOverlay = forwardRefWithName("FlashOverlay", function FlashOverlayImpl(_, ref) {
  // ref should be the flashRef returned by useSandboxAdapter
  const localRef = ref || useRef(0);
  // Inline component relying on a tiny animation tick from parent renders
  return (
    <div
      className="pointer-events-none absolute inset-0"
      style={{
        background: `rgba(255,255,255,${(localRef.current || 0) * 0.6})`,
        transition: "background 30ms linear",
        mixBlendMode: "screen",
      }}
    />
  );
});

function forwardRefWithName(name, comp) {
  const f = (props, ref) => comp(props, ref);
  Object.defineProperty(f, "name", { value: name });
  return (/** @type {any} */(React)).forwardRef(f);
}

function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

// ========================================
// USAGE EXAMPLE
// ========================================

/*
How to hook it up inside your component (you already have lastResult, setHue, setFxIntensity):

import { useSandboxAdapter, FlashOverlay } from "../scripts/react-adapter";

const { bindResult, flashRef } = useSandboxAdapter({ setHue, setFxIntensity });
useEffect(() => { bindResult(lastResult); }, [lastResult]);

// In JSX container (top layer)
<FlashOverlay ref={flashRef} />
*/

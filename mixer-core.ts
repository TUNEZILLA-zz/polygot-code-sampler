// mixer-core.ts - Core functionality for Code Live
// Interpolation, quantize, sidechain, solo logic

export type MixerState = {
  faders: Record<string, number>;
  macros: Record<string, number>;
  flags: Record<string, boolean>;
};

export type Keyframe = {
  t: number;
  state: MixerState;
};

export type Metric = {
  path: "rust.gen_ms" | "sql.rows" | "julia.loc" | "ts.workers";
  op: ">" | "<";
  value: number;
};

export type Action = {
  target: string; // e.g. "julia.level"
  delta: number;
};

export type Rule = {
  when: Metric;
  then: Action;
};

export type MidiMap = {
  cc: number;
  target: string; // e.g. "rust.level" | "macros.performance"
};

// === INTERPOLATION & EASING ===

export function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}

export function easeInOut(t: number): number {
  return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
}

export function easeLinear(t: number): number {
  return t;
}

export function easeExp(t: number): number {
  return Math.pow(t, 1.8);
}

export function easeS(t: number): number {
  return 0.5 * (1 - Math.cos(Math.PI * t));
}

export const ramps = {
  linear: easeLinear,
  exp: easeExp,
  s: easeS
};

export function interpState(a: Keyframe, b: Keyframe, tNow: number): MixerState {
  const t = easeInOut((tNow - a.t) / (b.t - a.t));

  const faders = Object.fromEntries(
    Object.keys(a.state.faders).map(k => [
      k,
      lerp(a.state.faders[k], b.state.faders[k], t)
    ])
  );

  const macros = Object.fromEntries(
    Object.keys(a.state.macros).map(k => [
      k,
      lerp(a.state.macros[k], b.state.macros[k], t)
    ])
  );

  // Flags: hold-then-switch near 0.5 to avoid flicker
  const flags = Object.fromEntries(
    Object.keys(a.state.flags).map(k => [
      k,
      (t < 0.5 ? a.state.flags[k] : b.state.flags[k])
    ])
  );

  return { faders, macros, flags };
}

// === QUANTIZATION ===

export function quantize(ts: number, stepMs: number = 100): number {
  return Math.round(ts / stepMs) * stepMs;
}

export function quantizeToGrid(value: number, gridSize: number = 0.25): number {
  return Math.round(value / gridSize) * gridSize;
}

// === SOLO LOGIC ===

export function applySoloLogic(
  tracks: Record<string, number>,
  soloed: Record<string, boolean>
): Record<string, boolean> {
  const hasAnySolo = Object.values(soloed).some(s => s);

  if (!hasAnySolo) {
    // No solo active, all tracks audible
    return Object.fromEntries(Object.keys(tracks).map(k => [k, true]));
  }

  // Solo active, only soloed tracks audible
  return Object.fromEntries(
    Object.keys(tracks).map(k => [k, soloed[k] || false])
  );
}

// === SIDECHAIN RULES ===

export function applyRule(
  rule: Rule,
  metrics: Record<string, any>,
  state: MixerState
): MixerState {
  const left = rule.when.path.split('.').reduce((o, k) => o?.[k], metrics);
  const ok = rule.when.op === ">"
    ? left > rule.when.value
    : left < rule.when.value;

  if (ok) {
    const [track, prop] = rule.then.target.split('.');
    const currentValue = state.faders[track] || 0;
    const newValue = Math.max(0, Math.min(1, currentValue + rule.then.delta));

    return {
      ...state,
      faders: {
        ...state.faders,
        [track]: newValue
      }
    };
  }

  return state;
}

export function applyRules(
  rules: Rule[],
  metrics: Record<string, any>,
  state: MixerState
): MixerState {
  return rules.reduce((acc, rule) => applyRule(rule, metrics, acc), state);
}

// === MIDI MAPPING ===

export function applyMidiMap(
  midiMap: MidiMap[],
  cc: number,
  value: number, // 0-127
  state: MixerState
): MixerState {
  const mapping = midiMap.find(m => m.cc === cc);
  if (!mapping) return state;

  const normalizedValue = value / 127; // Convert to 0-1

  if (mapping.target.startsWith('macros.')) {
    const macro = mapping.target.split('.')[1];
    return {
      ...state,
      macros: {
        ...state.macros,
        [macro]: normalizedValue
      }
    };
  } else {
    const [track, prop] = mapping.target.split('.');
    return {
      ...state,
      faders: {
        ...state.faders,
        [track]: normalizedValue
      }
    };
  }
}

// === PRESET MANAGEMENT ===

export type Preset = {
  version: string;
  name: string;
  state: MixerState;
  notes?: string;
};

export function exportPreset(name: string, state: MixerState, notes?: string): Preset {
  return {
    version: "1.0",
    name,
    state,
    notes
  };
}

export function importPreset(preset: Preset): MixerState {
  if (preset.version !== "1.0") {
    throw new Error(`Unsupported preset version: ${preset.version}`);
  }
  return preset.state;
}

// === PROJECT MANAGEMENT ===

export type Project = {
  project_version: string;
  python_source: string;
  clips: MixerState[];
  keyframes: Keyframe[];
  rules: Rule[];
  midi_map: MidiMap[];
  history: MixerState[];
};

export function createProject(pythonSource: string): Project {
  return {
    project_version: "1.0",
    python_source: pythonSource,
    clips: [],
    keyframes: [],
    rules: [],
    midi_map: [],
    history: []
  };
}

export function addToHistory(project: Project, state: MixerState): Project {
  return {
    ...project,
    history: [...project.history.slice(-9), state] // Keep last 10 states
  };
}

export function undo(project: Project): Project | null {
  if (project.history.length <= 1) return null;

  return {
    ...project,
    history: project.history.slice(0, -1)
  };
}

// === GLITCH MODE ===

export function applyGlitch(
  state: MixerState,
  intensity: number = 0.5,
  seed?: number
): MixerState {
  const rng = seed ? createSeededRNG(seed) : Math.random;

  const glitchedFaders = Object.fromEntries(
    Object.entries(state.faders).map(([k, v]) => [
      k,
      Math.max(0, Math.min(1, v + (rng() - 0.5) * intensity))
    ])
  );

  const glitchedMacros = Object.fromEntries(
    Object.entries(state.macros).map(([k, v]) => [
      k,
      Math.max(0, Math.min(1, v + (rng() - 0.5) * intensity))
    ])
  );

  return {
    faders: glitchedFaders,
    macros: glitchedMacros,
    flags: state.flags
  };
}

function createSeededRNG(seed: number) {
  let current = seed;
  return () => {
    current = (current * 9301 + 49297) % 233280;
    return current / 233280;
  };
}

// === PERFORMANCE OVERLAYS ===

export type PerformanceStats = {
  gen_ms: number;
  loc: number;
  fallbacks: string[];
  warnings: string[];
};

export function calculatePerformanceOverlay(
  backend: string,
  stats: PerformanceStats
): string[] {
  const overlays: string[] = [];

  if (stats.gen_ms > 25) {
    overlays.push(`⚠️ Slow generation: ${stats.gen_ms}ms`);
  }

  if (stats.fallbacks.length > 0) {
    overlays.push(`🔄 Fallbacks: ${stats.fallbacks.join(', ')}`);
  }

  if (stats.warnings.length > 0) {
    overlays.push(`⚠️ Warnings: ${stats.warnings.join(', ')}`);
  }

  return overlays;
}

// === A/B COMPARE ===

export type ABCompare = {
  a: MixerState;
  b: MixerState;
  active: 'a' | 'b';
};

export function createABCompare(state: MixerState): ABCompare {
  return {
    a: state,
    b: { ...state },
    active: 'a'
  };
}

export function toggleAB(compare: ABCompare): ABCompare {
  return {
    ...compare,
    active: compare.active === 'a' ? 'b' : 'a'
  };
}

export function getActiveState(compare: ABCompare): MixerState {
  return compare.active === 'a' ? compare.a : compare.b;
}

// === UTILITIES ===

export function clamp(value: number, min: number = 0, max: number = 1): number {
  return Math.max(min, Math.min(max, value));
}

export function roundToPrecision(value: number, precision: number = 2): number {
  return Math.round(value * Math.pow(10, precision)) / Math.pow(10, precision);
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

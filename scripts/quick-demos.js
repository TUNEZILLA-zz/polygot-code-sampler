/**
 * CodeSampler Live - Ready-to-Run Visual Demos
 * Copy any demo into your CodeSampler Live sandbox and hit Run!
 * Each returns structured data that steers your visual FX in real-time.
 */

// Each demo is a JS *snippet* meant to run inside the sandbox.
// OUT PROTOCOL:
// return { fx:{hue:intensity:flash}, burst:{count}|null, ui:{note}? }

export const DEMOS = {
  "Beat-Reactive Fireworks": `
const { beat, bpm, bands, t } = ENV;
const hue = (t * 90) % 360;
const intensity = Math.min(1, bands.bass * 2);
const flash = beat ? 0.8 : 0;
return {
  fx: { hue, intensity, flash },
  burst: beat ? { count: 60 + Math.floor(bands.bass * 120) } : null,
  ui: { note: \`Beat pop @ \${Math.round(bpm)} BPM\` }
};`,

  "Bass Waves": `
const { bands, t } = ENV;
const hue = ((bands.bass * 360) + t*20) % 360;
const intensity = Math.min(1, 0.25 + bands.low * 1.2);
return { fx: { hue, intensity, flash: 0 }, burst: null, ui: { note: "Bass waves" } };`,

  "Lightning Flicker": `
const { beat, bands } = ENV;
const flash = (beat && bands.bass > 0.25) ? 1 : 0;
return { fx: { hue: 220, intensity: 0.5, flash }, burst: null };`,

  "BPM Pulse": `
const { bpm, t } = ENV;
const ph = Math.sin(t * (bpm/60) * Math.PI * 2);
const intensity = 0.5 + 0.45 * (ph * 0.5 + 0.5);
return { fx: { hue: (t*40)%360, intensity, flash: 0 }, burst: null };`,

  "Rainbow Orbit": `
const { t } = ENV;
return { fx: { hue: (t*60)%360, intensity: 0.55, flash: 0 }, burst: null };`,

  "Mid-Band Geometry Cue": `
const { bands } = ENV;
const intensity = Math.min(1, 0.3 + bands.mid);
const hue = (60 + bands.mid * 180) % 360;
return { fx: { hue, intensity, flash: 0 }, burst: null, ui: { note: "Mid band drive" } };`,

  "Hi-Hat Sparkles": `
const { bands, beat } = ENV;
const sparkle = bands.high > 0.15 && !beat;
return { fx: { hue: 300, intensity: 0.45 + (sparkle?0.2:0), flash: sparkle?0.35:0 }, burst: sparkle?{count:8}:null };`,

  "Downbeat Bloom": `
const { beat, bpm } = ENV;
const intensity = beat ? 0.95 : 0.5;
const hue = beat ? 120 : 180;
return { fx: { hue, intensity, flash: beat?0.6:0 }, burst: beat?{count:40}:null, ui: { note: \`Downbeat bloom \${Math.round(bpm)}bpm\` } };`,

  "Spectrum Glide": `
const { bands, t } = ENV;
const weighted = (bands.bass*0.5 + bands.low*0.3 + bands.mid*0.15 + bands.high*0.05);
const hue = (t*30 + weighted*360) % 360;
const intensity = clamp(0.35 + weighted*0.9, 0, 1);
return { fx: { hue, intensity, flash: 0 }, burst: null };
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}`,

  "Crowd-Kicked Surges": `
const { beat, bands, t } = ENV;
const surge = (Math.floor(t*0.5)%2===0);
const intensity = 0.5 + (surge?0.3:0) + Math.min(0.2, bands.bass);
return { fx: { hue: (t*50)%360, intensity, flash: surge?0.25:0 }, burst: null };`,
};

// Optional: print quick instructions in terminal if run via node
if (import.meta && import.meta.main) {
  console.log("Demos loaded. Open CodeSampler Live, copy one snippet, paste, Run.");
}

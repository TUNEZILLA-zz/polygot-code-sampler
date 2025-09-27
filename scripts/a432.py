#!/usr/bin/env python3
"""
🎵 Code Live - A=432 Hz Fantasy Mode
====================================

A playful easter egg inspired by the 432 Hz lore - use for atmosphere, not as guaranteed medicinal tuning!
This mode is purely for creative fun and ambient effects.
"""

import math
import struct
import sys
import wave
from pathlib import Path
from typing import Optional, Tuple


def cents_to_ratio(cents: float) -> float:
    """Convert cents to frequency ratio"""
    return math.pow(2, cents / 1200)


def make_a432_wav(
    path: str = "a432.wav",
    seconds: float = 2.5,
    sample_rate: int = 48000,
    gain: float = 0.05,
    chorus: bool = True,
    detune_hz: float = 1.2,
) -> str:
    """Generate a gentle A=432 Hz tone with optional chorus"""
    frames = []

    for n in range(int(seconds * sample_rate)):
        t = n / sample_rate

        # Base 432 Hz sine wave
        y = math.sin(2 * math.pi * 432 * t)

        # Optional gentle chorus (detuned copy)
        if chorus:
            y += 0.6 * math.sin(2 * math.pi * (432 + detune_hz) * t)

        # ADSR envelope (avoid clicks, keep quiet)
        a, d, s, r = 0.05, 0.3, 0.6, 0.4
        if t < a:
            env = t / a
        elif t < a + d:
            env = 1 - (1 - s) * ((t - a) / d)
        elif t > seconds - r:
            env = max(0.0, (seconds - t) / r)
        else:
            env = s

        # Apply envelope and gain
        z = max(-1.0, min(1.0, y * env * gain))
        frames.append(struct.pack("<h", int(z * 32767)))

    # Write WAV file
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(b"".join(frames))

    return path


def generate_432_theme_css() -> str:
    """Generate CSS for 432 Hz fantasy theme"""
    return """
/* 🎵 A=432 Hz Fantasy Mode Theme */
.theme-a432 {
    --fx-primary: #4b6cff;   /* indigo */
    --fx-accent: #2dd4bf;    /* teal */
    --fx-secondary: #8b5cf6; /* purple */
    --fx-background: #0f172a; /* dark slate */
    --fx-text: #e2e8f0;      /* light gray */
    
    /* Breathing animation derived from 432 Hz */
    --breath-tempo: 108;     /* 432/4 = 108 BPM */
    --breath-duration: 2.22s; /* 60/108 * 4 = 2.22s */
}

.theme-a432 .fx-particle {
    animation: a432-breathe var(--breath-duration) ease-in-out infinite;
}

.theme-a432 .fx-background {
    background: linear-gradient(45deg, 
        var(--fx-primary) 0%, 
        var(--fx-accent) 50%, 
        var(--fx-secondary) 100%);
    opacity: 0.1;
}

@keyframes a432-breathe {
    0%, 100% { transform: scale(1); opacity: 0.8; }
    50% { transform: scale(1.05); opacity: 1.0; }
}

/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
    .theme-a432 .fx-particle {
        animation: none;
    }
}
"""


def generate_432_webaudio_js() -> str:
    """Generate JavaScript for 432 Hz WebAudio easter egg"""
    return (
        """
// 🎵 A=432 Hz Fantasy Mode - WebAudio Easter Egg
(function() {
    'use strict';
    
    // Check for 432 Hz mode activation
    const params = new URLSearchParams(location.search);
    const is432Mode = params.get('a432') === '1' || params.get('pitch') === '432';
    
    if (!is432Mode) return;
    
    // Apply 432 Hz theme
    function apply432Theme() {
        const style = document.createElement('style');
        style.textContent = `"""
        + generate_432_theme_css().replace("`", "\\`")
        + """`;
        document.head.appendChild(style);
        document.body.classList.add('theme-a432');
        
        // Add subtle visual indicator
        const indicator = document.createElement('div');
        indicator.innerHTML = '🎵 A=432 Hz Fantasy Mode';
        indicator.style.cssText = `
            position: fixed; top: 10px; right: 10px; z-index: 1000;
            background: rgba(75, 108, 255, 0.9); color: white;
            padding: 8px 12px; border-radius: 20px; font-size: 12px;
            font-family: monospace; pointer-events: none;
        `;
        document.body.appendChild(indicator);
    }
    
    // Generate 432 Hz tone with WebAudio
    function play432Hz(options = {}) {
        const { seconds = 3, gain = 0.08, chorus = false } = options;
        
        try {
            const AC = window.AudioContext || window.webkitAudioContext;
            const ctx = new AC();
            const now = ctx.currentTime;
            
            // Master gain with soft ADSR
            const master = ctx.createGain();
            master.gain.value = 0;
            master.connect(ctx.destination);
            
            const osc = ctx.createOscillator();
            osc.type = 'sine';
            osc.frequency.value = 432; // A4 = 432 Hz
            osc.connect(master);
            
            // Optional gentle chorus
            let lfoNode;
            if (chorus) {
                const lfo = ctx.createOscillator();
                const lfoGain = ctx.createGain();
                lfo.frequency.value = 0.2;       // slow wow
                lfoGain.gain.value = 1.5;        // ~±1.5 Hz
                lfo.connect(lfoGain);
                lfoGain.connect(osc.frequency);
                lfo.start();
                lfoNode = lfo;
            }
            
            // ADSR envelope (avoid clicks, keep quiet by default)
            const a = 0.08, d = 0.3, s = 0.5, r = 0.8;
            master.gain.linearRampToValueAtTime(gain, now + a);
            master.gain.linearRampToValueAtTime(gain * s, now + a + d);
            master.gain.setTargetAtTime(0, now + Math.max(0.2, seconds - r), 0.25);
            
            osc.start();
            osc.stop(now + seconds + 0.2);
            
            osc.onended = () => { 
                lfoNode?.stop?.(); 
                ctx.close(); 
            };
            
        } catch (error) {
            console.log('432 Hz audio not available:', error);
        }
    }
    
    // Microtuning based on metrics
    function getTunedFrequency(queueDepth = 50) {
        const cents = (Math.min(100, queueDepth) - 50) * (40 / 50); // ±40 cents span
        return 432 * Math.pow(2, cents / 1200);
    }
    
    // Initialize 432 Hz mode
    function init432Mode() {
        apply432Theme();
        
        // Respect reduced motion & user gesture policies
        if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            // Start on first user gesture to satisfy autoplay policies
            const once = () => { 
                play432Hz({ chorus: true }); 
                window.removeEventListener('click', once); 
            };
            window.addEventListener('click', once, { once: true });
        }
        
        // Log activation for telemetry
        if (window.gtag) {
            window.gtag('event', 'easter_egg_activated', {
                'event_category': 'a432',
                'event_label': 'fantasy_mode'
            });
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init432Mode);
    } else {
        init432Mode();
    }
})();
"""
    )


def generate_432_cli() -> str:
    """Generate CLI command for 432 Hz mode"""
    return """
# 🎵 A=432 Hz Fantasy Mode CLI Usage

# Enable 432 Hz mode with audio
python pcs_step3_ts.py --code "for i in range(10): process(i)" --egg a432

# Enable 432 Hz mode visuals only (no audio)
python pcs_step3_ts.py --code "for i in range(10): process(i)" --egg a432:mute

# Generate 432 Hz WAV file
python scripts/a432.py --output a432_fantasy.wav --seconds 5 --chorus

# Web interface with 432 Hz mode
# Add ?a432=1 or ?pitch=432 to URL
"""


def main():
    """Main CLI entry point for 432 Hz fantasy mode"""
    import argparse

    parser = argparse.ArgumentParser(
        description="🎵 A=432 Hz Fantasy Mode - Playful easter egg for creative coding",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/a432.py                    # Generate default 432 Hz tone
  python scripts/a432.py --output my.wav   # Custom output file
  python scripts/a432.py --seconds 5       # Longer duration
  python scripts/a432.py --no-chorus       # Pure sine wave
  python scripts/a432.py --gain 0.1        # Louder (be careful!)
        """,
    )

    parser.add_argument(
        "--output", "-o", default="a432.wav", help="Output WAV file path"
    )
    parser.add_argument(
        "--seconds", "-s", type=float, default=2.5, help="Duration in seconds"
    )
    parser.add_argument(
        "--gain", "-g", type=float, default=0.05, help="Audio gain (0.0-1.0)"
    )
    parser.add_argument(
        "--no-chorus", action="store_true", help="Disable chorus effect"
    )
    parser.add_argument(
        "--detune", "-d", type=float, default=1.2, help="Chorus detune in Hz"
    )
    parser.add_argument(
        "--sample-rate", "-r", type=int, default=48000, help="Sample rate"
    )
    parser.add_argument("--theme", action="store_true", help="Generate CSS theme")
    parser.add_argument(
        "--webaudio", action="store_true", help="Generate WebAudio JavaScript"
    )
    parser.add_argument(
        "--cli-help", action="store_true", help="Show CLI integration help"
    )

    args = parser.parse_args()

    if args.theme:
        print("🎵 A=432 Hz Fantasy Mode CSS Theme:")
        print("=" * 50)
        print(generate_432_theme_css())
        return

    if args.webaudio:
        print("🎵 A=432 Hz Fantasy Mode WebAudio JavaScript:")
        print("=" * 50)
        print(generate_432_webaudio_js())
        return

    if args.cli_help:
        print("🎵 A=432 Hz Fantasy Mode CLI Integration:")
        print("=" * 50)
        print(generate_432_cli())
        return

    # Generate 432 Hz WAV file
    print("🎵 Generating A=432 Hz Fantasy Mode Audio...")
    print(f"   Duration: {args.seconds}s")
    print(f"   Gain: {args.gain}")
    print(f"   Chorus: {'Yes' if not args.no_chorus else 'No'}")
    print(f"   Sample Rate: {args.sample_rate} Hz")
    print()

    try:
        output_path = make_a432_wav(
            path=args.output,
            seconds=args.seconds,
            sample_rate=args.sample_rate,
            gain=args.gain,
            chorus=not args.no_chorus,
            detune_hz=args.detune,
        )

        print(f"✅ Generated: {output_path}")
        print()
        print("🎵 A=432 Hz Fantasy Mode - Playful easter egg for creative coding!")
        print(
            "   This is inspired by 432 Hz lore - use for atmosphere, not as guaranteed medicinal tuning."
        )
        print("   Add ?a432=1 to your web interface URL to activate the easter egg!")

    except Exception as e:
        print(f"❌ Error generating 432 Hz audio: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

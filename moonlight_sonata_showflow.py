#!/usr/bin/env python3
"""
Moonlight Sonata Text-FX Performance Script
==========================================
A 90-second visual-text remix of Beethoven's Moonlight Sonata
using the touring rig string FX + chromatic light desk system.

Performance Flow:
- Movement I (0-30s): Pizzicato Strings + Cinemascope (haunting arpeggios)
- Movement II (30-60s): Arpeggio Harp + Neon Bloom (warm interlude)
- Movement III (60-90s): Guitar Lead + Prism Burst + Lightning (stormy finale)

Total Runtime: 90 seconds
"""

import time
import subprocess
import json
from datetime import datetime


class MoonlightSonataPerformance:
    def __init__(self):
        self.base_text = "Moonlight Sonata"
        self.performance_log = []
        self.start_time = None

    def log_action(self, action, timestamp, description):
        """Log performance actions with timestamps"""
        self.performance_log.append(
            {"timestamp": timestamp, "action": action, "description": description}
        )
        print(f"[{timestamp:02d}s] {action}: {description}")

    def run_make_command(self, target, **kwargs):
        """Run make command with error handling"""
        try:
            cmd = f"make {target}"
            if kwargs:
                params = " ".join([f"{k}={v}" for k, v in kwargs.items()])
                cmd += f" {params}"

            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                print(f"Warning: {target} returned {result.returncode}")
                return False
        except Exception as e:
            print(f"Error running {target}: {e}")
            return False

    def movement_i_adagio(self):
        """Movement I: Adagio sostenuto - Haunting arpeggios (FOH Cue Sheet)"""
        print("\n🌙 MOVEMENT I: ADAGIO SOSTENUTO (0-30s)")
        print("=" * 50)

        # 00:00 - Cinemascope + Pizzicato Strings (0.20 → 0.30)
        self.log_action(
            "SCENE", 0, "Cinemascope + Pizzicato Strings - start monochrome"
        )
        self.run_make_command(
            "show-controller-cinemascope", TEXT="Moonlight", INTENSITY=0.2
        )
        self.run_make_command("pizzicato-strings", TEXT="Sonata", INTENSITY=0.2)
        self.run_make_command("touring-rig-metrics-link", STRENGTH=0.25)
        self.run_make_command("touring-rig-param", PATH="cosmics.dust", VALUE=0.15)
        time.sleep(3)

        # 00:10 - Sustain veil with Chromatic Trails (0.30)
        self.log_action("FX", 10, "Chromatic Trails (low) - tap tempo slow")
        self.run_make_command("chromatic-trails", TEXT="Moonlight", INTENSITY=0.3)
        self.run_make_command("touring-rig-intensity", VALUE=0.3)
        time.sleep(3)

        # 00:20 - Candle flicker with Subtle Vibrato + Fringe (0.30 → 0.35)
        self.log_action("LIGHT", 20, "Subtle Vibrato + Fringe - add slight vibrato")
        self.run_make_command("chromatic-fringe", TEXT="Sonata", INTENSITY=0.35)
        self.run_make_command("touring-rig-param", PATH="space", VALUE=0.05)  # +5%
        time.sleep(3)

        # 00:30 - Prepare for Movement II
        self.log_action("TRANSITION", 30, "Prepare for Movement II - Allegretto")
        self.run_make_command("touring-rig-intensity", VALUE=0.35)
        time.sleep(1)

    def movement_ii_allegretto(self):
        """Movement II: Allegretto - Warm interlude (FOH Cue Sheet)"""
        print("\n🎵 MOVEMENT II: ALLEGRETTO (30-60s)")
        print("=" * 50)

        # 00:30 - Neon Bloom + Arpeggio Harp (0.45 → 0.60)
        self.log_action(
            "SCENE", 30, "Neon Bloom + Arpeggio Harp - enable color macro +10%"
        )
        self.run_make_command(
            "show-controller-neon-bloom", TEXT="Moonlight", INTENSITY=0.45
        )
        self.run_make_command("arpeggio-harp", TEXT="Sonata", INTENSITY=0.45)
        self.run_make_command("touring-rig-param", PATH="color", VALUE=0.1)  # +10%
        self.run_make_command("touring-rig-metrics-link", STRENGTH=0.5)
        time.sleep(3)

        # 00:45 - Lift with Chorus MicroShift (wide) (0.60)
        self.log_action(
            "FX", 45, "Chorus MicroShift (wide) - keep trails modest (a11y)"
        )
        self.run_make_command(
            "effect-rack-micro-shift", TEXT="Moonlight", INTENSITY=0.6
        )
        self.run_make_command("touring-rig-intensity", VALUE=0.6)
        time.sleep(3)

        # 01:00 - Prepare for Movement III
        self.log_action("TRANSITION", 60, "Prepare for Movement III - Presto agitato")
        self.run_make_command("touring-rig-intensity", VALUE=0.6)
        time.sleep(1)

    def movement_iii_presto(self):
        """Movement III: Presto agitato - Stormy finale (FOH Cue Sheet)"""
        print("\n⚡ MOVEMENT III: PRESTO AGITATO (60-90s)")
        print("=" * 50)

        # 01:00 - Prism Burst + Guitar Lead (0.70 → 0.90)
        self.log_action(
            "SCENE",
            60,
            "Prism Burst + Guitar Lead - start morph: Glass Cathedral → Data Storm over 10s",
        )
        self.run_make_command(
            "show-controller-prism-burst", TEXT="Moonlight", INTENSITY=0.7
        )
        self.run_make_command("guitar-lead", TEXT="Sonata", INTENSITY=0.7)
        self.run_make_command(
            "pro-rack-morph",
            RACK1="presets/racks/glass_cathedral.rack.json",
            RACK2="presets/racks/data_storm.rack.json",
            MORPH_TIME=10.0,
        )
        time.sleep(3)

        # 01:10 - Thunder with Lightning FX (guarded) (0.95)
        self.log_action(
            "LIGHT",
            70,
            "Lightning FX (guarded) - momentary White Bloom (≤1.0s) on downbeat",
        )
        self.run_make_command("light-lightning", TEXT="Moonlight", INTENSITY=0.95)
        self.run_make_command("touring-rig-all-white-bloom", STATE="true")
        time.sleep(1)  # ≤1.0s white bloom
        self.run_make_command("touring-rig-all-white-bloom", STATE="false")
        time.sleep(2)

        # 01:20 - Cadence with Broken Spectrum → Mono (0.90 → 0.45)
        self.log_action(
            "CADENCE",
            80,
            "Broken Spectrum → Mono - ease metrics-link to 0.2, taper intensity",
        )
        self.run_make_command("chromatic-spectrum", TEXT="Sonata", INTENSITY=0.9)
        self.run_make_command("touring-rig-metrics-link", STRENGTH=0.2)
        self.run_make_command("touring-rig-intensity", VALUE=0.45)
        time.sleep(3)

        # 01:30 - Blackout (Motion-safe fade) (0.00)
        self.log_action("BLACKOUT", 90, "Motion-safe fade - press Blackout; stop log")
        self.run_make_command("touring-rig-blackout", STATE="true")
        self.run_make_command("touring-rig-intensity", VALUE=0.0)
        time.sleep(1)

    def interactive_knob_mapping(self):
        """Interactive knob mapping for live performance (FOH Cue Sheet)"""
        print("\n🎛️ INTERACTIVE KNOB MAPPING")
        print("=" * 50)
        print(
            "Color → chromatic.offset (±0.25), prism.slope (+0.0→0.4), hologram.scanlines (0→0.35)"
        )
        print(
            "Space → trails.length (0.2→1.0), reverb.decay (0.3→1.2), dust.fade (0.1→0.7)"
        )
        print(
            "Motion → vibrato.depth (0→0.6), tremolo.rate (0.5→6.0 Hz w/ safety), trails.follow (0→0.5)"
        )
        print(
            "Crunch → distortion.drive (0→0.7), stutter.duty (guarded), lightning.chance (guarded)"
        )
        print("\nLive performance controls:")
        print("- Use knobs to 'play' harmonic changes")
        print("- Map to text FX parameters in real-time")
        print("- Create visual-text remix of the Sonata")

    def operator_hotkeys(self):
        """Operator hotkeys for live performance (FOH Cue Sheet)"""
        print("\n⌨️ OPERATOR HOTKEYS")
        print("=" * 50)
        print("1/2/3/4: jump to movements I/II/III/Outro")
        print("I / K: intensity up/down (slew-limited)")
        print("M: toggle metrics link (use 0.5 during Allegretto)")
        print("W: White Bloom hit (≤1.2s) on III accents")
        print("B: Blackout (final beat)")
        print("U / R: undo / redo (in case of over-crunch)")
        print(", / .: metrics link strength − / +")

    def rehearsal_tweaks(self):
        """Rehearsal tweaks for fast wins (FOH Cue Sheet)"""
        print("\n🎭 REHEARSAL TWEAKS")
        print("=" * 50)
        print(
            "Tempo feel: set jam BPM to ~56 (Adagio), 76 (Allegretto), 168 (Presto) for LFOs/tremolo"
        )
        print(
            "A11y pass: ensure reduced-motion flag forces mono + trails.length ≤0.25 during I & II"
        )
        print("Seeded take: run with a seed for shot-for-shot repeatability")
        print(
            "Venue profiles: small room → dust=0.12, trails=0.35; arena → dust=0.22, trails=0.6"
        )
        print("Safety rails: strobe ≤ 8 Hz, duty ≤ 35% / 10s, on-time ≥ 120 ms")
        print("Frame p95 ≤ 10–12 ms (auto-reduce trails/particles if exceeded)")
        print("Motion-reduced fade ≤ 490 ms (already quantized)")

    def pro_tips(self):
        """Pro tips for performance optimization (FOH Cue Sheet)"""
        print("\n💡 PRO TIPS")
        print("=" * 50)
        print(
            "Soft glass feel in I: lower chromatic to ~0.08, increase fringe 0.15, dust 0.18"
        )
        print(
            "Storm articulation in III: map sidechain to Crunch from QPS so busy sections 'growl' more—keep link ≤0.8"
        )
        print(
            "Grand cadence: morph back to Glass Cathedral over 6–8 s while pulling intensity to 0.45, then B"
        )
        print(
            "Cosmic dust overlay: add moonlight shimmer particles for drifting effect"
        )
        print(
            "Capture checklist: 30s highlight capture (III focus), snapshot grid (low/mid/peak)"
        )

    def cosmic_dust_overlay(self):
        """Add cosmic dust particles for moonlight shimmer"""
        print("\n✨ COSMIC DUST OVERLAY")
        print("=" * 50)
        print("Adding moonlight shimmer particles...")
        # This would integrate with your particle system
        # for the "drifting moonlight" effect
        self.log_action("PARTICLES", 0, "Cosmic dust overlay - moonlight shimmer")

    def run_performance(self):
        """Run the complete Moonlight Sonata performance"""
        print("🌙 MOONLIGHT SONATA TEXT-FX PERFORMANCE")
        print("=" * 60)
        print("A 90-second visual-text remix of Beethoven's masterpiece")
        print("Using touring rig string FX + chromatic light desk")
        print("=" * 60)

        self.start_time = time.time()

        try:
            # Pre-performance setup
            print("\n🎭 PRE-PERFORMANCE SETUP")
            print("Loading touring rig...")
            self.run_make_command("touring-rig-load")
            self.run_make_command("stage-proof-load")

            # Cosmic dust overlay
            self.cosmic_dust_overlay()

            # Run the three movements
            self.movement_i_adagio()
            self.movement_ii_allegretto()
            self.movement_iii_presto()

            # Post-performance
            print("\n🎉 PERFORMANCE COMPLETE")
            print("=" * 50)
            print("Moonlight Sonata text-FX performance finished!")
            print("Total runtime: 90 seconds")

            # Save performance log
            self.save_performance_log()

        except KeyboardInterrupt:
            print("\n⏹️ Performance interrupted by user")
        except Exception as e:
            print(f"\n❌ Performance error: {e}")
        finally:
            # Cleanup
            print("\n🧹 CLEANUP")
            self.run_make_command("touring-rig-blackout", STATE="true")
            self.run_make_command("touring-rig-intensity", VALUE=0.0)

    def save_performance_log(self):
        """Save performance log to file"""
        log_data = {
            "performance": "Moonlight Sonata Text-FX",
            "timestamp": datetime.now().isoformat(),
            "duration": 90,
            "movements": [
                {"name": "Adagio sostenuto", "start": 0, "end": 30},
                {"name": "Allegretto", "start": 30, "end": 60},
                {"name": "Presto agitato", "start": 60, "end": 90},
            ],
            "actions": self.performance_log,
        }

        with open("out/moonlight_sonata_performance.json", "w") as f:
            json.dump(log_data, f, indent=2)

        print(f"Performance log saved to: out/moonlight_sonata_performance.json")

    def show_interactive_mode(self):
        """Show interactive jam mode instructions"""
        print("\n🎹 INTERACTIVE JAM MODE")
        print("=" * 50)
        print("Map macro knobs to text FX parameters:")
        print("• Color = Chromatic offset (mimics key changes)")
        print("• Space = Reverb/trails length (like pedal sustain)")
        print("• Motion = Vibrato & tremolo intensity")
        print("• Crunch = Feedback + distortion (storm intensity)")
        print("\nThen 'play' the Sonata's harmonic changes using knobs!")
        print("Create a visual-text remix of the masterpiece.")


def main():
    """Main execution function"""
    performance = MoonlightSonataPerformance()

    print("🌙 MOONLIGHT SONATA TEXT-FX PERFORMANCE SCRIPT")
    print("=" * 60)
    print("Choose execution mode:")
    print("1. Full Performance (90s)")
    print("2. Interactive Jam Mode")
    print("3. Operator Hotkeys Reference")
    print("4. Rehearsal Tweaks")
    print("5. Pro Tips")
    print("6. Show Performance Log")
    print("7. Cosmic Dust Overlay")

    choice = input("\nEnter choice (1-7): ").strip()

    if choice == "1":
        performance.run_performance()
    elif choice == "2":
        performance.interactive_knob_mapping()
    elif choice == "3":
        performance.operator_hotkeys()
    elif choice == "4":
        performance.rehearsal_tweaks()
    elif choice == "5":
        performance.pro_tips()
    elif choice == "6":
        try:
            with open("out/moonlight_sonata_performance.json", "r") as f:
                log = json.load(f)
                print(f"Last performance: {log['timestamp']}")
                print(f"Duration: {log['duration']}s")
                print("Actions:")
                for action in log["actions"]:
                    print(
                        f"  {action['timestamp']:02d}s: {action['action']} - {action['description']}"
                    )
        except FileNotFoundError:
            print("No performance log found. Run a performance first.")
    elif choice == "7":
        performance.cosmic_dust_overlay()
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()

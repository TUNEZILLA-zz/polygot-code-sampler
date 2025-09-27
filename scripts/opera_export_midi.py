#!/usr/bin/env python3
"""
🎭 Code Opera - MIDI Export
==========================

Export Code Opera performance to MIDI format.
One track per voice for DAW integration.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any

try:
    from mido import MidiFile, MidiTrack, Message, bpm2tempo

    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False
    print("⚠️  mido not available. Install with: pip install mido")


def create_voice_notes(
    voice_name: str, voice_config: Dict[str, Any], act: int = 1
) -> List[Dict[str, Any]]:
    """Create note data for a voice based on its configuration"""
    notes = []

    # Map harmony notes to MIDI note numbers
    note_map = {"C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71}

    # Get base note from harmony
    base_note = note_map.get(voice_config.get("harmony_note", "C"), 60)

    # Add octave based on voice type
    octave_offset = {
        "rust": -12,  # Bass
        "go": -12,  # Bass
        "csharp": -12,  # Bass
        "sql": -12,  # Bass
        "python": 0,  # Tenor
        "typescript": 0,  # Alto
        "julia": 12,  # Soprano
    }

    base_note += octave_offset.get(voice_name, 0)

    # Generate notes based on texture
    texture = voice_config.get("texture", "sparse")
    tempo = voice_config.get("tempo", 120)

    if texture == "dense":
        # Dense texture - many notes
        for i in range(16):
            notes.append(
                {"note": base_note + (i % 12), "start": i * 0.5, "dur": 0.4, "vel": 80}
            )
    elif texture == "sparse":
        # Sparse texture - few notes
        for i in range(4):
            notes.append({"note": base_note, "start": i * 2.0, "dur": 1.5, "vel": 60})
    elif texture == "smooth":
        # Smooth texture - legato notes
        for i in range(8):
            notes.append(
                {"note": base_note + (i % 7), "start": i * 1.0, "dur": 0.8, "vel": 70}
            )
    elif texture == "grainy":
        # Grainy texture - staccato notes
        for i in range(12):
            notes.append(
                {"note": base_note + (i % 12), "start": i * 0.25, "dur": 0.2, "vel": 90}
            )
    elif texture == "polyphonic":
        # Polyphonic texture - multiple voices
        for i in range(6):
            notes.append(
                {"note": base_note + (i % 7), "start": i * 0.75, "dur": 0.6, "vel": 75}
            )
            notes.append(
                {
                    "note": base_note + 7 + (i % 7),
                    "start": i * 0.75 + 0.3,
                    "dur": 0.6,
                    "vel": 75,
                }
            )
    elif texture == "minimal":
        # Minimal texture - very few notes
        for i in range(2):
            notes.append({"note": base_note, "start": i * 4.0, "dur": 3.0, "vel": 50})
    elif texture == "maximal":
        # Maximal texture - complex patterns
        for i in range(20):
            notes.append(
                {"note": base_note + (i % 12), "start": i * 0.2, "dur": 0.15, "vel": 85}
            )
    elif texture == "fractal":
        # Fractal texture - recursive patterns
        for i in range(10):
            notes.append(
                {"note": base_note + (i % 12), "start": i * 0.8, "dur": 0.6, "vel": 80}
            )
            # Add fractal echoes
            for echo in range(1, 3):
                notes.append(
                    {
                        "note": base_note + (i % 12) - (echo * 12),
                        "start": i * 0.8 + (echo * 0.2),
                        "dur": 0.3,
                        "vel": 40,
                    }
                )

    # Add act-specific modifications
    if act == 2:  # Development
        # Add more complex patterns
        for i in range(len(notes)):
            if i % 3 == 0:
                notes[i]["note"] += 7  # Add harmony
    elif act == 3:  # Grand Cadence
        # Add resolution patterns
        notes.append(
            {
                "note": base_note,
                "start": max([n["start"] + n["dur"] for n in notes]) + 0.5,
                "dur": 2.0,
                "vel": 100,
            }
        )

    return notes


def export_to_midi(
    voices_data: Dict[str, List[Dict[str, Any]]],
    bpm: int = 96,
    output_file: str = "out/opera/opera.mid",
):
    """Export voice data to MIDI file"""
    if not MIDO_AVAILABLE:
        print("❌ Cannot export MIDI: mido not available")
        return False

    try:
        # Create MIDI file
        mf = MidiFile(ticks_per_beat=480)
        tempo = bpm2tempo(bpm)

        # Add tempo track
        tempo_track = MidiTrack()
        tempo_track.append(Message("meta", type="set_tempo", tempo=tempo))
        mf.tracks.append(tempo_track)

        # Add track for each voice
        for voice_name, notes in voices_data.items():
            track = MidiTrack()
            mf.tracks.append(track)

            # Set program change for voice
            program_map = {
                "rust": 0,  # Acoustic Grand Piano
                "python": 1,  # Bright Acoustic Piano
                "julia": 2,  # Electric Grand Piano
                "typescript": 3,  # Honky-tonk Piano
                "go": 4,  # Electric Piano 1
                "csharp": 5,  # Electric Piano 2
                "sql": 6,  # Harpsichord
            }

            track.append(
                Message(
                    "program_change", program=program_map.get(voice_name, 0), time=0
                )
            )

            # Add notes
            last_time = 0
            for note in notes:
                note_on_time = int(note["start"] * 480)
                note_off_time = int(note["dur"] * 480)
                velocity = note.get("vel", 80)

                # Note on
                track.append(
                    Message(
                        "note_on",
                        note=note["note"],
                        velocity=velocity,
                        time=note_on_time - last_time,
                    )
                )

                # Note off
                track.append(
                    Message(
                        "note_off", note=note["note"], velocity=0, time=note_off_time
                    )
                )

                last_time = note_on_time + note_off_time

        # Save MIDI file
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        mf.save(output_file)

        print(f"✅ MIDI exported: {output_file}")
        return True

    except Exception as e:
        print(f"❌ MIDI export failed: {e}")
        return False


def create_manifest(
    voices_data: Dict[str, List[Dict[str, Any]]], seed: str, bpm: int, key: str
) -> Dict[str, Any]:
    """Create manifest with content hash for determinism verification"""
    import hashlib

    # Create content hash
    content_data = ""
    for voice_name, notes in voices_data.items():
        content_data += f"{voice_name}:{len(notes)}"
        for note in notes:
            content_data += f"{note['note']}{note['start']}{note['dur']}{note['vel']}"

    content_hash = hashlib.sha256(content_data.encode()).hexdigest()

    manifest = {
        "seed": seed,
        "bpm": bpm,
        "key": key,
        "acts": 3,
        "key_path": ["C", "G", "C"],
        "voices": list(voices_data.keys()),
        "total_notes": sum(len(notes) for notes in voices_data.values()),
        "content_sha256": content_hash,
        "timestamp": time.time(),
    }

    return manifest


def main():
    """Main entry point for MIDI export"""
    parser = argparse.ArgumentParser(description="🎭 Code Opera - MIDI Export")
    parser.add_argument(
        "--voices-file", default="out/opera/voices_data.json", help="Voices data file"
    )
    parser.add_argument(
        "--output", default="out/opera/opera.mid", help="Output MIDI file"
    )
    parser.add_argument("--bpm", type=int, default=96, help="BPM for MIDI export")
    parser.add_argument("--key", default="C", help="Key for MIDI export")
    parser.add_argument("--seed", default="opera-default", help="Seed for manifest")

    args = parser.parse_args()

    print("🎭 Code Opera - MIDI Export")
    print("=" * 50)

    # Create sample voice data if file doesn't exist
    if not Path(args.voices_file).exists():
        print(f"📝 Creating sample voice data: {args.voices_file}")

        # Sample voice configurations
        voice_configs = {
            "rust": {"harmony_note": "C", "texture": "dense", "tempo": 120},
            "python": {"harmony_note": "E", "texture": "smooth", "tempo": 110},
            "julia": {"harmony_note": "G", "texture": "fractal", "tempo": 140},
            "typescript": {"harmony_note": "A", "texture": "polyphonic", "tempo": 115},
            "go": {"harmony_note": "D", "texture": "sparse", "tempo": 100},
            "csharp": {"harmony_note": "F", "texture": "maximal", "tempo": 105},
            "sql": {"harmony_note": "B", "texture": "minimal", "tempo": 90},
        }

        # Generate notes for each voice
        voices_data = {}
        for voice_name, config in voice_configs.items():
            voices_data[voice_name] = create_voice_notes(voice_name, config)

        # Save voices data
        Path(args.voices_file).parent.mkdir(parents=True, exist_ok=True)
        with open(args.voices_file, "w") as f:
            json.dump(voices_data, f, indent=2)

        print(f"✅ Created sample voice data: {args.voices_file}")

    # Load voices data
    try:
        with open(args.voices_file, "r") as f:
            voices_data = json.load(f)
        print(f"📁 Loaded voice data: {len(voices_data)} voices")
    except Exception as e:
        print(f"❌ Failed to load voice data: {e}")
        return

    # Export to MIDI
    success = export_to_midi(voices_data, args.bpm, args.output)

    if success:
        # Create manifest
        manifest = create_manifest(voices_data, args.seed, args.bpm, args.key)
        manifest_file = Path(args.output).parent / "manifest.json"
        with open(manifest_file, "w") as f:
            json.dump(manifest, f, indent=2)

        print(f"✅ Manifest created: {manifest_file}")
        print(f"🎭 MIDI export complete: {args.output}")
        print(f"📊 Content hash: {manifest['content_sha256'][:16]}...")
    else:
        print("❌ MIDI export failed")


if __name__ == "__main__":
    import time

    main()

#!/usr/bin/env python3
"""
🎭 Code Opera - Counterpoint Guard
=================================

Simple counterpoint rules to avoid consecutive parallel 5ths/8ves.
Rejects bad parallel intervals between adjacent voices.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any


def bad_parallel_int(prev_int: int, cur_int: int) -> bool:
    """Check if parallel interval is bad (5th or 8ve)"""
    return cur_int in (7, 12) and cur_int == prev_int


def get_interval(note1: int, note2: int) -> int:
    """Get interval between two notes (in semitones)"""
    return abs(note1 - note2) % 12


def analyze_voice_motion(
    voice1_notes: List[Dict], voice2_notes: List[Dict]
) -> List[Tuple[int, int, str]]:
    """Analyze motion between two voices and identify bad parallels"""
    issues = []

    # Sort notes by start time
    voice1_sorted = sorted(voice1_notes, key=lambda x: x["start"])
    voice2_sorted = sorted(voice2_notes, key=lambda x: x["start"])

    # Find overlapping time periods
    for i, note1 in enumerate(voice1_sorted):
        for j, note2 in enumerate(voice2_sorted):
            # Check if notes overlap in time
            if (
                note1["start"] < note2["start"] + note2["dur"]
                and note2["start"] < note1["start"] + note1["dur"]
            ):

                # Calculate interval
                interval = get_interval(note1["note"], note2["note"])

                # Check for bad parallels with previous notes
                if i > 0 and j > 0:
                    prev_interval = get_interval(
                        voice1_sorted[i - 1]["note"], voice2_sorted[j - 1]["note"]
                    )

                    if bad_parallel_int(prev_interval, interval):
                        issues.append(
                            (
                                interval,
                                prev_interval,
                                f"Parallel {interval} at {note1['start']:.2f}s",
                            )
                        )

    return issues


def fix_parallel_interval(
    notes: List[Dict], target_note: int, adjustment: int
) -> List[Dict]:
    """Fix parallel interval by adjusting note"""
    for note in notes:
        if note["note"] == target_note:
            note["note"] = max(0, min(127, note["note"] + adjustment))
            break
    return notes


def apply_counterpoint_guard(
    voices_data: Dict[str, List[Dict[str, Any]]],
) -> Tuple[Dict[str, List[Dict[str, Any]]], List[str]]:
    """Apply counterpoint guard to voice data"""
    log_messages = []
    fixed_voices = {name: notes.copy() for name, notes in voices_data.items()}

    # Get voice names in order
    voice_names = list(voices_data.keys())

    # Check adjacent voice pairs
    for i in range(len(voice_names) - 1):
        voice1_name = voice_names[i]
        voice2_name = voice_names[i + 1]

        voice1_notes = fixed_voices[voice1_name]
        voice2_notes = fixed_voices[voice2_name]

        # Analyze motion between adjacent voices
        issues = analyze_voice_motion(voice1_notes, voice2_notes)

        if issues:
            log_messages.append(
                f"🎭 Found {len(issues)} parallel issues between {voice1_name} and {voice2_name}"
            )

            # Fix issues by adjusting notes
            for interval, prev_interval, description in issues:
                log_messages.append(f"   🔧 Fixing: {description}")

                # Adjust the second voice's note by ±1 semitone
                if interval == 7:  # Perfect 5th
                    adjustment = 1
                elif interval == 12:  # Perfect 8ve
                    adjustment = -1
                else:
                    adjustment = 1

                # Find and fix the problematic note
                for note in voice2_notes:
                    if note["note"] in [n["note"] for n in voice2_notes]:
                        note["note"] = max(0, min(127, note["note"] + adjustment))
                        break

                log_messages.append(f"   ✅ Adjusted note by {adjustment} semitones")
        else:
            log_messages.append(
                f"✅ No parallel issues between {voice1_name} and {voice2_name}"
            )

    return fixed_voices, log_messages


def main():
    """Main entry point for counterpoint guard"""
    parser = argparse.ArgumentParser(description="🎭 Code Opera - Counterpoint Guard")
    parser.add_argument(
        "--input", default="out/opera/voices_data.json", help="Input voices data file"
    )
    parser.add_argument(
        "--output",
        default="out/opera/voices_data_fixed.json",
        help="Output fixed voices data file",
    )
    parser.add_argument(
        "--log",
        default="out/opera/counterpoint.log",
        help="Log file for counterpoint fixes",
    )

    args = parser.parse_args()

    print("🎭 Code Opera - Counterpoint Guard")
    print("=" * 50)

    # Load voices data
    try:
        with open(args.input, "r") as f:
            voices_data = json.load(f)
        print(f"📁 Loaded voice data: {len(voices_data)} voices")
    except Exception as e:
        print(f"❌ Failed to load voice data: {e}")
        return

    # Apply counterpoint guard
    print("🔍 Analyzing voice motion for parallel intervals...")
    fixed_voices, log_messages = apply_counterpoint_guard(voices_data)

    # Save fixed voices data
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(fixed_voices, f, indent=2)

    print(f"✅ Fixed voices data saved: {args.output}")

    # Save log
    Path(args.log).parent.mkdir(parents=True, exist_ok=True)
    with open(args.log, "w") as f:
        f.write("🎭 Code Opera - Counterpoint Guard Log\n")
        f.write("=" * 50 + "\n\n")
        for message in log_messages:
            f.write(message + "\n")

    print(f"📝 Counterpoint log saved: {args.log}")

    # Summary
    total_issues = len([msg for msg in log_messages if "parallel issues" in msg])
    print(f"\n📊 Summary:")
    print(f"   Voices analyzed: {len(voices_data)}")
    print(f"   Parallel issues found: {total_issues}")
    print(f"   Fixed voices saved: {args.output}")
    print(f"   Log saved: {args.log}")


if __name__ == "__main__":
    import argparse

    main()

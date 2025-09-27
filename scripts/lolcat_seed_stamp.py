#!/usr/bin/env python3
"""
LOLcat++ Seed Stamp & Recall - Embed {seed, preset, macro, sidechain} into artifacts
"""
import json
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string_fx.lolcat_plus import lolcat_plus


class LOLcatSeedStamp:
    def __init__(self):
        self.stamp_data = {
            "seed": 1337,
            "preset": "classic",
            "macro": {"color": 0.0, "space": 0.0, "motion": 0.0, "crunch": 0.0},
            "sidechain": {"qps": 0.0, "error_rate": 0.0, "p95": 0.0},
            "timestamp": time.time(),
            "version": "1.0",
        }

    def set_stamp(self, seed=None, preset=None, macro=None, sidechain=None):
        """Set stamp data"""
        if seed is not None:
            self.stamp_data["seed"] = seed
        if preset is not None:
            self.stamp_data["preset"] = preset
        if macro is not None:
            self.stamp_data["macro"].update(macro)
        if sidechain is not None:
            self.stamp_data["sidechain"].update(sidechain)

        self.stamp_data["timestamp"] = time.time()

    def get_stamp_filename(self, base_name="lolcat_artifact"):
        """Generate filename with stamp data"""
        seed = self.stamp_data["seed"]
        preset = self.stamp_data["preset"]
        timestamp = int(self.stamp_data["timestamp"])

        return f"{base_name}_seed{seed}_{preset}_{timestamp}.json"

    def create_artifact(self, text, output_dir="out"):
        """Create artifact with stamp data"""
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Transform text with current stamp data
        result = lolcat_plus(
            text,
            seed=self.stamp_data["seed"],
            intensity=0.6,  # Default intensity
            uwu=0.3 + self.stamp_data["macro"]["color"] * 0.4,
            chaos=0.15 + self.stamp_data["macro"]["motion"] * 0.35,
            emoji=0.1 + self.stamp_data["macro"]["space"] * 0.1,
            nyan_trail=0.2 + self.stamp_data["macro"]["crunch"] * 0.4,
            gradient_phase=self.stamp_data["macro"]["color"],
        )

        # Create artifact data
        artifact = {
            "text": result["text"],
            "ansi": result["ansi"],
            "meta": result["meta"],
            "stamp": self.stamp_data,
            "transformation": {
                "input": text,
                "output": result["text"],
                "ansi_output": result["ansi"],
            },
        }

        # Generate filename
        filename = self.get_stamp_filename()
        filepath = os.path.join(output_dir, filename)

        # Write artifact
        with open(filepath, "w") as f:
            json.dump(artifact, f, indent=2)

        print(f"😺 Artifact created: {filepath}")
        return filepath

    def recall_artifact(self, filepath):
        """Recall artifact and recreate transformation"""
        with open(filepath, "r") as f:
            artifact = json.load(f)

        stamp = artifact["stamp"]

        # Recreate transformation with original parameters
        result = lolcat_plus(
            artifact["transformation"]["input"],
            seed=stamp["seed"],
            intensity=0.6,
            uwu=0.3 + stamp["macro"]["color"] * 0.4,
            chaos=0.15 + stamp["macro"]["motion"] * 0.35,
            emoji=0.1 + stamp["macro"]["space"] * 0.1,
            nyan_trail=0.2 + stamp["macro"]["crunch"] * 0.4,
            gradient_phase=stamp["macro"]["color"],
        )

        print(f"😺 Recalled artifact: {filepath}")
        print(f"   Seed: {stamp['seed']}")
        print(f"   Preset: {stamp['preset']}")
        print(f"   Macro: {stamp['macro']}")
        print(f"   Sidechain: {stamp['sidechain']}")
        print(f"   Result: {result['text']}")

        return result

    def demo_seed_stamping(self, text="Seed Stamping Demo"):
        """Demo seed stamping and recall"""
        print("😺 LOLcat++ Seed Stamping Demo")
        print("=" * 50)

        # Create multiple artifacts with different stamps
        stamps = [
            {
                "seed": 42,
                "preset": "classic",
                "macro": {"color": 0.0, "space": 0.0, "motion": 0.0, "crunch": 0.0},
            },
            {
                "seed": 123,
                "preset": "stage-punch",
                "macro": {"color": 0.5, "space": 0.3, "motion": 0.7, "crunch": 0.4},
            },
            {
                "seed": 456,
                "preset": "cat-walk",
                "macro": {"color": 0.2, "space": 0.1, "motion": 0.1, "crunch": 0.2},
            },
        ]

        artifacts = []

        for i, stamp in enumerate(stamps):
            print(f"\n{i+1}. Creating artifact with stamp {stamp['seed']}...")
            self.set_stamp(**stamp)
            filepath = self.create_artifact(text)
            artifacts.append(filepath)

        # Recall all artifacts
        print("\n😺 Recalling all artifacts...")
        for artifact in artifacts:
            self.recall_artifact(artifact)

    def test_perfect_rerun(self, text="Perfect Rerun Test"):
        """Test perfect rerun with same stamp"""
        print("😺 Testing Perfect Rerun...")
        print("=" * 50)

        # Create initial artifact
        self.set_stamp(
            seed=999,
            preset="classic",
            macro={"color": 0.5, "space": 0.3, "motion": 0.2, "crunch": 0.1},
        )
        filepath = self.create_artifact(text)

        # Recall and verify identical results
        recalled = self.recall_artifact(filepath)

        # Create new artifact with same stamp
        self.set_stamp(
            seed=999,
            preset="classic",
            macro={"color": 0.5, "space": 0.3, "motion": 0.2, "crunch": 0.1},
        )
        new_result = lolcat_plus(
            text,
            seed=999,
            intensity=0.6,
            uwu=0.3 + 0.5 * 0.4,
            chaos=0.15 + 0.2 * 0.35,
            emoji=0.1 + 0.3 * 0.1,
            nyan_trail=0.2 + 0.1 * 0.4,
            gradient_phase=0.5,
        )

        if recalled["text"] == new_result["text"]:
            print("✅ Perfect rerun - identical results!")
        else:
            print("❌ Rerun failed - different results")
            print(f"   Original: {recalled['text']}")
            print(f"   Rerun: {new_result['text']}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="LOLcat++ Seed Stamp & Recall")
    parser.add_argument("--demo", action="store_true", help="Demo seed stamping")
    parser.add_argument("--test", action="store_true", help="Test perfect rerun")
    parser.add_argument("--create", action="store_true", help="Create artifact")
    parser.add_argument("--recall", help="Recall artifact from file")
    parser.add_argument("--text", default="Seed stamp test", help="Text to transform")
    parser.add_argument("--seed", type=int, default=1337, help="Seed value")
    parser.add_argument("--preset", default="classic", help="Preset name")
    parser.add_argument("--output", default="out", help="Output directory")

    args = parser.parse_args()

    stamp_system = LOLcatSeedStamp()

    if args.demo:
        stamp_system.demo_seed_stamping(args.text)
    elif args.test:
        stamp_system.test_perfect_rerun(args.text)
    elif args.recall:
        stamp_system.recall_artifact(args.recall)
    elif args.create:
        stamp_system.set_stamp(seed=args.seed, preset=args.preset)
        stamp_system.create_artifact(args.text, args.output)
    else:
        print(
            "Usage: python3 lolcat_seed_stamp.py --demo | --test | --create | --recall <file>"
        )


if __name__ == "__main__":
    main()

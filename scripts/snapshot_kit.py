#!/usr/bin/env python3
"""
Snapshot Kit Generator - Socials/Docs Export
============================================

Generates snapshot kit for social media and documentation.
"""

import json
import os
import time
from typing import Dict, List, Any, Tuple
from pathlib import Path


class SnapshotKit:
    """
    Snapshot Kit Generator
    
    Generates snapshots for social media and documentation:
    - Low (Intensity 0.4, metrics 0.2)
    - Mid (Intensity 0.7, metrics 0.5)
    - Peak (Intensity 0.95, metrics 0.8, bloom off)
    """
    
    def __init__(self):
        self.output_dir = "out/touring/snapshots"
        self.snapshot_configs = {
            "low": {
                "intensity": 0.4,
                "metrics": 0.2,
                "bloom": False,
                "description": "Low intensity, subtle reactive motion"
            },
            "mid": {
                "intensity": 0.7,
                "metrics": 0.5,
                "bloom": False,
                "description": "Medium intensity, balanced reactive motion"
            },
            "peak": {
                "intensity": 0.95,
                "metrics": 0.8,
                "bloom": False,
                "description": "Peak intensity, maximum reactive motion"
            }
        }
    
    def generate_snapshots(self, scene_id: str, text: str = "Code Live") -> Dict[str, str]:
        """Generate snapshots for a scene"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        snapshots = {}
        
        for variant, config in self.snapshot_configs.items():
            # Generate snapshot HTML
            html_content = self._generate_snapshot_html(
                scene_id, variant, text, config
            )
            
            # Save snapshot
            filename = f"{scene_id}-{variant}.html"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(html_content)
            
            snapshots[variant] = filepath
            print(f"📸 Generated snapshot: {filename}")
        
        # Generate manifest
        manifest = self._generate_manifest(scene_id, snapshots)
        manifest_path = os.path.join(self.output_dir, f"{scene_id}-manifest.json")
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"📋 Generated manifest: {scene_id}-manifest.json")
        
        return snapshots
    
    def _generate_snapshot_html(self, scene_id: str, variant: str, text: str, config: Dict[str, Any]) -> str:
        """Generate HTML for a snapshot"""
        # Simulate processed text based on config
        processed_text = self._simulate_text_processing(text, config)
        
        # Generate timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate seed for reproducibility
        seed = hash(f"{scene_id}-{variant}-{timestamp}") % 10000
        
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Snapshot: {scene_id} - {variant}</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(45deg, #000, #111);
            color: #0f0;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }}
        .snapshot-header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .snapshot-title {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 20px #0f0;
        }}
        .snapshot-variant {{
            font-size: 1.2em;
            opacity: 0.8;
            margin-bottom: 20px;
        }}
        .snapshot-content {{
            font-size: 3em;
            line-height: 1.5;
            text-align: center;
            text-shadow: 0 0 30px #0f0;
            animation: glow 2s ease-in-out infinite alternate;
            margin: 30px 0;
        }}
        .snapshot-info {{
            font-size: 1em;
            opacity: 0.7;
            text-align: center;
            margin-top: 30px;
        }}
        .snapshot-footer {{
            position: fixed;
            bottom: 10px;
            right: 10px;
            font-size: 0.8em;
            opacity: 0.5;
        }}
        @keyframes glow {{
            from {{ text-shadow: 0 0 20px #0f0; }}
            to {{ text-shadow: 0 0 30px #0f0, 0 0 40px #0f0; }}
        }}
    </style>
</head>
<body>
    <div class="snapshot-header">
        <div class="snapshot-title">{scene_id}</div>
        <div class="snapshot-variant">{variant.upper()}</div>
    </div>
    
    <div class="snapshot-content">{processed_text}</div>
    
    <div class="snapshot-info">
        <div>Intensity: {config['intensity']}</div>
        <div>Metrics: {config['metrics']}</div>
        <div>Bloom: {'ON' if config['bloom'] else 'OFF'}</div>
        <div>{config['description']}</div>
    </div>
    
    <div class="snapshot-footer">
        <div>Seed: {seed}</div>
        <div>Timestamp: {timestamp}</div>
        <div>Scene: {scene_id}</div>
    </div>
</body>
</html>
        """
    
    def _simulate_text_processing(self, text: str, config: Dict[str, Any]) -> str:
        """Simulate text processing based on config"""
        intensity = config["intensity"]
        metrics = config["metrics"]
        bloom = config["bloom"]
        
        # Simulate intensity scaling
        if intensity < 0.5:
            # Low intensity - subtle effects
            result = text.replace(" ", "  ")
        elif intensity < 0.8:
            # Medium intensity - moderate effects
            result = " ".join([f"{c} {c}" for c in text])
        else:
            # High intensity - strong effects
            result = " ".join([f"{c} {c} {c}" for c in text])
        
        # Simulate metrics reactive motion
        if metrics > 0.5:
            result = result.replace(" ", "~")
        
        # Simulate bloom effect
        if bloom:
            result = "█" * len(result)
        
        return result
    
    def _generate_manifest(self, scene_id: str, snapshots: Dict[str, str]) -> Dict[str, Any]:
        """Generate manifest for snapshots"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "scene_id": scene_id,
            "timestamp": timestamp,
            "snapshots": {
                variant: {
                    "file": os.path.basename(filepath),
                    "config": self.snapshot_configs[variant],
                    "generated": timestamp
                }
                for variant, filepath in snapshots.items()
            },
            "metadata": {
                "generator": "SnapshotKit",
                "version": "1.0.0",
                "total_snapshots": len(snapshots)
            }
        }
    
    def generate_all_scenes(self, scenes_dir: str = "presets/scenes") -> Dict[str, Dict[str, str]]:
        """Generate snapshots for all scenes in directory"""
        all_snapshots = {}
        
        for scene_file in Path(scenes_dir).glob("*.json"):
            scene_id = scene_file.stem
            print(f"📸 Generating snapshots for: {scene_id}")
            
            snapshots = self.generate_snapshots(scene_id)
            all_snapshots[scene_id] = snapshots
        
        # Generate master manifest
        master_manifest = {
            "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "scenes": all_snapshots,
            "total_scenes": len(all_snapshots)
        }
        
        master_manifest_path = os.path.join(self.output_dir, "master-manifest.json")
        with open(master_manifest_path, 'w') as f:
            json.dump(master_manifest, f, indent=2)
        
        print(f"📋 Generated master manifest: master-manifest.json")
        
        return all_snapshots


def main():
    """Main CLI function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Snapshot Kit Generator - Socials/Docs Export",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate snapshots for single scene
  python3 scripts/snapshot_kit.py --scene tour_opener --text "Code Live"

  # Generate snapshots for all scenes
  python3 scripts/snapshot_kit.py --all-scenes

  # Generate with custom text
  python3 scripts/snapshot_kit.py --scene tour_opener --text "TuneZilla"
        """
    )
    
    parser.add_argument("--scene", help="Generate snapshots for specific scene")
    parser.add_argument("--text", default="Code Live", help="Text to process")
    parser.add_argument("--all-scenes", action="store_true", help="Generate snapshots for all scenes")
    parser.add_argument("--output-dir", default="out/touring/snapshots", help="Output directory")
    
    args = parser.parse_args()
    
    kit = SnapshotKit()
    
    if args.output_dir:
        kit.output_dir = args.output_dir
    
    if args.scene:
        # Generate snapshots for single scene
        print(f"📸 Generating snapshots for scene: {args.scene}")
        snapshots = kit.generate_snapshots(args.scene, args.text)
        
        print(f"\n✅ Generated {len(snapshots)} snapshots:")
        for variant, filepath in snapshots.items():
            print(f"  {variant}: {filepath}")
    
    elif args.all_scenes:
        # Generate snapshots for all scenes
        print("📸 Generating snapshots for all scenes...")
        all_snapshots = kit.generate_all_scenes()
        
        print(f"\n✅ Generated snapshots for {len(all_snapshots)} scenes:")
        for scene_id, snapshots in all_snapshots.items():
            print(f"  {scene_id}: {len(snapshots)} snapshots")
    
    else:
        parser.print_help()
        return
    
    print(f"\n📁 Output directory: {kit.output_dir}")
    print("🎉 Snapshot kit generation complete!")


if __name__ == "__main__":
    main()

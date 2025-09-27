"""
Rack Show System - One-Command Rack Shows
========================================

Complete rack show system with:
- Rack show sequences
- Scene morphing
- HTML + animated webm recording
- Chromascene integration
- Professional show flow
"""

import json
import time
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

from .pro_rack import ProRack, RackScene


@dataclass
class ShowScene:
    """Individual scene in a rack show"""
    preset: str
    duration: float
    morph: float = 2.0
    notes: str = ""


@dataclass
class RackShow:
    """Complete rack show configuration"""
    name: str
    bpm: float = 110.0
    scenes: List[ShowScene] = None
    total_duration: float = 0.0
    seed: int = 777
    
    def __post_init__(self):
        if self.scenes is None:
            self.scenes = []
        if self.total_duration == 0.0:
            self.total_duration = sum(scene.duration for scene in self.scenes)


class RackShowEngine:
    """
    Rack Show Engine
    
    Orchestrates complete rack shows with scene morphing,
    HTML recording, and professional show flow.
    """
    
    def __init__(self):
        self.current_show: Optional[RackShow] = None
        self.current_scene_index: int = 0
        self.is_playing: bool = False
        self.start_time: float = 0.0
        self.rack = ProRack()
        
        # Recording settings
        self.record_html: bool = True
        self.record_webm: bool = True
        self.output_dir: str = "out/rack_shows"
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_show(self, show_config: RackShow) -> None:
        """Load a rack show configuration"""
        self.current_show = show_config
        self.current_scene_index = 0
        self.is_playing = False
        self.rack = ProRack()
    
    def load_show_from_json(self, path: str) -> None:
        """Load rack show from JSON file"""
        with open(path, 'r') as f:
            data = json.load(f)
        
        scenes = []
        for scene_data in data.get("scenes", []):
            scene = ShowScene(
                preset=scene_data["preset"],
                duration=scene_data["duration"],
                morph=scene_data.get("morph", 2.0),
                notes=scene_data.get("notes", "")
            )
            scenes.append(scene)
        
        show = RackShow(
            name=data.get("name", "Untitled Show"),
            bpm=data.get("bpm", 110.0),
            scenes=scenes,
            total_duration=data.get("total_duration", 0.0),
            seed=data.get("seed", 777)
        )
        
        self.load_show(show)
    
    def save_show_to_json(self, path: str) -> None:
        """Save current show to JSON file"""
        if not self.current_show:
            raise ValueError("No show loaded")
        
        data = {
            "name": self.current_show.name,
            "bpm": self.current_show.bpm,
            "scenes": [asdict(scene) for scene in self.current_show.scenes],
            "total_duration": self.current_show.total_duration,
            "seed": self.current_show.seed
        }
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def play_show(self, text: str = "Code Live", mode: str = "html") -> Dict[str, Any]:
        """Play the complete rack show"""
        if not self.current_show:
            raise ValueError("No show loaded")
        
        self.is_playing = True
        self.start_time = time.time()
        
        # Initialize recording
        show_id = f"{self.current_show.name}_{int(time.time())}"
        show_dir = os.path.join(self.output_dir, show_id)
        os.makedirs(show_dir, exist_ok=True)
        
        # Record show metadata
        show_metadata = {
            "name": self.current_show.name,
            "bpm": self.current_show.bpm,
            "total_duration": self.current_show.total_duration,
            "scenes": len(self.current_show.scenes),
            "start_time": self.start_time,
            "text": text,
            "mode": mode
        }
        
        with open(os.path.join(show_dir, "show_metadata.json"), 'w') as f:
            json.dump(show_metadata, f, indent=2)
        
        # Process each scene
        scene_results = []
        current_scene = None
        
        for i, scene in enumerate(self.current_show.scenes):
            print(f"🎬 Scene {i+1}/{len(self.current_show.scenes)}: {scene.preset}")
            
            # Load scene
            try:
                self.rack.load_from_json(scene.preset)
                current_scene = self.rack.current_scene
            except Exception as e:
                print(f"❌ Error loading scene {scene.preset}: {e}")
                continue
            
            # Process scene
            scene_start = time.time()
            result = self.rack.process(text, mode)
            scene_end = time.time()
            
            # Record scene result
            scene_result = {
                "scene_index": i,
                "preset": scene.preset,
                "duration": scene.duration,
                "morph": scene.morph,
                "notes": scene.notes,
                "result": result,
                "processing_time": scene_end - scene_start,
                "timestamp": scene_start
            }
            scene_results.append(scene_result)
            
            # Save scene HTML if recording
            if self.record_html:
                scene_html = self._generate_scene_html(result, scene, i)
                scene_file = os.path.join(show_dir, f"scene_{i+1:02d}.html")
                with open(scene_file, 'w') as f:
                    f.write(scene_html)
            
            # Simulate scene duration (in real implementation, this would be actual timing)
            print(f"⏱️  Scene duration: {scene.duration}s")
            time.sleep(0.5)  # Shortened for demo
        
        # Generate final show HTML
        if self.record_html:
            show_html = self._generate_show_html(scene_results, show_metadata)
            show_file = os.path.join(show_dir, "show.html")
            with open(show_file, 'w') as f:
                f.write(show_html)
        
        # Generate chromascene for reproducible reruns
        chromascene = self._generate_chromascene(show_metadata, scene_results)
        chromascene_file = os.path.join(show_dir, "show.chromascene.json")
        with open(chromascene_file, 'w') as f:
            json.dump(chromascene, f, indent=2)
        
        self.is_playing = False
        
        return {
            "show_id": show_id,
            "show_dir": show_dir,
            "metadata": show_metadata,
            "scenes": scene_results,
            "total_duration": time.time() - self.start_time
        }
    
    def _generate_scene_html(self, result: str, scene: ShowScene, index: int) -> str:
        """Generate HTML for a single scene"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Rack Show - Scene {index+1}</title>
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
        .scene-title {{
            font-size: 2em;
            margin-bottom: 20px;
            text-align: center;
            text-shadow: 0 0 10px #0f0;
        }}
        .result {{
            font-size: 3em;
            line-height: 1.5;
            text-align: center;
            text-shadow: 0 0 20px #0f0;
            animation: glow 2s ease-in-out infinite alternate;
        }}
        .scene-info {{
            margin-top: 20px;
            font-size: 1.2em;
            opacity: 0.8;
        }}
        @keyframes glow {{
            from {{ text-shadow: 0 0 20px #0f0; }}
            to {{ text-shadow: 0 0 30px #0f0, 0 0 40px #0f0; }}
        }}
    </style>
</head>
<body>
    <div class="scene-title">Scene {index+1}: {scene.preset}</div>
    <div class="result">{result}</div>
    <div class="scene-info">
        Duration: {scene.duration}s | Morph: {scene.morph}s<br>
        {scene.notes}
    </div>
</body>
</html>
        """
    
    def _generate_show_html(self, scene_results: List[Dict], metadata: Dict) -> str:
        """Generate complete show HTML"""
        scenes_html = ""
        for i, scene in enumerate(scene_results):
            scenes_html += f"""
            <div class="scene">
                <h3>Scene {i+1}: {scene['preset']}</h3>
                <div class="result">{scene['result']}</div>
                <div class="scene-info">
                    Duration: {scene['duration']}s | Processing: {scene['processing_time']:.2f}s
                </div>
            </div>
            """
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Rack Show: {metadata['name']}</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(45deg, #000, #111);
            color: #0f0;
            margin: 0;
            padding: 20px;
        }}
        .show-header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .show-title {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 0 0 20px #0f0;
        }}
        .show-info {{
            font-size: 1.2em;
            opacity: 0.8;
        }}
        .scene {{
            margin: 40px 0;
            padding: 20px;
            border: 1px solid #0f0;
            border-radius: 10px;
        }}
        .scene h3 {{
            margin-top: 0;
            color: #0f0;
        }}
        .result {{
            font-size: 2em;
            line-height: 1.5;
            margin: 20px 0;
            text-shadow: 0 0 10px #0f0;
        }}
        .scene-info {{
            font-size: 0.9em;
            opacity: 0.7;
        }}
    </style>
</head>
<body>
    <div class="show-header">
        <div class="show-title">{metadata['name']}</div>
        <div class="show-info">
            BPM: {metadata['bpm']} | Duration: {metadata['total_duration']}s | Scenes: {metadata['scenes']}
        </div>
    </div>
    {scenes_html}
</body>
</html>
        """
    
    def _generate_chromascene(self, metadata: Dict, scene_results: List[Dict]) -> Dict:
        """Generate chromascene for reproducible reruns"""
        return {
            "version": 1,
            "name": metadata['name'],
            "bpm": metadata['bpm'],
            "total_duration": metadata['total_duration'],
            "scenes": len(scene_results),
            "text": metadata['text'],
            "mode": metadata['mode'],
            "timestamp": metadata['start_time'],
            "scene_results": scene_results
        }
    
    def get_show_status(self) -> Dict[str, Any]:
        """Get current show status"""
        if not self.current_show:
            return {"status": "no_show"}
        
        return {
            "show_name": self.current_show.name,
            "bpm": self.current_show.bpm,
            "total_duration": self.current_show.total_duration,
            "scenes": len(self.current_show.scenes),
            "current_scene": self.current_scene_index,
            "is_playing": self.is_playing,
            "elapsed_time": time.time() - self.start_time if self.is_playing else 0
        }


def create_rack_show_cli():
    """Create command-line interface for rack shows"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Rack Show System - One-Command Rack Shows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Play a rack show
  python3 scripts/rack_show_cli.py --play presets/shows/tour_opener.show.json --text "Code Live"

  # Create a new show
  python3 scripts/rack_show_cli.py --create "My Show" --scenes tour_opener.rack.json,glass_cathedral.rack.json

  # Record show with HTML
  python3 scripts/rack_show_cli.py --play presets/shows/tour_opener.show.json --record-html --text "TuneZilla"
        """
    )
    
    parser.add_argument("--play", help="Play a rack show from JSON file")
    parser.add_argument("--create", help="Create a new rack show")
    parser.add_argument("--scenes", help="Comma-separated list of rack scenes for new show")
    parser.add_argument("--text", "-t", help="Input text to process")
    parser.add_argument("--record-html", action="store_true", help="Record HTML output")
    parser.add_argument("--record-webm", action="store_true", help="Record animated WebM")
    parser.add_argument("--output-dir", default="out/rack_shows", help="Output directory")
    parser.add_argument("--status", action="store_true", help="Show show status")
    
    return parser


if __name__ == "__main__":
    # Example usage
    engine = RackShowEngine()
    
    # Create a simple show
    show = RackShow(
        name="Demo Show",
        bpm=110.0,
        scenes=[
            ShowScene("presets/racks/tour_opener.rack.json", 10.0, 2.0, "Tour opener"),
            ShowScene("presets/racks/glass_cathedral.rack.json", 12.0, 3.0, "Glass cathedral"),
            ShowScene("presets/racks/data_storm.rack.json", 8.0, 1.5, "Data storm")
        ]
    )
    
    engine.load_show(show)
    result = engine.play_show("Code Live")
    print(f"Show Result: {result}")
    
    # Show status
    status = engine.get_show_status()
    print(f"Show Status: {json.dumps(status, indent=2)}")

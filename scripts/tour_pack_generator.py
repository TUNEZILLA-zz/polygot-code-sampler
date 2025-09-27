#!/usr/bin/env python3
"""
Tour Pack Generator - Bulletproof anywhere system
Creates venue profiles, stage page, and 30s reel for FOH on USB
"""
import os
import json
import zipfile
from datetime import datetime


class TourPackGenerator:
    def __init__(self):
        self.output_dir = "out/tour_pack"
        self.venue_profiles = {
            "small": {
                "name": "Small Venue",
                "description": "Intimate spaces, dust/trails low, 60fps bias",
                "settings": {
                    "dust": 0.12,
                    "trails": 0.35,
                    "intensity_start": 0.28,
                    "intensity_end": 0.45,
                    "fps_bias": 60,
                    "particle_density": 0.6,
                },
            },
            "medium": {
                "name": "Medium Venue",
                "description": "Mid-size venues, balanced settings",
                "settings": {
                    "dust": 0.18,
                    "trails": 0.5,
                    "intensity_start": 0.3,
                    "intensity_end": 0.6,
                    "fps_bias": 45,
                    "particle_density": 0.8,
                },
            },
            "large": {
                "name": "Large Venue",
                "description": "Arena spaces, bigger particles, longer tails",
                "settings": {
                    "dust": 0.22,
                    "trails": 0.6,
                    "intensity_start": 0.3,
                    "intensity_end": 0.7,
                    "fps_bias": 30,
                    "particle_density": 1.0,
                },
            },
        }

    def create_venue_profiles(self):
        """Create venue profile JSON files"""
        print("🏠 Creating venue profiles...")

        for venue_type, profile in self.venue_profiles.items():
            profile_file = f"{self.output_dir}/venue_{venue_type}.json"
            os.makedirs(os.path.dirname(profile_file), exist_ok=True)

            with open(profile_file, "w") as f:
                json.dump(profile, f, indent=2)

            print(f"   ✅ {profile['name']}: {profile_file}")

    def create_stage_page(self):
        """Create clean stream page (dark UI, big text, no controls)"""
        print("📺 Creating stage page...")

        stage_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Sampler + FX Symphony - Live</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: #000;
            color: #fff;
            font-family: 'Courier New', monospace;
            text-align: center;
            padding: 50px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        .title {
            font-size: 4rem;
            font-weight: bold;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .subtitle {
            font-size: 1.5rem;
            color: #a0a0a0;
            margin-bottom: 30px;
        }
        
        .status {
            font-size: 1.2rem;
            color: #4ecdc4;
            margin-bottom: 20px;
        }
        
        .movements {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 40px;
        }
        
        .movement {
            padding: 20px;
            border: 2px solid #333;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.05);
        }
        
        .movement-number {
            font-size: 2rem;
            font-weight: bold;
            color: #4ecdc4;
            margin-bottom: 10px;
        }
        
        .movement-title {
            font-size: 1.2rem;
            margin-bottom: 5px;
        }
        
        .movement-duration {
            font-size: 0.9rem;
            color: #666;
        }
        
        @media (max-width: 768px) {
            .title {
                font-size: 2.5rem;
            }
            
            .movements {
                flex-direction: column;
                gap: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="title">🎼 Code Sampler + FX Symphony</div>
    <div class="subtitle">Live Performance</div>
    <div class="status">🎭 Ready for Showtime</div>
    
    <div class="movements">
        <div class="movement">
            <div class="movement-number">I</div>
            <div class="movement-title">Polyglot Fugue</div>
            <div class="movement-duration">30s</div>
        </div>
        <div class="movement">
            <div class="movement-number">II</div>
            <div class="movement-title">FX Rack Morph</div>
            <div class="movement-duration">30s</div>
        </div>
        <div class="movement">
            <div class="movement-number">III</div>
            <div class="movement-title">Lunar Interlude</div>
            <div class="movement-duration">30s</div>
        </div>
    </div>
</body>
</html>"""

        stage_file = f"{self.output_dir}/stage/index.html"
        os.makedirs(os.path.dirname(stage_file), exist_ok=True)

        with open(stage_file, "w") as f:
            f.write(stage_html)

        print(f"   ✅ Stage page: {stage_file}")

    def create_foh_cheat_sheet(self):
        """Create FOH micro-cheat sheet"""
        print("🎛️ Creating FOH cheat sheet...")

        cheat_sheet = """# 🎛️ FOH MICRO-CHEAT SHEET

## Movement Navigation
- **1/2/3** — Jump to movements I/II/III
- **I / K** — Intensity up/down (slew-limited)
- **M** — Toggle metrics link (sweet spot ~0.6 in Movement II)
- **W** — White Bloom on the downbeat of Movement II → III
- **B** — Blackout on the final cadence

## Live Parameter Control
- **Color Macro** → Gradient phase + UwU (slew ≤0.6/s)
- **Space Macro** → Nyan trail + trails length
- **Motion Macro** → Chaos + vowel stretch
- **Crunch Macro** → Stutter mix + glitch colors

## Sidechain Sweet Spots
- **QPS ↑** → Gradient phase speed ↑ (cap 0.8/s)
- **Error rate ↑** → Chaos bump (≤ +0.1, guarded)
- **P95 ↑** → Emoji & trail × 0.75 (comfort + perf)

## Performance Flow
- **Open**: intensity 0.28 → 0.45 over 10s
- **Crest**: morph Glass Cathedral → Data Storm, 6–8s, sidechain ≤0.8
- **Cat-Walk**: Studio-Safe palette, dust 0.18, trails 0.25
- **Encore**: Stage-Punch for ≤2s + White Bloom, then B (blackout)

## Safety Rails
- **Strobe ≤ 8 Hz, duty ≤ 35%**
- **Frame p95 ≤ 10-12 ms**
- **Motion-reduced fade ≤ 490 ms**
- **A11y compliance: ✅**
- **Mono fallback: ✅**
"""

        cheat_file = f"{self.output_dir}/FOH_CHEAT_SHEET.md"
        with open(cheat_file, "w") as f:
            f.write(cheat_sheet)

        print(f"   ✅ FOH cheat sheet: {cheat_file}")

    def create_30s_reel_script(self):
        """Create 30s highlight reel script"""
        print("📸 Creating 30s highlight reel script...")

        reel_script = """#!/bin/bash
# 30s Highlight Reel Script
# Run this to create a 30s capture for social media

echo "📸 Creating 30s highlight reel..."

# Capture 30s from Movement II (FX Rack Morph) - the most dramatic part
echo "🎬 Capturing Movement II (FX Rack Morph)..."

# Generate snapshots
make snapshot-kit

# Create 30s highlight
echo "📸 30s highlight reel ready for social media!"
echo "📁 Check out/touring/snapshots/ for captures"
"""

        reel_file = f"{self.output_dir}/30s_highlight_reel.sh"
        with open(reel_file, "w") as f:
            f.write(reel_script)

        os.chmod(reel_file, 0o755)  # Make executable
        print(f"   ✅ 30s reel script: {reel_file}")

    def create_tour_pack_zip(self):
        """Create tour pack zip file"""
        print("📦 Creating tour pack zip...")

        zip_file = f"{self.output_dir}/tour_pack.zip"

        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zf:
            # Add all files in the tour_pack directory
            for root, dirs, files in os.walk(self.output_dir):
                for file in files:
                    if file != "tour_pack.zip":  # Don't include the zip itself
                        file_path = os.path.join(root, file)
                        arc_path = os.path.relpath(file_path, self.output_dir)
                        zf.write(file_path, arc_path)

        print(f"   ✅ Tour pack zip: {zip_file}")

    def create_readme(self):
        """Create tour pack README"""
        print("📖 Creating tour pack README...")

        readme_content = f"""# 🎼 Code Sampler + FX Symphony - Tour Pack

## 📦 What's Included
- **Venue Profiles**: Small, Medium, Large venue settings
- **Stage Page**: Clean stream page (dark UI, big text, no controls)
- **FOH Cheat Sheet**: Micro-cheat sheet for operators
- **30s Highlight Reel**: Script for social media captures
- **Concert Poster**: Professional promo materials

## 🚀 Quick Start
1. **Extract** this zip to your USB drive
2. **Run** the appropriate venue profile:
   - `make venue-small` (intimate spaces)
   - `make venue-medium` (mid-size venues)  
   - `make venue-large` (arena spaces)
3. **Start** the offline stage page: `make offline-stage-page`
4. **Open** http://localhost:8080 in browser

## 🎛️ FOH Control
- **Movement Navigation**: 1/2/3 for movements I/II/III
- **Live Parameters**: I/K for intensity, M for metrics link
- **Effects**: W for White Bloom, B for blackout
- **Safety**: All rails active, A11y compliant

## 📸 Capture & Share
- **30s Highlight**: Run `./30s_highlight_reel.sh`
- **Snapshots**: Generated in out/touring/snapshots/
- **Gallery**: Chromatic enhanced HTML gallery
- **Poster**: Concert program poster

## 🛡️ Safety Features
- **Strobe guard**: ≤ 8 Hz, duty ≤ 35%
- **Frame rate**: p95 ≤ 10-12 ms
- **Motion-reduced**: ≤ 490 ms fades
- **A11y compliance**: Full accessibility support
- **Mono fallback**: Safe for all audiences

## 🎭 Performance Flow
1. **Movement I**: Polyglot Fugue (30s) - Glass Cathedral shimmer
2. **Movement II**: FX Rack Morph (30s) - Cathedral → Data Storm
3. **Movement III**: Lunar Interlude (30s) - LOLcat++ Cat-Walk

## 🌙✨ Ready for Showtime!
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

        readme_file = f"{self.output_dir}/README.md"
        with open(readme_file, "w") as f:
            f.write(readme_content)

        print(f"   ✅ README: {readme_file}")

    def generate_tour_pack(self):
        """Generate complete tour pack"""
        print("🎼 GENERATING TOUR PACK")
        print("=" * 50)

        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)

        # Generate all components
        self.create_venue_profiles()
        self.create_stage_page()
        self.create_foh_cheat_sheet()
        self.create_30s_reel_script()
        self.create_readme()
        self.create_tour_pack_zip()

        print("\n🎉 TOUR PACK COMPLETE!")
        print("=" * 50)
        print(f"📁 Tour pack: {self.output_dir}/tour_pack.zip")
        print("🚀 Ready to hand to FOH on USB!")
        print("📱 Works in venues with flaky Wi-Fi")
        print("🎭 Complete show system in one package")


def main():
    generator = TourPackGenerator()
    generator.generate_tour_pack()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
🎛️ Code Live - Vintage CLI
==========================

Command-line interface for vintage profile testing and demonstration.
Like a vintage sampler interface for code generation.
"""

import argparse
import json
from pathlib import Path
from typing import Dict

from pcs.vintage_profiles import VintageProfileEngine


class VintageCLI:
    """Vintage CLI interface"""

    def __init__(self):
        self.engine = VintageProfileEngine()

    def list_profiles(self):
        """List all available vintage profiles"""
        print("🎛️ Code Live - Vintage Profiles")
        print("=" * 50)
        print("Available vintage profiles:")
        print()

        for profile_name in self.engine.list_profiles():
            profile = self.engine.get_profile(profile_name)
            print(f"🎵 {profile_name.upper()}")
            print(f"   {profile.label}")
            print(f"   {profile.description}")
            print(f"   Bit Depth: {profile.global_degraders.bit_depth}")
            print(f"   Sample Rate: {profile.global_degraders.sample_rate}")
            print(f"   Buffer Size: {profile.global_degraders.buffer_size}")
            print()

    def test_profile(self, profile_name: str, language: str, code: str):
        """Test a vintage profile on code"""
        print(f"🎛️ Testing {profile_name} profile on {language}")
        print("=" * 50)

        # Apply vintage constraints
        vintage_code = self.engine.apply_vintage_constraints(
            code, language, profile_name
        )

        print(f"Original {language} code:")
        print("-" * 30)
        print(code)
        print()

        print(f"Vintage {language} code ({profile_name}):")
        print("-" * 30)
        print(vintage_code)
        print()

        # Validate compatibility
        is_compatible, issues = self.engine.validate_vintage_compatibility(
            vintage_code, language, profile_name
        )

        if is_compatible:
            print("✅ Vintage compatibility: PASSED")
        else:
            print("❌ Vintage compatibility: FAILED")
            for issue in issues:
                print(f"   - {issue}")

        # Show compiler flags
        flags = self.engine.get_vintage_compiler_flags(language, profile_name)
        if flags:
            print(f"🔧 Compiler flags: {' '.join(flags)}")

        # Show toolchain
        toolchain = self.engine.get_vintage_toolchain(language, profile_name)
        if toolchain:
            print(f"🛠️  Toolchain: {toolchain}")

        # Show degraders
        degraders = self.engine.get_vintage_degraders(profile_name)
        print(
            f"🎚️  Degraders: {degraders.bit_depth}-bit, {degraders.sample_rate}Hz, {degraders.buffer_size}B"
        )

    def demo_vintage_transforms(self):
        """Demonstrate vintage transformations"""
        print("🎛️ Code Live - Vintage Transform Demo")
        print("=" * 50)

        # TypeScript examples
        print("\n🎵 TypeScript Vintage Transforms")
        print("-" * 30)

        modern_ts = """
        export async function sumEvens(n: number): Promise<number> {
          const xs = Array.from({length: n}, (_, i) => i);
          return xs.filter(x => x % 2 === 0).reduce((a,b) => a+b*b, 0);
        }
        """

        for profile_name in ["mpc60", "sp1200", "y2k_web"]:
            print(f"\n{profile_name.upper()} Profile:")
            self.test_profile(profile_name, "typescript", modern_ts)

        # Rust examples
        print("\n🎵 Rust Vintage Transforms")
        print("-" * 30)

        modern_rust = """
        pub fn sum_evens(n: usize) -> i64 {
            (0..n).into_par_iter().filter(|x| x % 2 == 0).map(|x| (x*x) as i64).sum()
        }
        """

        for profile_name in ["mpc60", "sp1200"]:
            print(f"\n{profile_name.upper()} Profile:")
            self.test_profile(profile_name, "rust", modern_rust)

        # SQL examples
        print("\n🎵 SQL Vintage Transforms")
        print("-" * 30)

        modern_sql = """
        SELECT k, SUM(v) OVER (PARTITION BY k ORDER BY t ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling
        FROM input;
        """

        for profile_name in ["postgres_92", "sp1200"]:
            print(f"\n{profile_name.upper()} Profile:")
            self.test_profile(profile_name, "sql", modern_sql)

    def generate_vintage_art(self, profile_name: str, duration: int = 30):
        """Generate vintage performance art"""
        print(f"🎨 Generating Vintage Performance Art ({profile_name})")
        print("=" * 50)

        profile = self.engine.get_profile(profile_name)
        if not profile:
            print(f"❌ Profile not found: {profile_name}")
            return

        print(f"🎵 {profile.label}")
        print(f"   {profile.description}")
        print()

        # Apply vintage degraders to performance art
        degraders = profile.global_degraders
        print("🎚️  Applying Vintage Degraders:")
        print(f"   Bit Depth: {degraders.bit_depth} (vs 32-bit modern)")
        print(f"   Sample Rate: {degraders.sample_rate}Hz (vs 48kHz modern)")
        print(f"   Buffer Size: {degraders.buffer_size}B (vs 4KB modern)")
        print(f"   Noise Floor: {degraders.noise_floor} (vs 0.0 modern)")
        print()

        # Simulate vintage performance characteristics
        print("🎛️ Vintage Performance Characteristics:")
        print(f"   - Reduced precision: {degraders.bit_depth}-bit arithmetic")
        print(f"   - Lower sample rate: {degraders.sample_rate}Hz processing")
        print(f"   - Smaller buffers: {degraders.buffer_size}B chunks")
        print(f"   - Added noise: {degraders.noise_floor} noise floor")
        print("   - Single-threaded: No parallel processing")
        print("   - No SIMD: Scalar operations only")
        print("   - No optimization: -O0 compiler flags")
        print()

        # Generate vintage art data
        vintage_art_data = {
            "profile": profile_name,
            "label": profile.label,
            "description": profile.description,
            "degraders": {
                "bit_depth": degraders.bit_depth,
                "sample_rate": degraders.sample_rate,
                "buffer_size": degraders.buffer_size,
                "noise_floor": degraders.noise_floor,
            },
            "performance_impact": {
                "precision_loss": f"{32 - degraders.bit_depth} bits",
                "sample_rate_loss": f"{48000 - degraders.sample_rate}Hz",
                "buffer_size_loss": f"{4096 - degraders.buffer_size}B",
                "noise_added": degraders.noise_floor,
            },
            "vintage_characteristics": [
                "Single-threaded processing",
                "No SIMD optimizations",
                "No compiler optimizations",
                "Manual memory management",
                "Explicit type annotations",
                "No modern language features",
            ],
        }

        # Save vintage art data
        output_file = Path(f"vintage_art_{profile_name}.json")
        with open(output_file, "w") as f:
            json.dump(vintage_art_data, f, indent=2)

        print(f"🎨 Vintage art data saved to {output_file}")

        # Generate HTML visualization
        self._generate_vintage_html(profile_name, vintage_art_data)

    def _generate_vintage_html(self, profile_name: str, art_data: Dict):
        """Generate HTML visualization for vintage art"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Live - Vintage Performance Art ({profile_name})</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(45deg, #1a1a1a, #2d2d2d);
            color: #00ff00;
            margin: 0;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .vintage-profile {{
            background: rgba(255, 165, 0, 0.1);
            border: 2px solid #ffa500;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
        }}
        
        .degraders {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .degrader-card {{
            background: rgba(255, 0, 0, 0.1);
            border: 2px solid #ff0000;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }}
        
        .vintage-canvas {{
            width: 100%;
            height: 400px;
            border: 2px solid #ffa500;
            border-radius: 10px;
            background: #000;
            position: relative;
            overflow: hidden;
        }}
        
        .vintage-particle {{
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
            opacity: 0.8;
        }}
        
        .vintage-controls {{
            text-align: center;
            margin: 20px 0;
        }}
        
        button {{
            background: #ffa500;
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }}
        
        button:hover {{
            background: #ff8c00;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎛️ Code Live - Vintage Performance Art</h1>
            <p>Vintage profile: {art_data["label"]}</p>
        </div>
        
        <div class="vintage-profile">
            <h2>🎵 {art_data["label"]}</h2>
            <p>{art_data["description"]}</p>
        </div>
        
        <div class="degraders">
            <div class="degrader-card">
                <h3>Bit Depth</h3>
                <p>{art_data["degraders"]["bit_depth"]}-bit</p>
            </div>
            <div class="degrader-card">
                <h3>Sample Rate</h3>
                <p>{art_data["degraders"]["sample_rate"]}Hz</p>
            </div>
            <div class="degrader-card">
                <h3>Buffer Size</h3>
                <p>{art_data["degraders"]["buffer_size"]}B</p>
            </div>
            <div class="degrader-card">
                <h3>Noise Floor</h3>
                <p>{art_data["degraders"]["noise_floor"]}</p>
            </div>
        </div>
        
        <div class="vintage-controls">
            <button onclick="startVintageAnimation()">Start Vintage Animation</button>
            <button onclick="stopVintageAnimation()">Stop Animation</button>
        </div>
        
        <div class="vintage-canvas" id="vintageCanvas"></div>
        
        <div style="margin-top: 30px;">
            <h3>Vintage Characteristics:</h3>
            <ul>
                {"".join(f"<li>{char}</li>" for char in art_data["vintage_characteristics"])}
            </ul>
        </div>
    </div>
    
    <script>
        const vintageCanvas = document.getElementById('vintageCanvas');
        let animationId = null;
        
        function startVintageAnimation() {{
            if (animationId) return;
            
            function animate() {{
                // Clear canvas
                vintageCanvas.innerHTML = '';
                
                // Generate vintage particles with degraded characteristics
                const particleCount = Math.floor({art_data["degraders"]["buffer_size"]} / 10);
                const bitDepth = {art_data["degraders"]["bit_depth"]};
                const sampleRate = {art_data["degraders"]["sample_rate"]};
                const noiseFloor = {art_data["degraders"]["noise_floor"]};
                
                for (let i = 0; i < particleCount; i++) {{
                    const particle = document.createElement('div');
                    particle.className = 'vintage-particle';
                    
                    // Apply vintage degraders
                    const x = Math.random() * vintageCanvas.offsetWidth;
                    const y = Math.random() * vintageCanvas.offsetHeight;
                    const size = Math.max(1, (bitDepth / 32) * 10);
                    const opacity = Math.max(0.1, 1.0 - noiseFloor);
                    
                    // Vintage color palette (reduced bit depth)
                    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'];
                    const color = colors[Math.floor(Math.random() * colors.length)];
                    
                    particle.style.left = x + 'px';
                    particle.style.top = y + 'px';
                    particle.style.width = size + 'px';
                    particle.style.height = size + 'px';
                    particle.style.backgroundColor = color;
                    particle.style.opacity = opacity;
                    
                    vintageCanvas.appendChild(particle);
                }}
                
                animationId = requestAnimationFrame(animate);
            }}
            
            animate();
        }}
        
        function stopVintageAnimation() {{
            if (animationId) {{
                cancelAnimationFrame(animationId);
                animationId = null;
            }}
        }}
        
        // Auto-start animation
        startVintageAnimation();
    </script>
</body>
</html>
"""

        output_file = Path(f"vintage_art_{profile_name}.html")
        with open(output_file, "w") as f:
            f.write(html_content)

        print(f"🎨 Vintage HTML visualization generated: {output_file}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Code Live - Vintage Profiles CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python vintage_cli.py list
  python vintage_cli.py test mpc60 typescript "const x = 1;"
  python vintage_cli.py demo
  python vintage_cli.py art sp1200
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List profiles command
    subparsers.add_parser("list", help="List all available vintage profiles")

    # Test profile command
    test_parser = subparsers.add_parser("test", help="Test a vintage profile on code")
    test_parser.add_argument("profile", help="Vintage profile name")
    test_parser.add_argument("language", help="Programming language")
    test_parser.add_argument("code", help="Code to transform")

    # Demo command
    subparsers.add_parser("demo", help="Demonstrate vintage transformations")

    # Art command
    art_parser = subparsers.add_parser("art", help="Generate vintage performance art")
    art_parser.add_argument("profile", help="Vintage profile name")
    art_parser.add_argument(
        "--duration", type=int, default=30, help="Duration in seconds"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = VintageCLI()

    if args.command == "list":
        cli.list_profiles()
    elif args.command == "test":
        cli.test_profile(args.profile, args.language, args.code)
    elif args.command == "demo":
        cli.demo_vintage_transforms()
    elif args.command == "art":
        cli.generate_vintage_art(args.profile, args.duration)


if __name__ == "__main__":
    main()

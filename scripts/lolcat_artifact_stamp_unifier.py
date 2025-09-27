#!/usr/bin/env python3
"""
LOLcat++ Artifact Stamp Unifier - Standardize artifact stamp format for side-by-side comparisons
"""
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string_fx.lolcat_plus import lolcat_plus

class LOLcatArtifactStampUnifier:
    def __init__(self):
        self.timestamp = int(time.time())
        
    def generate_unified_stamp(self, slug, preset, seed, macro, timestamp=None):
        """Generate unified artifact stamp format"""
        if timestamp is None:
            timestamp = self.timestamp
            
        # Format: <slug>__preset-<name>__seed-<n>__macro-C<S>-S<P>-M<M>-C<R>__t-<timestamp>.html
        macro_str = f"C{macro.get('color', 0):.1f}-S{macro.get('space', 0):.1f}-M{macro.get('motion', 0):.1f}-C{macro.get('crunch', 0):.1f}"
        
        stamp = f"{slug}__preset-{preset}__seed-{seed}__macro-{macro_str}__t-{timestamp}.html"
        
        return stamp
        
    def create_unified_artifact(self, text, slug, preset, seed, macro, output_dir="out"):
        """Create artifact with unified stamp format"""
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Transform text
        result = lolcat_plus(
            text,
            seed=seed,
            intensity=0.6,
            uwu=0.3 + macro.get('color', 0) * 0.4,
            chaos=0.15 + macro.get('motion', 0) * 0.35,
            emoji=0.1 + macro.get('space', 0) * 0.1,
            nyan_trail=0.2 + macro.get('crunch', 0) * 0.4,
            gradient_phase=macro.get('color', 0)
        )
        
        # Generate unified filename
        filename = self.generate_unified_stamp(slug, preset, seed, macro)
        filepath = os.path.join(output_dir, filename)
        
        # Create HTML artifact
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>LOLcat++ Artifact</title>
    <style>
        body {{ font-family: monospace; background: #000; color: #fff; padding: 20px; }}
        .artifact {{ font-size: 24px; line-height: 1.5; }}
        .meta {{ font-size: 12px; color: #666; margin-top: 20px; }}
        .ansi {{ white-space: pre-wrap; }}
    </style>
</head>
<body>
    <div class="artifact">{result['text']}</div>
    <div class="meta">
        <p>Preset: {preset}</p>
        <p>Seed: {seed}</p>
        <p>Macro: {macro}</p>
        <p>Timestamp: {self.timestamp}</p>
    </div>
</body>
</html>
"""
        
        # Write artifact
        with open(filepath, 'w') as f:
            f.write(html_content)
            
        print(f"😺 Unified artifact created: {filepath}")
        return filepath
        
    def demo_unified_stamps(self, text="Unified Stamp Demo"):
        """Demo unified stamp format"""
        print("😺 LOLcat++ Artifact Stamp Unifier Demo")
        print("=" * 50)
        
        # Create multiple artifacts with different parameters
        artifacts = [
            {
                "slug": "lolcat-demo",
                "preset": "classic",
                "seed": 42,
                "macro": {"color": 0.0, "space": 0.0, "motion": 0.0, "crunch": 0.0}
            },
            {
                "slug": "lolcat-demo",
                "preset": "stage-punch",
                "seed": 42,
                "macro": {"color": 0.5, "space": 0.3, "motion": 0.7, "crunch": 0.4}
            },
            {
                "slug": "lolcat-demo",
                "preset": "cat-walk",
                "seed": 123,
                "macro": {"color": 0.2, "space": 0.1, "motion": 0.1, "crunch": 0.2}
            }
        ]
        
        for i, artifact in enumerate(artifacts, 1):
            print(f"\n{i}. Creating artifact:")
            print(f"   Slug: {artifact['slug']}")
            print(f"   Preset: {artifact['preset']}")
            print(f"   Seed: {artifact['seed']}")
            print(f"   Macro: {artifact['macro']}")
            
            filepath = self.create_unified_artifact(
                text, 
                artifact['slug'], 
                artifact['preset'], 
                artifact['seed'], 
                artifact['macro']
            )
            
            print(f"   Filename: {os.path.basename(filepath)}")
            
    def test_side_by_side_comparison(self, text="Side-by-Side Comparison"):
        """Test side-by-side comparison with unified stamps"""
        print("😺 Testing Side-by-Side Comparison...")
        print("=" * 50)
        
        # Create two artifacts with same seed but different presets
        classic_file = self.create_unified_artifact(
            text, "comparison", "classic", 999, 
            {"color": 0.0, "space": 0.0, "motion": 0.0, "crunch": 0.0}
        )
        
        stage_punch_file = self.create_unified_artifact(
            text, "comparison", "stage-punch", 999,
            {"color": 0.5, "space": 0.3, "motion": 0.7, "crunch": 0.4}
        )
        
        print(f"\n📁 Classic: {os.path.basename(classic_file)}")
        print(f"📁 Stage-Punch: {os.path.basename(stage_punch_file)}")
        
        # Show the difference in filenames
        print("\n🔍 Filename Analysis:")
        print(f"   Both use same seed (999) for identical base transformation")
        print(f"   Different presets: classic vs stage-punch")
        print(f"   Different macros: C0.0-S0.0-M0.0-C0.0 vs C0.5-S0.3-M0.7-C0.4")
        print(f"   Same timestamp: {self.timestamp}")
        
    def generate_comparison_matrix(self, text="Comparison Matrix"):
        """Generate comparison matrix with different parameters"""
        print("😺 Generating Comparison Matrix...")
        print("=" * 50)
        
        # Matrix of parameters to compare
        presets = ["classic", "stage-punch", "cat-walk"]
        seeds = [42, 123, 456]
        macro_configs = [
            {"color": 0.0, "space": 0.0, "motion": 0.0, "crunch": 0.0},
            {"color": 0.5, "space": 0.3, "motion": 0.7, "crunch": 0.4},
            {"color": 0.2, "space": 0.1, "motion": 0.1, "crunch": 0.2}
        ]
        
        artifacts = []
        
        for preset in presets:
            for seed in seeds:
                for macro in macro_configs:
                    filepath = self.create_unified_artifact(
                        text, "matrix", preset, seed, macro
                    )
                    artifacts.append(filepath)
                    
        print(f"\n📊 Generated {len(artifacts)} artifacts for comparison")
        print("📁 Artifacts created in out/ directory")
        
        # Show filename pattern
        print(f"\n🔍 Filename Pattern:")
        print(f"   matrix__preset-<name>__seed-<n>__macro-C<S>-S<P>-M<M>-C<R>__t-<timestamp>.html")
        
        return artifacts

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="LOLcat++ Artifact Stamp Unifier")
    parser.add_argument("--demo", action="store_true", help="Demo unified stamps")
    parser.add_argument("--comparison", action="store_true", help="Test side-by-side comparison")
    parser.add_argument("--matrix", action="store_true", help="Generate comparison matrix")
    parser.add_argument("--create", action="store_true", help="Create single artifact")
    parser.add_argument("--slug", default="lolcat-demo", help="Artifact slug")
    parser.add_argument("--preset", default="classic", help="Preset name")
    parser.add_argument("--seed", type=int, default=42, help="Seed value")
    parser.add_argument("--text", default="Artifact stamp test", help="Text to transform")
    parser.add_argument("--output", default="out", help="Output directory")
    
    args = parser.parse_args()
    
    unifier = LOLcatArtifactStampUnifier()
    
    if args.demo:
        unifier.demo_unified_stamps(args.text)
    elif args.comparison:
        unifier.test_side_by_side_comparison(args.text)
    elif args.matrix:
        unifier.generate_comparison_matrix(args.text)
    elif args.create:
        macro = {"color": 0.0, "space": 0.0, "motion": 0.0, "crunch": 0.0}
        unifier.create_unified_artifact(args.text, args.slug, args.preset, args.seed, macro, args.output)
    else:
        print("Usage: python3 lolcat_artifact_stamp_unifier.py --demo | --comparison | --matrix | --create")

if __name__ == "__main__":
    main()

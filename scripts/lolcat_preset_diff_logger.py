#!/usr/bin/env python3
"""
LOLcat++ Preset Diff Logger - Log only parameters that change across A/B morphs
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string_fx.lolcat_plus import lolcat_plus

class LOLcatPresetDiffLogger:
    def __init__(self):
        self.presets = {
            "classic": {
                "intensity": 0.5, "uwu": 0.3, "chaos": 0.15, 
                "emoji": 0.1, "nyan_trail": 0.2, "gradient_phase": 0.0
            },
            "stage-punch": {
                "intensity": 0.7, "uwu": 0.4, "chaos": 0.32, 
                "emoji": 0.16, "nyan_trail": 0.42, "gradient_phase": 0.0
            },
            "cat-walk": {
                "intensity": 0.4, "uwu": 0.18, "chaos": 0.04, 
                "emoji": 0.08, "nyan_trail": 0.28, "gradient_phase": 0.0
            },
            "classic-lite": {
                "intensity": 0.5, "uwu": 0.28, "chaos": 0.15, 
                "emoji": 0.06, "nyan_trail": 0.12, "gradient_phase": 0.0
            }
        }
        
    def get_preset_params(self, preset_name):
        """Get parameters for a preset"""
        return self.presets.get(preset_name, {})
        
    def calculate_diff(self, preset_a, preset_b):
        """Calculate diff between two presets"""
        params_a = self.get_preset_params(preset_a)
        params_b = self.get_preset_params(preset_b)
        
        diff = {}
        all_keys = set(params_a.keys()) | set(params_b.keys())
        
        for key in all_keys:
            val_a = params_a.get(key, 0.0)
            val_b = params_b.get(key, 0.0)
            
            if val_a != val_b:
                diff[key] = {
                    "from": val_a,
                    "to": val_b,
                    "delta": val_b - val_a
                }
                
        return diff
        
    def format_diff_log(self, preset_a, preset_b, diff):
        """Format diff log in PR-friendly format"""
        if not diff:
            return f"[LOLcat++] No parameter changes between {preset_a} and {preset_b}"
            
        log_lines = [f"[LOLcat++] diff: {preset_a} → {preset_b}"]
        
        for param, change in diff.items():
            from_val = change["from"]
            to_val = change["to"]
            delta = change["delta"]
            
            if delta > 0:
                direction = "↑"
            elif delta < 0:
                direction = "↓"
            else:
                direction = "="
                
            log_lines.append(f"  {param}: {from_val:.2f}→{to_val:.2f} ({direction}{abs(delta):.2f})")
            
        return "\n".join(log_lines)
        
    def log_morph_diff(self, preset_a, preset_b):
        """Log diff for a morph between two presets"""
        diff = self.calculate_diff(preset_a, preset_b)
        log = self.format_diff_log(preset_a, preset_b, diff)
        
        print(f"😺 Preset Diff Log:")
        print(log)
        
        return diff
        
    def demo_diff_logging(self):
        """Demo diff logging for common morphs"""
        print("😺 LOLcat++ Preset Diff Logger Demo")
        print("=" * 50)
        
        morphs = [
            ("classic", "stage-punch"),
            ("classic-lite", "stage-punch"),
            ("cat-walk", "classic"),
            ("stage-punch", "cat-walk")
        ]
        
        for preset_a, preset_b in morphs:
            print(f"\n🎭 Morph: {preset_a} → {preset_b}")
            self.log_morph_diff(preset_a, preset_b)
            
    def test_parameter_changes(self, text="Parameter Change Test"):
        """Test parameter changes with diff logging"""
        print("😺 Testing Parameter Changes...")
        
        # Test classic → stage-punch
        print("\n1. Classic → Stage-Punch:")
        diff = self.log_morph_diff("classic", "stage-punch")
        
        # Transform with both presets
        result_a = lolcat_plus(text, **self.get_preset_params("classic"))
        result_b = lolcat_plus(text, **self.get_preset_params("stage-punch"))
        
        print(f"   Classic: {result_a['text']}")
        print(f"   Stage-Punch: {result_b['text']}")
        
        # Test classic-lite → stage-punch
        print("\n2. Classic-Lite → Stage-Punch:")
        diff = self.log_morph_diff("classic-lite", "stage-punch")
        
        result_a = lolcat_plus(text, **self.get_preset_params("classic-lite"))
        result_b = lolcat_plus(text, **self.get_preset_params("stage-punch"))
        
        print(f"   Classic-Lite: {result_a['text']}")
        print(f"   Stage-Punch: {result_b['text']}")
        
    def generate_pr_diff(self, preset_a, preset_b):
        """Generate PR-friendly diff for GitHub"""
        diff = self.calculate_diff(preset_a, preset_b)
        
        if not diff:
            return f"## LOLcat++ Preset Diff\n\nNo parameter changes between `{preset_a}` and `{preset_b}`."
            
        pr_content = f"## LOLcat++ Preset Diff\n\n**Morph:** `{preset_a}` → `{preset_b}`\n\n"
        pr_content += "| Parameter | From | To | Delta |\n"
        pr_content += "|-----------|------|----|-------|\n"
        
        for param, change in diff.items():
            from_val = change["from"]
            to_val = change["to"]
            delta = change["delta"]
            
            pr_content += f"| `{param}` | {from_val:.2f} | {to_val:.2f} | {delta:+.2f} |\n"
            
        return pr_content

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="LOLcat++ Preset Diff Logger")
    parser.add_argument("--demo", action="store_true", help="Demo diff logging")
    parser.add_argument("--test", action="store_true", help="Test parameter changes")
    parser.add_argument("--pr", action="store_true", help="Generate PR diff")
    parser.add_argument("--preset-a", default="classic", help="Preset A name")
    parser.add_argument("--preset-b", default="stage-punch", help="Preset B name")
    parser.add_argument("--text", default="Diff logger test", help="Text to transform")
    
    args = parser.parse_args()
    
    diff_logger = LOLcatPresetDiffLogger()
    
    if args.demo:
        diff_logger.demo_diff_logging()
    elif args.test:
        diff_logger.test_parameter_changes(args.text)
    elif args.pr:
        pr_diff = diff_logger.generate_pr_diff(args.preset_a, args.preset_b)
        print(pr_diff)
    else:
        # Single diff log
        diff_logger.log_morph_diff(args.preset_a, args.preset_b)

if __name__ == "__main__":
    main()

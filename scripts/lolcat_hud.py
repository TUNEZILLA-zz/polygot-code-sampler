#!/usr/bin/env python3
"""
LOLcat++ Mini HUD - Real-time parameter monitoring with amber warnings
"""
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string_fx.lolcat_plus import lolcat_plus

class LOLcatHUD:
    def __init__(self):
        self.emoji_density = 0.0
        self.chaos_level = 0.0
        self.trail_intensity = 0.0
        self.gradient_phase = 0.0
        self.uwu_level = 0.0
        self.intensity = 0.0
        
        # Warning thresholds
        self.emoji_warning = 0.15  # Amber at 75% of max (0.2)
        self.chaos_warning = 0.4   # Amber at 80% of max (0.5)
        self.trail_warning = 0.48  # Amber at 80% of max (0.6)
        
    def update_params(self, emoji, chaos, trail, gradient, uwu, intensity):
        """Update HUD parameters"""
        self.emoji_density = emoji
        self.chaos_level = chaos
        self.trail_intensity = trail
        self.gradient_phase = gradient
        self.uwu_level = uwu
        self.intensity = intensity
        
    def get_status_color(self, value, warning_threshold, max_value):
        """Get color based on value and thresholds"""
        if value >= max_value:
            return "🔴"  # Red - at max
        elif value >= warning_threshold:
            return "🟡"  # Amber - warning
        else:
            return "🟢"  # Green - safe
            
    def render_hud(self):
        """Render the mini HUD"""
        # Clear screen (simple approach)
        print("\033[2J\033[H", end="")
        
        # Header
        print("😺 LOLcat++ Mini HUD - Real-time Parameter Monitor")
        print("=" * 60)
        
        # Emoji density
        emoji_color = self.get_status_color(self.emoji_density, self.emoji_warning, 0.2)
        emoji_bar = "█" * int(self.emoji_density * 50) + "░" * (50 - int(self.emoji_density * 50))
        print(f"😸 Emoji Density: {emoji_color} {self.emoji_density:.3f} [{emoji_bar}]")
        
        # Chaos level
        chaos_color = self.get_status_color(self.chaos_level, self.chaos_warning, 0.5)
        chaos_bar = "█" * int(self.chaos_level * 50) + "░" * (50 - int(self.chaos_level * 50))
        print(f"🌀 Chaos Level:   {chaos_color} {self.chaos_level:.3f} [{chaos_bar}]")
        
        # Trail intensity
        trail_color = self.get_status_color(self.trail_intensity, self.trail_warning, 0.6)
        trail_bar = "█" * int(self.trail_intensity * 50) + "░" * (50 - int(self.trail_intensity * 50))
        print(f"🌈 Trail:        {trail_color} {self.trail_intensity:.3f} [{trail_bar}]")
        
        # Additional parameters
        print(f"🎨 Gradient:     {self.gradient_phase:.3f}")
        print(f"😊 UwU Level:    {self.uwu_level:.3f}")
        print(f"⚡ Intensity:    {self.intensity:.3f}")
        
        # Warnings
        warnings = []
        if self.emoji_density >= self.emoji_warning:
            warnings.append("⚠️  Emoji density high")
        if self.chaos_level >= self.chaos_warning:
            warnings.append("⚠️  Chaos level high")
        if self.trail_intensity >= self.trail_warning:
            warnings.append("⚠️  Trail intensity high")
            
        if warnings:
            print("\n🚨 WARNINGS:")
            for warning in warnings:
                print(f"   {warning}")
        else:
            print("\n✅ All parameters within safe limits")
            
        # Footer
        print("\n" + "=" * 60)
        print("Press Ctrl+C to exit")
        
    def demo_animation(self):
        """Demo animation showing parameter changes"""
        print("😺 Starting LOLcat++ HUD Demo Animation...")
        print("Press Ctrl+C to exit")
        
        try:
            while True:
                # Simulate parameter changes
                import math
                t = time.time()
                
                # Animate parameters
                emoji = 0.1 + 0.1 * math.sin(t * 0.5)
                chaos = 0.2 + 0.2 * math.sin(t * 0.3)
                trail = 0.3 + 0.2 * math.sin(t * 0.4)
                gradient = (t * 0.1) % 1.0
                uwu = 0.3 + 0.2 * math.sin(t * 0.6)
                intensity = 0.5 + 0.3 * math.sin(t * 0.2)
                
                # Update and render
                self.update_params(emoji, chaos, trail, gradient, uwu, intensity)
                self.render_hud()
                
                time.sleep(0.1)  # 10 FPS
                
        except KeyboardInterrupt:
            print("\n😺 HUD Demo stopped")
            
    def test_preset(self, preset_name, text="Test text"):
        """Test a preset and show HUD"""
        from string_fx.lolcat_plus import lolcat_plus
        
        # Get preset parameters
        presets = {
            "classic": {"intensity": 0.5, "uwu": 0.3, "chaos": 0.15, "emoji": 0.1, "nyan_trail": 0.2},
            "uwu-rainbow": {"intensity": 0.8, "uwu": 0.6, "chaos": 0.25, "emoji": 0.2, "nyan_trail": 0.45},
            "stage-punch": {"intensity": 0.7, "uwu": 0.4, "chaos": 0.32, "emoji": 0.16, "nyan_trail": 0.42},
            "cat-walk": {"intensity": 0.4, "uwu": 0.18, "chaos": 0.04, "emoji": 0.08, "nyan_trail": 0.28}
        }
        
        if preset_name not in presets:
            print(f"Unknown preset: {preset_name}")
            return
            
        params = presets[preset_name]
        
        # Update HUD with preset values
        self.update_params(
            params["emoji"], 
            params["chaos"], 
            params["nyan_trail"], 
            0.0,  # gradient_phase
            params["uwu"], 
            params["intensity"]
        )
        
        # Render HUD
        self.render_hud()
        
        # Show transformed text
        result = lolcat_plus(text, **params)
        print(f"\n📝 Transformed text: {result['text']}")
        print(f"🎨 ANSI output: {result['ansi']}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="LOLcat++ Mini HUD")
    parser.add_argument("--demo", action="store_true", help="Run demo animation")
    parser.add_argument("--preset", help="Test preset (classic, uwu-rainbow, stage-punch, cat-walk)")
    parser.add_argument("--text", default="Hello world!", help="Text to transform")
    
    args = parser.parse_args()
    
    hud = LOLcatHUD()
    
    if args.demo:
        hud.demo_animation()
    elif args.preset:
        hud.test_preset(args.preset, args.text)
    else:
        print("Usage: python3 lolcat_hud.py --demo | --preset <name> [--text <text>]")

if __name__ == "__main__":
    main()

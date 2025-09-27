#!/usr/bin/env python3
"""
LOLcat++ Palette Autoselect by Scene - Map scene tag → palette with metrics.link bias
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string_fx.lolcat_plus import lolcat_plus, EMOJI_PALETTES

class LOLcatPaletteAutoselect:
    def __init__(self):
        # Scene → palette mapping
        self.scene_palette_map = {
            "warmup": "copper",
            "build": "neon", 
            "impact": "cyberpunk",
            "texture": "emerald",
            "moonlight-sonata": "vintage",
            "clair-de-lune": "emerald",
            "lunar-recital": "gold",
            "cyberpunk": "cyberpunk",
            "neon-bloom": "neon",
            "data-storm": "cyberpunk",
            "glass-cathedral": "emerald",
            "default": "default"
        }
        
        # High-contrast palettes for high metrics.link
        self.high_contrast_palettes = ["cyberpunk", "neon", "gold"]
        
        # Soft palettes for low metrics.link
        self.soft_palettes = ["emerald", "vintage", "default"]
        
        # Copper palette (new addition)
        self.copper_palette = ["🟠", "🧡", "🔥", "⭐", "🌟", "💫", "🔆", "☀️", "🌅"]
        
        # Add copper to palettes
        EMOJI_PALETTES["copper"] = self.copper_palette
        
    def get_palette_for_scene(self, scene_name, metrics_link=0.0):
        """Get palette for scene with metrics.link bias"""
        # Get base palette for scene
        base_palette = self.scene_palette_map.get(scene_name, "default")
        
        # Apply metrics.link bias
        if metrics_link > 0.7:
            # High metrics.link → bias to high-contrast palettes
            if base_palette in self.soft_palettes:
                # Switch to high-contrast equivalent
                if base_palette == "emerald":
                    return "cyberpunk"
                elif base_palette == "vintage":
                    return "neon"
                elif base_palette == "default":
                    return "gold"
        else:
            # Low metrics.link → bias to soft palettes
            if base_palette in self.high_contrast_palettes:
                # Switch to soft equivalent
                if base_palette == "cyberpunk":
                    return "emerald"
                elif base_palette == "neon":
                    return "vintage"
                elif base_palette == "gold":
                    return "default"
                    
        return base_palette
        
    def transform_with_scene(self, text, scene_name, metrics_link=0.0, **kwargs):
        """Transform text with scene-specific palette selection"""
        palette = self.get_palette_for_scene(scene_name, metrics_link)
        
        print(f"😺 Scene: {scene_name} | Metrics Link: {metrics_link:.2f} | Palette: {palette}")
        
        return lolcat_plus(text, emoji_palette=palette, **kwargs)
        
    def demo_scene_palette_mapping(self, text="Scene Palette Demo"):
        """Demo scene palette mapping"""
        print("😺 LOLcat++ Palette Autoselect Demo")
        print("=" * 50)
        
        scenes = [
            ("warmup", 0.3),
            ("build", 0.5),
            ("impact", 0.8),
            ("texture", 0.2),
            ("moonlight-sonata", 0.4),
            ("clair-de-lune", 0.6),
            ("lunar-recital", 0.9)
        ]
        
        for scene, metrics_link in scenes:
            result = self.transform_with_scene(text, scene, metrics_link, seed=1337)
            print(f"   {scene} (link={metrics_link:.1f}): {result['text']}")
            
    def test_metrics_link_bias(self, text="Metrics Link Bias Test"):
        """Test metrics.link bias on palette selection"""
        print("😺 Testing Metrics Link Bias...")
        print("=" * 50)
        
        test_scenes = [
            ("warmup", "copper"),
            ("build", "neon"),
            ("impact", "cyberpunk"),
            ("texture", "emerald")
        ]
        
        for scene, expected_palette in test_scenes:
            print(f"\n🎭 Scene: {scene}")
            
            # Low metrics.link
            palette_low = self.get_palette_for_scene(scene, 0.3)
            result_low = self.transform_with_scene(text, scene, 0.3, seed=1337)
            print(f"   Low link (0.3): {palette_low} → {result_low['text']}")
            
            # High metrics.link
            palette_high = self.get_palette_for_scene(scene, 0.8)
            result_high = self.transform_with_scene(text, scene, 0.8, seed=1337)
            print(f"   High link (0.8): {palette_high} → {result_high['text']}")
            
            # Check if bias applied correctly
            if palette_low != palette_high:
                print(f"   ✅ Bias applied: {palette_low} → {palette_high}")
            else:
                print(f"   ℹ️  No bias needed: {palette_low}")
                
    def demo_copper_palette(self, text="Copper Palette Demo"):
        """Demo the new copper palette"""
        print("😺 Copper Palette Demo...")
        
        result = lolcat_plus(text, emoji_palette="copper", seed=1337)
        print(f"   Copper: {result['text']}")
        
        # Show copper emojis
        copper_emojis = EMOJI_PALETTES["copper"]
        print(f"   Copper emojis: {' '.join(copper_emojis)}")
        
    def get_available_palettes(self):
        """Get list of available palettes"""
        return list(EMOJI_PALETTES.keys())
        
    def get_scene_mapping(self):
        """Get scene → palette mapping"""
        return self.scene_palette_map.copy()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="LOLcat++ Palette Autoselect by Scene")
    parser.add_argument("--demo", action="store_true", help="Demo scene palette mapping")
    parser.add_argument("--test-bias", action="store_true", help="Test metrics link bias")
    parser.add_argument("--copper", action="store_true", help="Demo copper palette")
    parser.add_argument("--scene", default="warmup", help="Scene name")
    parser.add_argument("--metrics-link", type=float, default=0.5, help="Metrics link value")
    parser.add_argument("--text", default="Palette autoselect test", help="Text to transform")
    
    args = parser.parse_args()
    
    autoselect = LOLcatPaletteAutoselect()
    
    if args.demo:
        autoselect.demo_scene_palette_mapping(args.text)
    elif args.test_bias:
        autoselect.test_metrics_link_bias(args.text)
    elif args.copper:
        autoselect.demo_copper_palette(args.text)
    else:
        # Single scene test
        result = autoselect.transform_with_scene(args.text, args.scene, args.metrics_link, seed=1337)
        print(f"😺 Result: {result['text']}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
LOLcat++ Emoji Palette by Scene Theme - Auto-swap emojis based on scene
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string_fx.lolcat_plus import lolcat_plus, EMOJI_PALETTES

class LOLcatEmojiPalette:
    def __init__(self):
        self.current_scene = "default"
        self.scene_emoji_map = {
            "moonlight-sonata": "vintage",
            "clair-de-lune": "emerald", 
            "lunar-recital": "gold",
            "cyberpunk": "cyberpunk",
            "neon-bloom": "neon",
            "data-storm": "cyberpunk",
            "glass-cathedral": "emerald",
            "default": "default"
        }
        
    def set_scene(self, scene_name):
        """Set current scene and auto-swap emoji palette"""
        self.current_scene = scene_name
        emoji_palette = self.scene_emoji_map.get(scene_name, "default")
        print(f"😺 Scene: {scene_name} → Emoji Palette: {emoji_palette}")
        return emoji_palette
        
    def get_available_palettes(self):
        """Get list of available emoji palettes"""
        return list(EMOJI_PALETTES.keys())
        
    def get_palette_emojis(self, palette_name):
        """Get emojis for a specific palette"""
        return EMOJI_PALETTES.get(palette_name, EMOJI_PALETTES["default"])
        
    def transform_with_scene(self, text, scene_name, **kwargs):
        """Transform text with scene-specific emoji palette"""
        emoji_palette = self.set_scene(scene_name)
        return lolcat_plus(text, emoji_palette=emoji_palette, **kwargs)
        
    def demo_palettes(self, text="Emoji Palette Demo"):
        """Demo all emoji palettes"""
        print("😺 LOLcat++ Emoji Palette Demo")
        print("=" * 50)
        
        for palette_name, emojis in EMOJI_PALETTES.items():
            print(f"\n🎨 {palette_name.upper()} Palette:")
            print(f"   Emojis: {' '.join(emojis[:5])}{'...' if len(emojis) > 5 else ''}")
            
            result = lolcat_plus(text, emoji_palette=palette_name, seed=1337)
            print(f"   Result: {result['text']}")
            
    def demo_scene_switching(self, text="Scene Switching Demo"):
        """Demo scene-based emoji switching"""
        print("😺 LOLcat++ Scene Switching Demo")
        print("=" * 50)
        
        scenes = ["moonlight-sonata", "clair-de-lune", "cyberpunk", "neon-bloom", "default"]
        
        for scene in scenes:
            result = self.transform_with_scene(text, scene, seed=1337)
            print(f"🎭 {scene}: {result['text']}")
            
    def test_palette_consistency(self, text="Consistency Test"):
        """Test that same scene + seed produces consistent results"""
        print("😺 Testing Palette Consistency...")
        
        # Test same scene + seed multiple times
        results = []
        for i in range(3):
            result = self.transform_with_scene(text, "cyberpunk", seed=42)
            results.append(result['text'])
            
        # Check consistency
        if len(set(results)) == 1:
            print("✅ Consistent results across runs")
        else:
            print("❌ Inconsistent results:")
            for i, result in enumerate(results):
                print(f"   Run {i+1}: {result}")
                
        print(f"🎨 Cyberpunk result: {results[0]}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="LOLcat++ Emoji Palette by Scene")
    parser.add_argument("--demo", action="store_true", help="Demo all palettes")
    parser.add_argument("--scenes", action="store_true", help="Demo scene switching")
    parser.add_argument("--test", action="store_true", help="Test consistency")
    parser.add_argument("--scene", default="default", help="Scene name")
    parser.add_argument("--text", default="Emoji palette test", help="Text to transform")
    parser.add_argument("--palette", help="Specific palette to use")
    
    args = parser.parse_args()
    
    palette_system = LOLcatEmojiPalette()
    
    if args.demo:
        palette_system.demo_palettes(args.text)
    elif args.scenes:
        palette_system.demo_scene_switching(args.text)
    elif args.test:
        palette_system.test_palette_consistency(args.text)
    else:
        if args.palette:
            result = lolcat_plus(args.text, emoji_palette=args.palette, seed=1337)
            print(f"😺 {args.palette} palette: {result['text']}")
        else:
            result = palette_system.transform_with_scene(args.text, args.scene, seed=1337)
            print(f"😺 Scene {args.scene}: {result['text']}")

if __name__ == "__main__":
    main()

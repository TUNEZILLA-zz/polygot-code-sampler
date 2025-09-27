#!/usr/bin/env python3
"""
LOLcat++ Preset A/B + Morph - Crossfade between two presets
"""
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string_fx.lolcat_plus import lolcat_plus

class LOLcatPresetAB:
    def __init__(self):
        self.preset_a = None
        self.preset_b = None
        self.current_preset = None
        self.morph_duration = 2.0  # seconds
        self.morph_start_time = 0
        self.is_morphing = False
        
        # Preset definitions
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
        
    def set_preset_a(self, preset_name):
        """Set preset A"""
        if preset_name in self.presets:
            self.preset_a = preset_name
            print(f"😺 Preset A set to: {preset_name}")
        else:
            print(f"Unknown preset: {preset_name}")
            
    def set_preset_b(self, preset_name):
        """Set preset B"""
        if preset_name in self.presets:
            self.preset_b = preset_name
            print(f"😺 Preset B set to: {preset_name}")
        else:
            print(f"Unknown preset: {preset_name}")
            
    def morph_to_b(self, duration=2.0):
        """Morph from A to B"""
        if not self.preset_a or not self.preset_b:
            print("😺 Error: Both preset A and B must be set")
            return
            
        self.morph_duration = duration
        self.morph_start_time = time.time()
        self.is_morphing = True
        print(f"😺 Morphing from {self.preset_a} to {self.preset_b} over {duration}s...")
        
    def morph_to_a(self, duration=2.0):
        """Morph from B to A"""
        if not self.preset_a or not self.preset_b:
            print("😺 Error: Both preset A and B must be set")
            return
            
        self.morph_duration = duration
        self.morph_start_time = time.time()
        self.is_morphing = True
        print(f"😺 Morphing from {self.preset_b} to {self.preset_a} over {duration}s...")
        
    def get_current_params(self):
        """Get current parameters (morphed if morphing)"""
        if not self.preset_a or not self.preset_b:
            return None
            
        if self.is_morphing:
            # Calculate morph progress (0.0 to 1.0)
            elapsed = time.time() - self.morph_start_time
            progress = min(elapsed / self.morph_duration, 1.0)
            
            # EaseInOut curve
            if progress < 0.5:
                ease = 2 * progress * progress
            else:
                ease = 1 - 2 * (1 - progress) * (1 - progress)
                
            # Interpolate between presets
            params_a = self.presets[self.preset_a]
            params_b = self.presets[self.preset_b]
            
            morphed_params = {}
            for key in params_a:
                if key in params_b:
                    morphed_params[key] = params_a[key] + (params_b[key] - params_a[key]) * ease
                else:
                    morphed_params[key] = params_a[key]
                    
            # Check if morph is complete
            if progress >= 1.0:
                self.is_morphing = False
                self.current_preset = self.preset_b
                print(f"😺 Morph complete! Now using {self.preset_b}")
                
            return morphed_params
        else:
            # Return current preset
            current = self.current_preset or self.preset_a
            return self.presets[current]
            
    def transform_text(self, text, seed=1337):
        """Transform text with current parameters"""
        params = self.get_current_params()
        if not params:
            return {"text": text, "ansi": text, "meta": {}}
            
        result = lolcat_plus(text, seed=seed, **params)
        return result
        
    def demo_ab_morph(self, text="A/B Morph Demo"):
        """Demo A/B morphing"""
        print("😺 Starting LOLcat++ A/B Morph Demo...")
        print("Press Ctrl+C to stop")
        
        # Set up presets
        self.set_preset_a("classic")
        self.set_preset_b("stage-punch")
        
        try:
            while True:
                # Show current state
                if self.is_morphing:
                    elapsed = time.time() - self.morph_start_time
                    progress = min(elapsed / self.morph_duration, 1.0)
                    print(f"\r😺 Morphing... {progress:.1%}", end="")
                else:
                    current = self.current_preset or self.preset_a
                    print(f"\r😺 Current: {current}", end="")
                
                # Transform text
                result = self.transform_text(text)
                print(f" | {result['text']}")
                
                # Auto-morph every 5 seconds
                if not self.is_morphing and int(time.time()) % 5 == 0:
                    if self.current_preset == self.preset_a:
                        self.morph_to_b(2.0)
                    else:
                        self.morph_to_a(2.0)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n😺 A/B Morph demo stopped")
            
    def quick_ab_test(self, text="Quick A/B Test"):
        """Quick A/B test between two presets"""
        print("😺 Quick A/B Test:")
        
        # Set up presets
        self.set_preset_a("classic")
        self.set_preset_b("stage-punch")
        
        # Test A
        self.current_preset = self.preset_a
        result_a = self.transform_text(text)
        print(f"😺 Preset A ({self.preset_a}): {result_a['text']}")
        
        # Test B
        self.current_preset = self.preset_b
        result_b = self.transform_text(text)
        print(f"😺 Preset B ({self.preset_b}): {result_b['text']}")
        
        # Morph demo
        print("😺 Morphing A → B...")
        self.morph_to_b(2.0)
        time.sleep(2.5)  # Wait for morph to complete
        result_morph = self.transform_text(text)
        print(f"😺 Morphed: {result_morph['text']}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="LOLcat++ Preset A/B + Morph")
    parser.add_argument("--demo", action="store_true", help="Run A/B morph demo")
    parser.add_argument("--test", action="store_true", help="Quick A/B test")
    parser.add_argument("--text", default="A/B Morph Test", help="Text to transform")
    parser.add_argument("--preset-a", default="classic", help="Preset A name")
    parser.add_argument("--preset-b", default="stage-punch", help="Preset B name")
    parser.add_argument("--morph-duration", type=float, default=2.0, help="Morph duration in seconds")
    
    args = parser.parse_args()
    
    ab = LOLcatPresetAB()
    
    if args.demo:
        ab.demo_ab_morph(args.text)
    elif args.test:
        ab.quick_ab_test(args.text)
    else:
        # Set presets and morph
        ab.set_preset_a(args.preset_a)
        ab.set_preset_b(args.preset_b)
        ab.morph_to_b(args.morph_duration)
        
        # Show result
        result = ab.transform_text(args.text)
        print(f"😺 A/B Result: {result['text']}")

if __name__ == "__main__":
    main()

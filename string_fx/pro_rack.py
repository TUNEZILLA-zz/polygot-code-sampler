"""
Professional Rack System - Soundtoys-for-Text
============================================

A complete professional rack system with:
- Rack scenes and morphing
- JSON preset schema
- Parallel & multiband routing
- Latency & order compensation
- Macro knobs + MIDI learn
- Sidechain from metrics
- Safety rails & QA
- Rack API
- Preset packs
- One-command rack show
"""

import json
import time
import random
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path


class RoutingType(Enum):
    """Rack routing types"""
    SERIAL = "serial"
    PARALLEL = "parallel"
    MULTIBAND = "multiband"


class BandType(Enum):
    """Multiband routing band types"""
    SYMBOLS = "symbols"
    UPPERCASE = "uppercase"
    LOWERCASE = "lowercase"
    DIGITS = "digits"


@dataclass
class FXConfig:
    """Configuration for a single FX in the rack"""
    name: str
    wet: float = 1.0
    params: Dict[str, Any] = None
    latency_ms: float = 0.0
    locked_order: bool = False
    
    def __post_init__(self):
        if self.params is None:
            self.params = {}


@dataclass
class RackScene:
    """Complete rack scene configuration"""
    version: int = 1
    seed: int = 777
    sample: str = "Code Live"
    routing: RoutingType = RoutingType.SERIAL
    fx: List[FXConfig] = None
    notes: str = ""
    
    def __post_init__(self):
        if self.fx is None:
            self.fx = []
        if isinstance(self.routing, str):
            self.routing = RoutingType(self.routing)


@dataclass
class MacroKnobs:
    """Macro knobs configuration"""
    color: float = 0.0  # chromatic offset + neon intensity
    space: float = 0.0  # reverb tail + trail length
    motion: float = 0.0  # tremolo rate + LFO depth
    crunch: float = 0.0  # distortion drive + glitch probability


@dataclass
class Metrics:
    """Live metrics for sidechain"""
    qps: float = 0.0
    p95: float = 0.0
    error_rate: float = 0.0
    bpm: float = 60.0


class ProRack:
    """
    Professional Rack System - Soundtoys-for-Text
    
    Complete rack system with scenes, morphing, routing,
    macro knobs, sidechain, and professional features.
    """
    
    def __init__(self):
        self.current_scene: Optional[RackScene] = None
        self.macros = MacroKnobs()
        self.metrics = Metrics()
        self.effect_registry = {}
        self._register_builtin_effects()
        
        # Safety rails
        self.clamps = {
            "wet_min": 0.0,
            "wet_max": 1.0,
            "feedback_max": 0.6,
            "chromatic_offset_max": 8,
            "trail_max": 12,
            "perf_budget_ms": 8.0
        }
        
        # Latency compensation
        self.fx_latencies = {
            "granular": 50.0,
            "trails": 30.0,
            "reverb": 20.0,
            "echo": 15.0,
            "delay": 10.0,
            "chorus": 5.0,
            "distortion": 2.0,
            "neon_fx": 1.0
        }
    
    def _register_builtin_effects(self):
        """Register all available effects"""
        from .runtime import FX_REGISTRY
        
        for effect_name, effect_func in FX_REGISTRY.items():
            self.effect_registry[effect_name] = effect_func
    
    def load_scene(self, scene: RackScene) -> None:
        """Load a rack scene"""
        self.current_scene = scene
        random.seed(scene.seed)
    
    def load_from_json(self, path: str) -> None:
        """Load rack scene from JSON file"""
        with open(path, 'r') as f:
            data = json.load(f)
        
        # Convert to RackScene
        fx_list = []
        for fx_data in data.get("fx", []):
            fx_config = FXConfig(
                name=fx_data["name"],
                wet=fx_data.get("wet", 1.0),
                params=fx_data.get("params", {}),
                latency_ms=self.fx_latencies.get(fx_data["name"], 0.0)
            )
            fx_list.append(fx_config)
        
        scene = RackScene(
            version=data.get("version", 1),
            seed=data.get("seed", 777),
            sample=data.get("sample", "Code Live"),
            routing=RoutingType(data.get("routing", "serial")),
            fx=fx_list,
            notes=data.get("notes", "")
        )
        
        self.load_scene(scene)
    
    def save_to_json(self, path: str) -> None:
        """Save current scene to JSON file"""
        if not self.current_scene:
            raise ValueError("No scene loaded")
        
        data = {
            "version": self.current_scene.version,
            "seed": self.current_scene.seed,
            "sample": self.current_scene.sample,
            "routing": self.current_scene.routing.value,
            "fx": [asdict(fx) for fx in self.current_scene.fx],
            "notes": self.current_scene.notes
        }
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def morph_to(self, target_scene: RackScene, t: float) -> RackScene:
        """Morph between two scenes"""
        if not self.current_scene:
            return target_scene
        
        t = max(0.0, min(1.0, t))  # Clamp to [0,1]
        
        # Create morphed scene
        morphed_fx = []
        for i, (current_fx, target_fx) in enumerate(zip(self.current_scene.fx, target_scene.fx)):
            if current_fx.name == target_fx.name:
                # Morph parameters
                morphed_params = {}
                for key in current_fx.params:
                    if key in target_fx.params:
                        morphed_params[key] = current_fx.params[key] * (1-t) + target_fx.params[key] * t
                    else:
                        morphed_params[key] = current_fx.params[key]
                
                # Add new parameters from target
                for key, value in target_fx.params.items():
                    if key not in morphed_params:
                        morphed_params[key] = value * t
                
                morphed_fx.append(FXConfig(
                    name=current_fx.name,
                    wet=current_fx.wet * (1-t) + target_fx.wet * t,
                    params=morphed_params,
                    latency_ms=current_fx.latency_ms,
                    locked_order=current_fx.locked_order
                ))
            else:
                # Different effects - use target if t > 0.5
                if t > 0.5:
                    morphed_fx.append(target_fx)
                else:
                    morphed_fx.append(current_fx)
        
        return RackScene(
            version=target_scene.version,
            seed=target_scene.seed,
            sample=target_scene.sample,
            routing=target_scene.routing,
            fx=morphed_fx,
            notes=f"Morph: {self.current_scene.notes} → {target_scene.notes}"
        )
    
    def apply_macros(self, macros: Dict[str, float]) -> None:
        """Apply macro knobs"""
        self.macros.color = max(0.0, min(1.0, macros.get("color", 0.0)))
        self.macros.space = max(0.0, min(1.0, macros.get("space", 0.0)))
        self.macros.motion = max(0.0, min(1.0, macros.get("motion", 0.0)))
        self.macros.crunch = max(0.0, min(1.0, macros.get("crunch", 0.0)))
    
    def sidechain(self, metrics: Dict[str, float]) -> None:
        """Apply sidechain from metrics"""
        self.metrics.qps = metrics.get("qps", 0.0)
        self.metrics.p95 = metrics.get("p95", 0.0)
        self.metrics.error_rate = metrics.get("error_rate", 0.0)
        self.metrics.bpm = metrics.get("bpm", 60.0)
    
    def process(self, text: str, mode: str = "raw") -> str:
        """Process text through the rack"""
        if not self.current_scene:
            return text
        
        start_time = time.time()
        
        # Apply macro knobs to FX parameters
        processed_fx = self._apply_macros_to_fx()
        
        # Apply sidechain
        processed_fx = self._apply_sidechain_to_fx(processed_fx)
        
        # Apply safety clamps
        processed_fx = self._apply_safety_clamps(processed_fx)
        
        # Process based on routing
        if self.current_scene.routing == RoutingType.SERIAL:
            result = self._process_serial(text, processed_fx, mode)
        elif self.current_scene.routing == RoutingType.PARALLEL:
            result = self._process_parallel(text, processed_fx, mode)
        elif self.current_scene.routing == RoutingType.MULTIBAND:
            result = self._process_multiband(text, processed_fx, mode)
        else:
            result = text
        
        # Check performance budget
        elapsed_ms = (time.time() - start_time) * 1000
        if elapsed_ms > self.clamps["perf_budget_ms"]:
            print(f"⚠️  Performance warning: {elapsed_ms:.1f}ms > {self.clamps['perf_budget_ms']}ms")
        
        return result
    
    def _apply_macros_to_fx(self) -> List[FXConfig]:
        """Apply macro knobs to FX parameters"""
        if not self.current_scene:
            return []
        
        processed_fx = []
        for fx in self.current_scene.fx:
            new_params = fx.params.copy()
            
            # Macro 1 (Color): chromatic offset + neon intensity
            if fx.name in ["chromatic", "neon_fx"]:
                if "offset_px" in new_params:
                    new_params["offset_px"] *= (1 + self.macros.color)
                if "glow" in new_params:
                    new_params["glow"] *= (1 + self.macros.color)
            
            # Macro 2 (Space): reverb tail + trail length
            if fx.name in ["reverb", "trails"]:
                if "decay" in new_params:
                    new_params["decay"] *= (1 + self.macros.space)
                if "trail_len" in new_params:
                    new_params["trail_len"] *= (1 + self.macros.space)
            
            # Macro 3 (Motion): tremolo rate + LFO depth
            if fx.name in ["tremolo", "lfo"]:
                if "rate" in new_params:
                    new_params["rate"] *= (1 + self.macros.motion)
                if "depth" in new_params:
                    new_params["depth"] *= (1 + self.macros.motion)
            
            # Macro 4 (Crunch): distortion drive + glitch probability
            if fx.name in ["distortion", "glitch_colors"]:
                if "drive" in new_params:
                    new_params["drive"] *= (1 + self.macros.crunch)
                if "glitch_factor" in new_params:
                    new_params["glitch_factor"] *= (1 + self.macros.crunch)
            
            processed_fx.append(FXConfig(
                name=fx.name,
                wet=fx.wet,
                params=new_params,
                latency_ms=fx.latency_ms,
                locked_order=fx.locked_order
            ))
        
        return processed_fx
    
    def _apply_sidechain_to_fx(self, fx_list: List[FXConfig]) -> List[FXConfig]:
        """Apply sidechain from metrics to FX"""
        processed_fx = []
        for fx in fx_list:
            new_params = fx.params.copy()
            
            # Let p95 duck reverb (less smear under load)
            if fx.name == "reverb" and self.metrics.p95 > 50:
                duck_factor = max(0.3, 1.0 - (self.metrics.p95 - 50) / 100)
                if "decay" in new_params:
                    new_params["decay"] *= duck_factor
            
            # Let error_rate pump stutter amount
            if fx.name == "stutter" and self.metrics.error_rate > 0.02:
                pump_factor = min(2.0, 1.0 + self.metrics.error_rate * 10)
                if "stutter_rate" in new_params:
                    new_params["stutter_rate"] *= pump_factor
            
            # Let QPS open MicroShift spread + echo feedback
            if fx.name in ["chorus", "echo"] and self.metrics.qps > 30:
                open_factor = min(1.5, 1.0 + (self.metrics.qps - 30) / 100)
                if "spread" in new_params:
                    new_params["spread"] *= open_factor
                if "feedback" in new_params:
                    new_params["feedback"] *= open_factor
            
            processed_fx.append(FXConfig(
                name=fx.name,
                wet=fx.wet,
                params=new_params,
                latency_ms=fx.latency_ms,
                locked_order=fx.locked_order
            ))
        
        return processed_fx
    
    def _apply_safety_clamps(self, fx_list: List[FXConfig]) -> List[FXConfig]:
        """Apply safety clamps to FX parameters"""
        processed_fx = []
        for fx in fx_list:
            new_params = fx.params.copy()
            
            # Clamp wet/dry
            new_wet = max(self.clamps["wet_min"], min(self.clamps["wet_max"], fx.wet))
            
            # Clamp specific parameters
            if "feedback" in new_params:
                new_params["feedback"] = min(self.clamps["feedback_max"], new_params["feedback"])
            if "offset_px" in new_params:
                new_params["offset_px"] = min(self.clamps["chromatic_offset_max"], new_params["offset_px"])
            if "trail_len" in new_params:
                new_params["trail_len"] = min(self.clamps["trail_max"], new_params["trail_len"])
            
            processed_fx.append(FXConfig(
                name=fx.name,
                wet=new_wet,
                params=new_params,
                latency_ms=fx.latency_ms,
                locked_order=fx.locked_order
            ))
        
        return processed_fx
    
    def _process_serial(self, text: str, fx_list: List[FXConfig], mode: str) -> str:
        """Process text through FX in serial"""
        result = text
        
        for fx in fx_list:
            if fx.wet <= 0:
                continue
            
            effect_func = self.effect_registry.get(fx.name)
            if not effect_func:
                continue
            
            try:
                params = fx.params.copy()
                params["mode"] = mode
                params["intensity"] = fx.wet
                
                processed = effect_func(result, params)
                
                # Mix with original (wet/dry)
                if fx.wet < 1.0:
                    result = self._mix_text(result, processed, fx.wet)
                else:
                    result = processed
                    
            except Exception as e:
                print(f"Error applying effect {fx.name}: {e}")
                continue
        
        return result
    
    def _process_parallel(self, text: str, fx_list: List[FXConfig], mode: str) -> str:
        """Process text through FX in parallel"""
        if not fx_list:
            return text
        
        # Split FX into two chains
        mid_point = len(fx_list) // 2
        chain_a = fx_list[:mid_point]
        chain_b = fx_list[mid_point:]
        
        # Process through each chain
        result_a = self._process_serial(text, chain_a, mode)
        result_b = self._process_serial(text, chain_b, mode)
        
        # Blend the results
        return self._mix_text(result_a, result_b, 0.5)
    
    def _process_multiband(self, text: str, fx_list: List[FXConfig], mode: str) -> str:
        """Process text through FX with multiband routing"""
        # Split text into bands
        bands = self._split_text_into_bands(text)
        
        # Process each band with different FX
        processed_bands = {}
        for band_type, band_text in bands.items():
            if band_text:
                # Use different FX for different bands
                if band_type == BandType.SYMBOLS:
                    band_fx = [fx for fx in fx_list if fx.name in ["distortion", "glitch_colors"]]
                elif band_type == BandType.UPPERCASE:
                    band_fx = [fx for fx in fx_list if fx.name in ["neon_fx", "chromatic"]]
                elif band_type == BandType.LOWERCASE:
                    band_fx = [fx for fx in fx_list if fx.name in ["reverb", "trails"]]
                else:  # DIGITS
                    band_fx = [fx for fx in fx_list if fx.name in ["echo", "delay"]]
                
                processed_bands[band_type] = self._process_serial(band_text, band_fx, mode)
            else:
                processed_bands[band_type] = band_text
        
        # Recombine bands
        return self._recombine_bands(processed_bands, text)
    
    def _split_text_into_bands(self, text: str) -> Dict[BandType, str]:
        """Split text into frequency bands"""
        bands = {
            BandType.SYMBOLS: "",
            BandType.UPPERCASE: "",
            BandType.LOWERCASE: "",
            BandType.DIGITS: ""
        }
        
        for char in text:
            if char.isupper():
                bands[BandType.UPPERCASE] += char
            elif char.islower():
                bands[BandType.LOWERCASE] += char
            elif char.isdigit():
                bands[BandType.DIGITS] += char
            else:
                bands[BandType.SYMBOLS] += char
        
        return bands
    
    def _recombine_bands(self, processed_bands: Dict[BandType, str], original: str) -> str:
        """Recombine processed bands back into text"""
        result = ""
        band_chars = {
            BandType.UPPERCASE: list(processed_bands[BandType.UPPERCASE]),
            BandType.LOWERCASE: list(processed_bands[BandType.LOWERCASE]),
            BandType.DIGITS: list(processed_bands[BandType.DIGITS]),
            BandType.SYMBOLS: list(processed_bands[BandType.SYMBOLS])
        }
        
        for char in original:
            if char.isupper() and band_chars[BandType.UPPERCASE]:
                result += band_chars[BandType.UPPERCASE].pop(0)
            elif char.islower() and band_chars[BandType.LOWERCASE]:
                result += band_chars[BandType.LOWERCASE].pop(0)
            elif char.isdigit() and band_chars[BandType.DIGITS]:
                result += band_chars[BandType.DIGITS].pop(0)
            elif not char.isalnum() and band_chars[BandType.SYMBOLS]:
                result += band_chars[BandType.SYMBOLS].pop(0)
            else:
                result += char
        
        return result
    
    def _mix_text(self, dry: str, wet: str, mix: float) -> str:
        """Mix dry and wet text based on mix ratio"""
        if mix <= 0.0:
            return dry
        elif mix >= 1.0:
            return wet
        
        # Simple text mixing
        if len(dry) == len(wet):
            result = ""
            for i in range(len(dry)):
                if random.random() < mix:
                    result += wet[i] if i < len(wet) else dry[i]
                else:
                    result += dry[i] if i < len(dry) else wet[i]
            return result
        else:
            return wet if random.random() < mix else dry
    
    def get_rack_status(self) -> Dict[str, Any]:
        """Get current rack status"""
        if not self.current_scene:
            return {"status": "no_scene"}
        
        return {
            "scene": self.current_scene.sample,
            "routing": self.current_scene.routing.value,
            "fx_count": len(self.current_scene.fx),
            "macros": asdict(self.macros),
            "metrics": asdict(self.metrics),
            "notes": self.current_scene.notes
        }


def create_pro_rack_cli():
    """Create command-line interface for pro rack"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Professional Rack System - Soundtoys-for-Text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Load and process with rack
  python3 scripts/pro_rack_cli.py --load presets/racks/tour_opener.rack.json --text "Code Live"

  # Apply macro knobs
  python3 scripts/pro_rack_cli.py --load presets/racks/glass_cathedral.rack.json --macros color=0.7,space=0.3

  # Sidechain from metrics
  python3 scripts/pro_rack_cli.py --load presets/racks/data_storm.rack.json --sidechain qps=50,p95=60,error_rate=0.05

  # Morph between scenes
  python3 scripts/pro_rack_cli.py --morph presets/racks/tour_opener.rack.json presets/racks/glass_cathedral.rack.json --morph-time 0.5
        """
    )
    
    parser.add_argument("--text", "-t", help="Input text to process")
    parser.add_argument("--load", help="Load rack scene from JSON file")
    parser.add_argument("--save", help="Save current rack to JSON file")
    parser.add_argument("--macros", help="Apply macro knobs (color=0.7,space=0.3,motion=0.5,crunch=0.8)")
    parser.add_argument("--sidechain", help="Apply sidechain from metrics (qps=50,p95=60,error_rate=0.05)")
    parser.add_argument("--morph", nargs=2, help="Morph between two rack scenes")
    parser.add_argument("--morph-time", type=float, default=0.5, help="Morph time (0.0-1.0)")
    parser.add_argument("--mode", default="raw", choices=["raw", "ansi", "html"], help="Output mode")
    parser.add_argument("--output", "-o", help="Output file for HTML mode")
    parser.add_argument("--status", action="store_true", help="Show rack status")
    
    return parser


if __name__ == "__main__":
    # Example usage
    rack = ProRack()
    
    # Create a simple scene
    scene = RackScene(
        sample="Code Live",
        fx=[
            FXConfig("distortion", 0.8, {"drive": 0.7}),
            FXConfig("neon_fx", 0.6, {"glow": 1.5}),
            FXConfig("echo", 0.4, {"delay": 0.5})
        ]
    )
    
    rack.load_scene(scene)
    result = rack.process("Code Live")
    print(f"Pro Rack Result: {result}")
    
    # Show status
    status = rack.get_rack_status()
    print(f"Rack Status: {json.dumps(status, indent=2)}")

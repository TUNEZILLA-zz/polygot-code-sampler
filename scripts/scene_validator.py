#!/usr/bin/env python3
"""
Scene JSON Validator - Pre-flight Safety Check
==============================================

Validates scene JSON files for safety, performance, and compliance.
"""

import json
import sys
import os
from typing import Dict, List, Any, Tuple
from pathlib import Path


class SceneValidator:
    """
    Scene JSON Validator
    
    Validates scene JSON files for:
    - Duration limits
    - Intensity limits
    - Strobe safety
    - A11y compliance
    - Performance constraints
    """
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.safety_rules = {
            "morph_duration_min": 0.3,
            "morph_duration_max": 6.0,
            "scene_duration_min": 5.0,
            "scene_duration_max": 60.0,
            "intensity_max": 1.0,
            "strobe_hz_max": 8.0,
            "strobe_on_time_min_ms": 120.0,
            "duty_cycle_max": 0.35
        }
    
    def validate_scene(self, scene_data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """Validate a single scene"""
        self.errors = []
        self.warnings = []
        
        # Check required fields
        self._check_required_fields(scene_data)
        
        # Check duration limits
        self._check_duration_limits(scene_data)
        
        # Check intensity limits
        self._check_intensity_limits(scene_data)
        
        # Check strobe safety
        self._check_strobe_safety(scene_data)
        
        # Check A11y compliance
        self._check_a11y_compliance(scene_data)
        
        # Check performance constraints
        self._check_performance_constraints(scene_data)
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _check_required_fields(self, scene_data: Dict[str, Any]) -> None:
        """Check required fields are present"""
        required_fields = ["id", "seed", "routing", "fx"]
        
        for field in required_fields:
            if field not in scene_data:
                self.errors.append(f"Missing required field: {field}")
    
    def _check_duration_limits(self, scene_data: Dict[str, Any]) -> None:
        """Check duration limits"""
        # Check morph durations
        if "morph" in scene_data:
            morph_duration = scene_data["morph"]
            if isinstance(morph_duration, (int, float)):
                if morph_duration < self.safety_rules["morph_duration_min"]:
                    self.errors.append(f"Morph duration too short: {morph_duration}s < {self.safety_rules['morph_duration_min']}s")
                elif morph_duration > self.safety_rules["morph_duration_max"]:
                    self.errors.append(f"Morph duration too long: {morph_duration}s > {self.safety_rules['morph_duration_max']}s")
        
        # Check scene duration
        if "duration" in scene_data:
            duration = scene_data["duration"]
            if isinstance(duration, (int, float)):
                if duration < self.safety_rules["scene_duration_min"]:
                    self.errors.append(f"Scene duration too short: {duration}s < {self.safety_rules['scene_duration_min']}s")
                elif duration > self.safety_rules["scene_duration_max"]:
                    self.errors.append(f"Scene duration too long: {duration}s > {self.safety_rules['scene_duration_max']}s")
    
    def _check_intensity_limits(self, scene_data: Dict[str, Any]) -> None:
        """Check intensity limits"""
        # Check scene intensity
        if "intensity" in scene_data:
            intensity = scene_data["intensity"]
            if isinstance(intensity, (int, float)):
                if intensity > self.safety_rules["intensity_max"]:
                    if not scene_data.get("allow_boost", False):
                        self.errors.append(f"Scene intensity too high: {intensity} > {self.safety_rules['intensity_max']} (requires allow_boost: true)")
                    else:
                        self.warnings.append(f"High intensity scene: {intensity} (boost allowed)")
        
        # Check FX intensity
        if "fx" in scene_data:
            for i, fx in enumerate(scene_data["fx"]):
                if isinstance(fx, dict) and "mix" in fx:
                    mix = fx["mix"]
                    if isinstance(mix, (int, float)) and mix > 1.0:
                        self.warnings.append(f"FX {i} mix > 1.0: {mix}")
    
    def _check_strobe_safety(self, scene_data: Dict[str, Any]) -> None:
        """Check strobe safety"""
        if "fx" in scene_data:
            for i, fx in enumerate(scene_data["fx"]):
                if isinstance(fx, dict) and fx.get("type") == "strobe":
                    # Check strobe frequency
                    if "rate_hz" in fx:
                        rate_hz = fx["rate_hz"]
                        if isinstance(rate_hz, (int, float)) and rate_hz > self.safety_rules["strobe_hz_max"]:
                            self.errors.append(f"Strobe frequency too high: {rate_hz}Hz > {self.safety_rules['strobe_hz_max']}Hz")
                    
                    # Check strobe on-time
                    if "on_time_ms" in fx:
                        on_time = fx["on_time_ms"]
                        if isinstance(on_time, (int, float)) and on_time < self.safety_rules["strobe_on_time_min_ms"]:
                            self.errors.append(f"Strobe on-time too short: {on_time}ms < {self.safety_rules['strobe_on_time_min_ms']}ms")
                    
                    # Check duty cycle
                    if "duty_cycle" in fx:
                        duty_cycle = fx["duty_cycle"]
                        if isinstance(duty_cycle, (int, float)) and duty_cycle > self.safety_rules["duty_cycle_max"]:
                            self.errors.append(f"Strobe duty cycle too high: {duty_cycle} > {self.safety_rules['duty_cycle_max']}")
    
    def _check_a11y_compliance(self, scene_data: Dict[str, Any]) -> None:
        """Check A11y compliance"""
        scene_id = scene_data.get("id", "unknown")
        
        # Check for required thumbnails
        required_thumbnails = ["mono", "motion_safe"]
        for variant in required_thumbnails:
            thumbnail_path = f"presets/scenes/{scene_id}-{variant}.png"
            if not os.path.exists(thumbnail_path):
                self.warnings.append(f"Missing A11y thumbnail: {thumbnail_path}")
        
        # Check for motion-reduced mode
        if "a11y" not in scene_data:
            self.warnings.append("Missing A11y configuration")
        else:
            a11y = scene_data["a11y"]
            if not a11y.get("motion_reduced", False):
                self.warnings.append("Motion-reduced mode not enabled")
    
    def _check_performance_constraints(self, scene_data: Dict[str, Any]) -> None:
        """Check performance constraints"""
        # Check FX count
        if "fx" in scene_data:
            fx_count = len(scene_data["fx"])
            if fx_count > 8:
                self.warnings.append(f"High FX count: {fx_count} (may impact performance)")
        
        # Check complex routing
        routing = scene_data.get("routing", "serial")
        if routing == "multiband":
            self.warnings.append("Multiband routing may impact performance")
        
        # Check sidechain complexity
        if "sidechain" in scene_data and scene_data["sidechain"].get("enabled", False):
            maps = scene_data["sidechain"].get("maps", [])
            if len(maps) > 5:
                self.warnings.append(f"High sidechain map count: {len(maps)} (may impact performance)")
    
    def validate_file(self, file_path: str) -> Tuple[bool, List[str], List[str]]:
        """Validate a scene JSON file"""
        try:
            with open(file_path, 'r') as f:
                scene_data = json.load(f)
            
            return self.validate_scene(scene_data)
        except json.JSONDecodeError as e:
            return False, [f"JSON decode error: {e}"], []
        except FileNotFoundError:
            return False, [f"File not found: {file_path}"], []
        except Exception as e:
            return False, [f"Validation error: {e}"], []
    
    def validate_directory(self, dir_path: str) -> Dict[str, Tuple[bool, List[str], List[str]]]:
        """Validate all scene JSON files in a directory"""
        results = {}
        
        for file_path in Path(dir_path).glob("*.json"):
            results[str(file_path)] = self.validate_file(str(file_path))
        
        return results


def main():
    """Main CLI function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Scene JSON Validator - Pre-flight Safety Check",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate single scene
  python3 scripts/scene_validator.py --file presets/scenes/tour_opener.json

  # Validate all scenes in directory
  python3 scripts/scene_validator.py --dir presets/scenes

  # Validate with strict mode
  python3 scripts/scene_validator.py --file presets/scenes/tour_opener.json --strict
        """
    )
    
    parser.add_argument("--file", help="Validate single scene file")
    parser.add_argument("--dir", help="Validate all scenes in directory")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--output", help="Output results to file")
    
    args = parser.parse_args()
    
    validator = SceneValidator()
    
    if args.file:
        # Validate single file
        success, errors, warnings = validator.validate_file(args.file)
        
        print(f"🔍 Validating: {args.file}")
        print(f"Status: {'✅ PASSED' if success else '❌ FAILED'}")
        
        if errors:
            print("\n❌ Errors:")
            for error in errors:
                print(f"  - {error}")
        
        if warnings:
            print("\n⚠️  Warnings:")
            for warning in warnings:
                print(f"  - {warning}")
        
        if args.strict and warnings:
            print("\n❌ Strict mode: Warnings treated as errors")
            success = False
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(f"Validation Results for {args.file}\n")
                f.write(f"Status: {'PASSED' if success else 'FAILED'}\n")
                f.write(f"Errors: {len(errors)}\n")
                f.write(f"Warnings: {len(warnings)}\n")
        
        sys.exit(0 if success else 1)
    
    elif args.dir:
        # Validate directory
        results = validator.validate_directory(args.dir)
        
        print(f"🔍 Validating directory: {args.dir}")
        print(f"Files found: {len(results)}")
        
        all_passed = True
        total_errors = 0
        total_warnings = 0
        
        for file_path, (success, errors, warnings) in results.items():
            print(f"\n📄 {file_path}")
            print(f"Status: {'✅ PASSED' if success else '❌ FAILED'}")
            
            if errors:
                print("❌ Errors:")
                for error in errors:
                    print(f"  - {error}")
                total_errors += len(errors)
            
            if warnings:
                print("⚠️  Warnings:")
                for warning in warnings:
                    print(f"  - {warning}")
                total_warnings += len(warnings)
            
            if args.strict and warnings:
                print("❌ Strict mode: Warnings treated as errors")
                success = False
            
            if not success:
                all_passed = False
        
        print(f"\n📊 Summary:")
        print(f"Total files: {len(results)}")
        print(f"Passed: {sum(1 for success, _, _ in results.values() if success)}")
        print(f"Failed: {sum(1 for success, _, _ in results.values() if not success)}")
        print(f"Total errors: {total_errors}")
        print(f"Total warnings: {total_warnings}")
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(f"Validation Results for {args.dir}\n")
                f.write(f"Total files: {len(results)}\n")
                f.write(f"Passed: {sum(1 for success, _, _ in results.values() if success)}\n")
                f.write(f"Failed: {sum(1 for success, _, _ in results.values() if not success)}\n")
                f.write(f"Total errors: {total_errors}\n")
                f.write(f"Total warnings: {total_warnings}\n")
        
        sys.exit(0 if all_passed else 1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

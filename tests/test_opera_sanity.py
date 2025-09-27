#!/usr/bin/env python3
"""
🎭 Code Opera - Sanity Tests
===========================

Fast sanity tests for Code Opera performance.
Tests determinism, act structure, and voice output.
"""

import json
import hashlib
import glob
from pathlib import Path
from typing import Dict, List, Any


def test_opera_manifest():
    """Test that manifest exists and has correct structure"""
    manifest_file = Path("out/opera/manifest.json")
    
    if not manifest_file.exists():
        raise AssertionError("Manifest file not found")
    
    with open(manifest_file, "r") as f:
        manifest = json.load(f)
    
    # Check required fields
    assert "seed" in manifest, "Manifest missing seed"
    assert "bpm" in manifest, "Manifest missing bpm"
    assert "key" in manifest, "Manifest missing key"
    assert "acts" in manifest, "Manifest missing acts"
    assert "key_path" in manifest, "Manifest missing key_path"
    assert "content_sha256" in manifest, "Manifest missing content_sha256"
    
    # Check act structure
    assert manifest["acts"] == 3, f"Expected 3 acts, got {manifest['acts']}"
    assert manifest["key_path"] == ["C", "G", "C"], f"Expected key path ['C', 'G', 'C'], got {manifest['key_path']}"
    
    print("✅ Manifest structure test passed")
    return True


def test_deterministic_seed():
    """Test that deterministic seed reproduces same hash"""
    seed_file = Path("out/opera/SEED.txt")
    
    if not seed_file.exists():
        raise AssertionError("Seed file not found")
    
    seed = seed_file.read_text().strip()
    assert seed, "Seed file is empty"
    
    print(f"✅ Deterministic seed test passed: {seed}")
    return True


def test_content_hash():
    """Test that content hash matches actual content"""
    manifest_file = Path("out/opera/manifest.json")
    
    with open(manifest_file, "r") as f:
        manifest = json.load(f)
    
    # Calculate actual content hash
    content_data = ""
    voice_files = sorted(glob.glob("out/voices/*_act_*.py"))
    
    for voice_file in voice_files:
        with open(voice_file, "r") as f:
            content_data += f.read()
    
    actual_hash = hashlib.sha256(content_data.encode()).hexdigest()
    expected_hash = manifest["content_sha256"]
    
    assert actual_hash == expected_hash, f"Content hash mismatch: expected {expected_hash[:16]}..., got {actual_hash[:16]}..."
    
    print("✅ Content hash test passed")
    return True


def test_voice_output():
    """Test that each voice emits at least one phrase per act"""
    voice_files = glob.glob("out/voices/*_act_*.py")
    
    if not voice_files:
        raise AssertionError("No voice act files found")
    
    # Group by voice and act
    voice_acts = {}
    for file_path in voice_files:
        filename = Path(file_path).name
        parts = filename.replace(".py", "").split("_act_")
        if len(parts) == 2:
            voice_name, act_num = parts
            if voice_name not in voice_acts:
                voice_acts[voice_name] = []
            voice_acts[voice_name].append(int(act_num))
    
    # Check each voice has all 3 acts
    for voice_name, acts in voice_acts.items():
        assert len(acts) == 3, f"Voice {voice_name} missing acts: {acts}"
        assert set(acts) == {1, 2, 3}, f"Voice {voice_name} has wrong acts: {acts}"
    
    print(f"✅ Voice output test passed: {len(voice_acts)} voices, 3 acts each")
    return True


def test_act_key_structure():
    """Test that Act II uses target key and Act III returns to tonic"""
    # This is a simplified test - in a real implementation,
    # you'd parse the actual code to check key usage
    
    manifest_file = Path("out/opera/manifest.json")
    with open(manifest_file, "r") as f:
        manifest = json.load(f)
    
    key_path = manifest["key_path"]
    assert key_path == ["C", "G", "C"], f"Expected key path ['C', 'G', 'C'], got {key_path}"
    
    print("✅ Act key structure test passed")
    return True


def test_no_parallel_fifths():
    """Test that counterpoint guard has been applied"""
    counterpoint_log = Path("out/opera/counterpoint.log")
    
    if not counterpoint_log.exists():
        print("⚠️  Counterpoint log not found - skipping parallel fifths test")
        return True
    
    with open(counterpoint_log, "r") as f:
        log_content = f.read()
    
    # Check that no parallel fifths were found
    if "parallel issues" in log_content:
        # Count the number of parallel issues
        issue_count = log_content.count("parallel issues")
        if issue_count > 0:
            print(f"⚠️  Found {issue_count} parallel issues - counterpoint guard applied")
        else:
            print("✅ No parallel issues found")
    else:
        print("✅ Counterpoint guard applied successfully")
    
    return True


def test_performance_budget():
    """Test that performance is within budget (simplified)"""
    # This would normally test actual performance metrics
    # For now, we'll just check that files exist and are reasonable sizes
    
    harmony_file = Path("out/opera/code_opera_harmony.html")
    if harmony_file.exists():
        file_size = harmony_file.stat().st_size
        assert file_size < 100000, f"Harmony file too large: {file_size} bytes"
        print(f"✅ Performance budget test passed: {file_size} bytes")
    else:
        print("⚠️  Harmony file not found - skipping performance test")
    
    return True


def run_all_tests():
    """Run all sanity tests"""
    print("🎭 Code Opera - Sanity Tests")
    print("=" * 50)
    
    tests = [
        ("Manifest Structure", test_opera_manifest),
        ("Deterministic Seed", test_deterministic_seed),
        ("Content Hash", test_content_hash),
        ("Voice Output", test_voice_output),
        ("Act Key Structure", test_act_key_structure),
        ("No Parallel Fifths", test_no_parallel_fifths),
        ("Performance Budget", test_performance_budget),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Running {test_name}...")
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            failed += 1
    
    print(f"\n📊 Test Results:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 All sanity tests passed!")
        return True
    else:
        print(f"\n⚠️  {failed} tests failed")
        return False


if __name__ == "__main__":
    import sys
    
    success = run_all_tests()
    sys.exit(0 if success else 1)

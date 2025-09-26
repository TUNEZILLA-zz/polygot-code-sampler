#!/usr/bin/env python3
"""
Generate automated validation report for CI/CD
Runs all enterprise features and outputs validation status
"""

import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime

def run_test(test_name, command, expected_exit_code=0):
    """Run a test and return results"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        success = result.returncode == expected_exit_code
        return {
            "test": test_name,
            "status": "✅ PASSED" if success else "❌ FAILED",
            "exit_code": result.returncode,
            "stdout": result.stdout[:200] if result.stdout else "",
            "stderr": result.stderr[:200] if result.stderr else ""
        }
    except subprocess.TimeoutExpired:
        return {
            "test": test_name,
            "status": "⏰ TIMEOUT",
            "exit_code": -1,
            "stdout": "",
            "stderr": "Test timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "test": test_name,
            "status": "❌ ERROR",
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e)[:200]
        }

def main():
    """Generate validation report"""
    print("🔍 Generating Enterprise Platform Validation Report")
    print("=" * 60)
    
    # Change to project directory
    project_root = Path(__file__).resolve().parents[1]
    
    # Check if we have demo data to determine which tests to run
    has_demo_data = False
    try:
        with open("site/benchmarks.json", "r") as f:
            data = json.load(f)
        has_demo_data = any(row.get("commit", "").startswith("demo-") for row in data)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    tests = [
        ("Policy Loading", "python3 scripts/policy_loader.py"),
        ("Demo Data Generation", "make demo-data"),
        ("Policy Schema Validation", "python3 -c \"import json, yaml, jsonschema; sch=json.load(open('bench/policy.schema.json')); pol=yaml.safe_load(open('bench/policy.yml')); jsonschema.validate(pol, sch); print('Schema OK')\""),
    ]
    
    # Add regression/anomaly tests only if we have real data (not demo)
    if not has_demo_data:
        tests.extend([
            ("Regression Check", "python3 scripts/regression_check.py --input site/benchmarks.json"),
            ("K-Anomaly Detection", "python3 scripts/k_anomaly_detector.py --input site/benchmarks.json --k-threshold 0.6"),
        ])
    else:
        print("⚠️  Demo data detected - skipping regression/anomaly tests")
    
    results = []
    for test_name, command in tests:
        print(f"🧪 Running {test_name}...")
        result = run_test(test_name, command)
        results.append(result)
        print(f"   {result['status']}")
    
    # Generate report
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "platform": "Enterprise Performance Monitoring",
        "version": "1.0",
        "tests": results,
        "summary": {
            "total": len(results),
            "passed": len([r for r in results if "✅" in r["status"]]),
            "failed": len([r for r in results if "❌" in r["status"]]),
            "timeout": len([r for r in results if "⏰" in r["status"]])
        }
    }
    
    # Write report
    report_file = project_root / "validation-report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n📊 Validation Summary")
    print("=" * 30)
    print(f"Total Tests: {report['summary']['total']}")
    print(f"✅ Passed: {report['summary']['passed']}")
    print(f"❌ Failed: {report['summary']['failed']}")
    print(f"⏰ Timeout: {report['summary']['timeout']}")
    print(f"\n📄 Report saved to: {report_file}")
    
    # Exit with error if any tests failed
    if report['summary']['failed'] > 0 or report['summary']['timeout'] > 0:
        print("\n❌ Some tests failed - check the report for details")
        sys.exit(1)
    else:
        print("\n🎉 All tests passed - Enterprise platform is operational!")
        sys.exit(0)

if __name__ == "__main__":
    main()

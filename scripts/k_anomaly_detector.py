#!/usr/bin/env python3
"""
K-Anomaly Detector

Detects days with simultaneous regressions across all backends,
indicating likely infrastructure issues (runner problems, toolchain changes, etc.)
rather than actual performance regressions.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Set
from collections import defaultdict
import statistics

def load_benchmark_data(file_path: Path) -> List[Dict[str, Any]]:
    """Load benchmark data from JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("benchmarks.json must be a JSON array")
        return data
    except Exception as e:
        print(f"❌ Error loading benchmark data: {e}", file=sys.stderr)
        sys.exit(1)

def group_by_date(data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group data by date (YYYY-MM-DD)."""
    by_date = defaultdict(list)
    
    for record in data:
        try:
            timestamp = record.get('timestamp', '')
            if 'T' in timestamp:
                date = timestamp.split('T')[0]
            else:
                date = timestamp[:10]
            by_date[date].append(record)
        except (AttributeError, IndexError):
            continue
    
    return dict(by_date)

def detect_k_anomaly(data: List[Dict[str, Any]], k_threshold: float = 0.8) -> List[Dict[str, Any]]:
    """
    Detect K-anomalies: days where k% of backends show regressions.
    
    Args:
        data: List of benchmark records
        k_threshold: Fraction of backends that must show regressions (default: 0.8 = 80%)
    
    Returns:
        List of anomaly records
    """
    by_date = group_by_date(data)
    anomalies = []
    
    for date, day_records in by_date.items():
        if len(day_records) < 3:  # Need at least 3 backends
            continue
        
        # Group by backend
        by_backend = defaultdict(list)
        for record in day_records:
            backend = record.get('backend', 'unknown')
            by_backend[backend].append(record)
        
        # Check if enough backends show regressions
        backends_with_regressions = 0
        total_backends = len(by_backend)
        
        for backend, records in by_backend.items():
            if len(records) < 2:  # Need at least 2 records to detect regression
                continue
            
            # Simple regression detection: current vs previous
            records.sort(key=lambda x: x.get('timestamp', ''))
            current = records[-1]
            previous = records[-2] if len(records) > 1 else None
            
            if previous and current.get('mean_ns') and previous.get('mean_ns'):
                regression_ratio = (current['mean_ns'] - previous['mean_ns']) / previous['mean_ns']
                if regression_ratio > 0.1:  # 10% regression threshold
                    backends_with_regressions += 1
        
        # Check if this is a K-anomaly
        if total_backends > 0:
            regression_fraction = backends_with_regressions / total_backends
            if regression_fraction >= k_threshold:
                anomalies.append({
                    'date': date,
                    'total_backends': total_backends,
                    'backends_with_regressions': backends_with_regressions,
                    'regression_fraction': regression_fraction,
                    'likely_infrastructure_issue': True,
                    'records': day_records
                })
    
    return anomalies

def format_anomaly_report(anomalies: List[Dict[str, Any]]) -> str:
    """Format anomaly report for display."""
    if not anomalies:
        return "✅ No K-anomalies detected (infrastructure looks stable)"
    
    report = ["🚨 K-Anomaly Detection Results:", ""]
    
    for anomaly in anomalies:
        date = anomaly['date']
        total = anomaly['total_backends']
        regressed = anomaly['backends_with_regressions']
        fraction = anomaly['regression_fraction']
        
        report.append(f"**Date: {date}**")
        report.append(f"  Backends: {regressed}/{total} showing regressions ({fraction:.1%})")
        report.append(f"  Likely Cause: Infrastructure issue (runner, toolchain, etc.)")
        report.append(f"  Recommendation: Check CI runner logs, toolchain versions")
        report.append("")
    
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Detect K-anomalies in benchmark data")
    parser.add_argument("--input", "-i", type=Path, default=Path("site/benchmarks.json"),
                       help="Path to benchmarks.json file")
    parser.add_argument("--k-threshold", "-k", type=float, default=0.8,
                       help="Fraction of backends that must show regressions (default: 0.8)")
    parser.add_argument("--github-comment", action="store_true",
                       help="Format output for GitHub PR comment")
    
    args = parser.parse_args()
    
    # Load data
    data = load_benchmark_data(args.input)
    
    if not data:
        print("⚠️  No benchmark data found", file=sys.stderr)
        sys.exit(0)
    
    # Detect anomalies
    anomalies = detect_k_anomaly(data, k_threshold=args.k_threshold)
    
    # Generate report
    report = format_anomaly_report(anomalies)
    
    if args.github_comment:
        print("## 🔍 K-Anomaly Detection")
        print("")
        print(report)
        print("")
        print("---")
        print("*Automated infrastructure issue detection*")
    else:
        print(report)
    
    # Exit with error code if anomalies found
    if anomalies:
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Benchmark aggregator - combines all NDJSON results into GitHub Pages data
"""

import json
import pathlib
import statistics
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
RESULTS = ROOT / "bench" / "results"
PAGES = ROOT / "site"

# Create site directory
PAGES.mkdir(parents=True, exist_ok=True)

def load_all_results():
    """Load all benchmark results from NDJSON files"""
    all_rows = []

    if not RESULTS.exists():
        print(f"❌ Results directory not found: {RESULTS}")
        return all_rows

    for p in sorted(RESULTS.glob("*.ndjson")):
        print(f"📖 Reading {p.name}...")
        try:
            with open(p) as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        all_rows.append(data)
                    except json.JSONDecodeError as e:
                        print(f"⚠️ Invalid JSON in {p.name}:{line_num}: {e}")
        except Exception as e:
            print(f"❌ Error reading {p}: {e}")

    print(f"✅ Loaded {len(all_rows)} benchmark results")
    return all_rows

def filter_outliers(data, field='mean_ns', threshold=3.0):
    """Remove outliers using z-score method"""
    if len(data) < 3:
        return data

    values = [row.get(field, 0) for row in data if isinstance(row.get(field), (int, float))]
    if len(values) < 3:
        return data

    mean = statistics.mean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0

    if std == 0:
        return data

    filtered = []
    for row in data:
        value = row.get(field, 0)
        if isinstance(value, (int, float)):
            z_score = abs(value - mean) / std
            if z_score <= threshold:
                filtered.append(row)
        else:
            filtered.append(row)

    return filtered

def aggregate_by_day(data):
    """Aggregate results by day, keeping best performance per backend/test/mode"""
    daily_results = {}

    for row in data:
        if 'error' in row:
            continue  # Skip error results

        timestamp = row.get('timestamp', '')
        if not timestamp:
            continue

        # Extract date (YYYY-MM-DD)
        try:
            date = timestamp.split('T')[0]
        except (AttributeError, IndexError):
            continue

        backend = row.get('backend', 'unknown')
        test = row.get('test', 'unknown')
        mode = row.get('mode', 'unknown')
        parallel = row.get('parallel', False)

        key = (date, backend, test, mode, parallel)

        if key not in daily_results:
            daily_results[key] = []

        daily_results[key].append(row)

    # For each day/backend/test/mode combination, keep the best result
    aggregated = []
    for _key, results in daily_results.items():
        # Filter outliers first
        filtered_results = filter_outliers(results)

        if not filtered_results:
            continue

        # Find the result with the lowest mean_ns (best performance)
        best_result = min(filtered_results, key=lambda x: x.get('mean_ns', float('inf')))
        aggregated.append(best_result)

    return aggregated

def generate_summary_stats(data):
    """Generate summary statistics"""
    backends = set()
    tests = set()
    modes = set()
    dates = set()

    for row in data:
        if 'error' in row:
            continue

        backends.add(row.get('backend', 'unknown'))
        tests.add(row.get('test', 'unknown'))
        modes.add(row.get('mode', 'unknown'))

        timestamp = row.get('timestamp', '')
        if timestamp:
            try:
                date = timestamp.split('T')[0]
                dates.add(date)
            except (AttributeError, IndexError):
                pass

    return {
        'total_results': len(data),
        'backends': sorted(backends),
        'tests': sorted(tests),
        'modes': sorted(modes),
        'date_range': {
            'start': min(dates) if dates else None,
            'end': max(dates) if dates else None
        },
        'last_updated': datetime.utcnow().isoformat() + 'Z'
    }

def main():
    """Main aggregator function"""
    print("📊 PCS Benchmark Aggregator")
    print("=" * 30)

    # Load all results
    all_data = load_all_results()

    if not all_data:
        print("❌ No benchmark data found")
        return

    # Aggregate by day (keep best performance per day/backend/test/mode)
    aggregated_data = aggregate_by_day(all_data)

    # Generate summary statistics
    summary = generate_summary_stats(aggregated_data)

    # Write combined JSON for the dashboard
    output_data = {
        'summary': summary,
        'results': aggregated_data
    }

    output_file = PAGES / "benchmarks.json"
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"✅ Wrote {output_file} with {len(aggregated_data)} aggregated results")

    # Print summary
    print("\n📈 Summary:")
    print(f"   Total results: {summary['total_results']}")
    print(f"   Backends: {', '.join(summary['backends'])}")
    print(f"   Tests: {', '.join(summary['tests'])}")
    print(f"   Date range: {summary['date_range']['start']} to {summary['date_range']['end']}")

    # Count by backend
    backend_counts = {}
    for row in aggregated_data:
        backend = row.get('backend', 'unknown')
        backend_counts[backend] = backend_counts.get(backend, 0) + 1

    print("\n📊 Results by backend:")
    for backend, count in sorted(backend_counts.items()):
        print(f"   {backend}: {count} results")

    print("\n🎉 Aggregation complete!")

if __name__ == "__main__":
    main()

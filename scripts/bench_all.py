#!/usr/bin/env python3
"""
Benchmark orchestrator - runs all backends and collects NDJSON results
"""

import datetime
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "bench" / "results"
GENDIR = ROOT / "generated"
TARGETDIR = ROOT / "target"

# Create directories
OUTDIR.mkdir(parents=True, exist_ok=True)
GENDIR.mkdir(parents=True, exist_ok=True)
TARGETDIR.mkdir(parents=True, exist_ok=True)

today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
outfile = OUTDIR / f"{today}.ndjson"

def run(cmd, cwd=ROOT, shell=False):
    """Run command and return output"""
    try:
        if shell:
            p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
        else:
            p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

        if p.returncode != 0:
            print(f"Command failed: {' '.join(cmd) if isinstance(cmd, list) else cmd}", file=sys.stderr)
            print(f"STDOUT: {p.stdout}", file=sys.stderr)
            print(f"STDERR: {p.stderr}", file=sys.stderr)
            return None
        return p.stdout
    except Exception as e:
        print(f"Error running command: {e}", file=sys.stderr)
        return None

def check_tool(tool, version_cmd):
    """Check if tool is available"""
    print(f"🔍 Checking {tool}...")
    output = run(version_cmd, shell=True)
    if output:
        print(f"✅ {tool}: {output.strip()}")
        return True
    else:
        print(f"❌ {tool} not found")
        return False

def run_backend_bench(backend, script_name, description):
    """Run benchmark for a specific backend"""
    print(f"\n🚀 Running {description} benchmarks...")

    script_path = ROOT / "scripts" / script_name
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return []

    # Make script executable if it's a shell script
    if script_name.endswith(('.jl', '.js', '.go', '.rs')):
        os.chmod(script_path, 0o755)

    # Run the benchmark script
    if script_name.endswith('.jl'):
        cmd = ["julia", str(script_path)]
    elif script_name.endswith('.js'):
        cmd = ["node", str(script_path)]
    elif script_name.endswith('.go'):
        # Compile and run Go script
        go_binary = TARGETDIR / f"bench_{backend}"
        compile_cmd = ["go", "build", "-o", str(go_binary), str(script_path)]
        if run(compile_cmd):
            cmd = [str(go_binary)]
        else:
            return []
    elif script_name.endswith('.rs'):
        # Compile and run Rust script
        rust_binary = TARGETDIR / f"bench_{backend}"
        compile_cmd = ["rustc", "-O", str(script_path), "-o", str(rust_binary)]
        if run(compile_cmd):
            cmd = [str(rust_binary)]
        else:
            return []
    elif script_name.endswith('.cs'):
        # Compile and run C# script
        cs_binary = TARGETDIR / f"bench_{backend}.exe"
        compile_cmd = ["dotnet", "build", str(script_path), "-c", "Release", "-o", str(TARGETDIR)]
        if run(compile_cmd):
            cmd = [str(cs_binary)]
        else:
            return []
    else:
        cmd = [str(script_path)]

    output = run(cmd)
    if not output:
        return []

    # Parse NDJSON output
    lines = []
    for line in output.strip().splitlines():
        line = line.strip()
        if line and line.startswith('{'):
            try:
                json.loads(line)  # Validate JSON
                lines.append(line)
            except json.JSONDecodeError:
                print(f"⚠️ Invalid JSON line: {line}", file=sys.stderr)

    print(f"✅ {description}: {len(lines)} benchmark results")
    return lines

def main():
    """Main benchmark orchestrator"""
    print("🎯 PCS Multi-Backend Benchmark Orchestrator")
    print("=" * 50)

    # Check required tools
    tools_available = {
        'Python': check_tool('Python', 'python3 --version'),
        'Julia': check_tool('Julia', 'julia --version'),
        'Rust': check_tool('Rust', 'rustc --version'),
        'Go': check_tool('Go', 'go version'),
        'Node.js': check_tool('Node.js', 'node --version'),
        'C#': check_tool('C#', 'dotnet --version'),
    }

    if not all(tools_available.values()):
        print("\n❌ Some required tools are missing. Please install them and try again.")
        sys.exit(1)

    # Set environment variables
    os.environ['PCS_BENCH_N'] = '1000000'
    if 'GITHUB_SHA' not in os.environ:
        os.environ['GITHUB_SHA'] = 'local'

    # Collect all benchmark results
    all_lines = []

    # Run Julia benchmarks
    if tools_available['Julia']:
        julia_lines = run_backend_bench('julia', 'bench_julia.jl', 'Julia')
        all_lines.extend(julia_lines)

    # Run Rust benchmarks
    if tools_available['Rust']:
        rust_lines = run_backend_bench('rust', 'bench_rust.rs', 'Rust')
        all_lines.extend(rust_lines)

    # Run Go benchmarks
    if tools_available['Go']:
        go_lines = run_backend_bench('go', 'bench_go.go', 'Go')
        all_lines.extend(go_lines)

    # Run TypeScript benchmarks
    if tools_available['Node.js']:
        ts_lines = run_backend_bench('ts', 'bench_ts.js', 'TypeScript')
        all_lines.extend(ts_lines)

    # Run C# benchmarks
    if tools_available['C#']:
        csharp_lines = run_backend_bench('csharp', 'bench_csharp.cs', 'C#')
        all_lines.extend(csharp_lines)

    # Write results to NDJSON file
    print(f"\n📝 Writing results to {outfile}...")
    with open(outfile, "a") as f:
        for line in all_lines:
            f.write(line.rstrip() + "\n")

    print(f"✅ Wrote {len(all_lines)} benchmark results to {outfile}")

    # Summary
    print("\n📊 Benchmark Summary:")
    print(f"   Total results: {len(all_lines)}")
    print(f"   Output file: {outfile}")

    # Count by backend
    backend_counts = {}
    for line in all_lines:
        try:
            data = json.loads(line)
            backend = data.get('backend', 'unknown')
            backend_counts[backend] = backend_counts.get(backend, 0) + 1
        except json.JSONDecodeError:
            continue

    for backend, count in backend_counts.items():
        print(f"   {backend}: {count} results")

    print("\n🎉 Benchmark orchestration complete!")

if __name__ == "__main__":
    main()

